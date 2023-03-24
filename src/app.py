import boto3


def handler(event, context):
    """Handler"""
    print("Hello World!")
    print(boto3.__version__)
