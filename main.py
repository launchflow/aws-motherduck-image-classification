"""This application classifies images uploaded to S3 and writes the output to MotherDuck."""
import dataclasses
import datetime
import hashlib
import os

from buildflow import Flow
from buildflow.dependencies.bucket import BucketDependencyBuilder
from buildflow.io.aws import S3FileChangeStream, S3Bucket
from buildflow.io.duckdb import DuckDBTable
from buildflow.requests import UploadFile
from buildflow.responses import FileResponse
from buildflow.types.aws import S3FileChangeEvent
import dotenv

from image_classification import Model

dotenv.load_dotenv()

# Define the resources that we will use.
# 1. An S3 bucket that images will be uploaded to
# 2. A DuckDB table stored in MotherDuck that the results of the image classification
#    will be written to (this table will be created when we write to it).
# 3. A file change stream that will emit events when files are uploaded to the S3
#    bucket.
bucket = S3Bucket(
    bucket_name=os.environ["S3_BUCKET_NAME"], aws_region="us-east-1"
).options(force_destroy=True)

source = S3FileChangeStream(s3_bucket=bucket)
motherduck_table = DuckDBTable(
    database="md:launchflow_image_classification", table="image_classification"
)


app = Flow()
# Mark our bucket and change stream as managed resources. This means that they will be
# create / updated when running `buildflow apply`. This will specifically create:
# 1. The S3 bucket
# 2. An S3 bucket notification that will send events to our change stream when files
#    are uploaded to the bucket.
# 3. An SQS Queue that events will be sent to and consumed from.
app.manage(bucket, source)


# Define the scheme of our table in MotherDuck. When our table is created it will have a
# schema matching this definition.
@dataclasses.dataclass
class ImageClassificationRow:
    image_id: str
    image_name: str
    upload: str
    classification: str
    confidence: float


# This consumer will be run when events are emitted from our change stream (i.e.
# when a new file is uploaded to our bucket). It will classify the image and return
# the results as a list of ImageClassificationRow objects. The returned results will be
# written to our table, one row for each element returned.
@app.consumer(source=source, sink=motherduck_table)
def classify_image(
    file_event: S3FileChangeEvent, model: Model
) -> ImageClassificationRow:
    upload_time = datetime.datetime.utcnow().isoformat()
    image_id = hashlib.sha256(
        f"{file_event.file_path}{upload_time}".encode("utf-8")
    ).hexdigest()
    classifications = model.predict(file_event.blob)
    if classifications is not None:
        print(
            "Image classified (results can be viewed in MotherDuck): ", classifications
        )
        return [
            ImageClassificationRow(
                image_id,
                file_event.file_path,
                upload_time,
                **dataclasses.asdict(c),
            )
            for c in classifications
        ]


# Below we define a simple service to make it easier to upload images to the provided
# bucket. When you run the application this can be viewed at http://localhost:8000
service = app.service(service_id="image-classification")
BucketDep = BucketDependencyBuilder(bucket)


@service.endpoint("/", method="GET")
def index():
    return FileResponse("index.html")


@service.endpoint("/image-upload", method="POST")
def image_upload(image_file: UploadFile, bucket_dep: BucketDep):
    bucket_dep.bucket.put_object(Key=image_file.filename, Body=image_file.file)
