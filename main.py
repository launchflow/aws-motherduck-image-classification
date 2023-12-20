import dataclasses
import datetime
from typing import List

from buildflow import Flow
from buildflow.dependencies.bucket import BucketDependencyBuilder
from buildflow.io.aws import S3FileChangeStream, S3Bucket
from buildflow.io.duckdb import DuckDBTable
from buildflow.requests import UploadFile
from buildflow.responses import FileResponse
from buildflow.types.aws import S3FileChangeEvent

from image_classification import Classification, Model


bucket = S3Bucket(
    bucket_name="caleb-buildflow-motherduck",
    aws_region="us-east-1",
).options(force_destroy=True)

source = S3FileChangeStream(s3_bucket=bucket)
motherduck_table = DuckDBTable(
    database="md:launchflow_image_classification",
    table="image_classification",
    motherduck_token="TODO",
)


app = Flow()
app.manage(bucket, source)

service = app.service(service_id="image-classification")


BucketDep = BucketDependencyBuilder(bucket)


@service.endpoint("/", method="GET")
def index():
    return FileResponse("index.html")


@service.endpoint("/image-upload", method="POST")
def image_upload(image_file: UploadFile, bucket_dep: BucketDep):
    bucket_dep.bucket.put_object(Key=image_file.filename, Body=image_file.file)


@dataclasses.dataclass
class ImageClassificationRow:
    image_name: str
    upload: str
    classifications: List[Classification]


@app.consumer(source=source, sink=motherduck_table)
def classify_image(
    file_event: S3FileChangeEvent, model: Model
) -> ImageClassificationRow:
    classification = ImageClassificationRow(
        image_name=file_event.file_path,
        upload=datetime.datetime.utcnow().isoformat(),
        classifications=model.predict(file_event.blob),
    )
    print("Image classified (results can be viewed in MotherDuck): ", classification)
    return classification
