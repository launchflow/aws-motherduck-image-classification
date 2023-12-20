# Image Classification: AWS -> MotherDuck with LaunchFlow

This is a simple example of how to use LaunchFlow to classify images as they are uploaded to an S3 bucket, and write the results to a table housed in MotherDuck.

To run this example, you will need to have an AWS account, and a MotherDuck account. You will also need to have the AWS CLI installed and configured with your AWS credentials.

## Setup

Update the [bucket name](https://github.com/launchflow/aws-motherduck-image-classification/blob/main/main.py#L16) in `main.py` to a bucket you would like to write the files in. This bucket does not need to be created yet.

Update the [MotherDuck token](https://github.com/launchflow/aws-motherduck-image-classification/blob/main/main.py#L25) to your [MotherDuck service token](https://motherduck.com/docs/authenticating-to-motherduck/#authentication-using-a-service-token).

## Install Dependencies

```bash
pip install -r requirements.txt
```

## Create your Resources

Be sure to run `aws sso login` before doing this!

Run:

```
buildflow apply
```

And type `yes` to confirm the resources you are about to create.

This will create a S3 bucket, a S3 Notification, and an SQS Queue.

## Run the Example

Run:

```
buildflow run
```

Visit http://localhost:8000 for a simple UI for uploading images. Once uploaded you can view the results in MotherDuck: https://app.motherduck.com

