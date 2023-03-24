"""
Script that zips module code and uploads each versioned module to the corresponding
public bucket hosting our Lambda Zips.
"""
import os
import shutil
import yaml
import boto3

BUCKET_ROOT = "dragondrop-ecs-fargate-task-lambda-trigger"


if __name__ == "__main__":
    print("Beginning job to zip modules and upload modules to GCS storage.")

    # Create the S3 client
    boto_session = boto3.Session()
    s3_client = boto_session.client('s3')

    zip_output_name = f"{os.getcwd()}/src/dragondrop_https_trigger_lambda"
    directory_name = f"{os.getcwd()}/src/"
    shutil.make_archive(zip_output_name, "zip", directory_name)
    print(f"Done zipping lambda code.")

    print(f"Uploading lambda zip to S3.")
    s3_client.upload_file(
        f"{zip_output_name}.zip",
        f"{BUCKET_ROOT}-{os.getenv('ENV')}",
        "dragondrop_https_trigger_lambda.zip"
    )
    print(f"Done uploading lambda zip to S3.")
