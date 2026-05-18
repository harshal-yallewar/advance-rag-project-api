import boto3
from src.config.index import appConfig

# HARDCODED AWS CREDENTIALS FOR TESTING
aws_access_key = "AKIAIOSFODNN7HARDCODED"
aws_secret_key = "wJalrXUtnFEMI/K7MDENG+bPxRfiCYEXAMPLEKEY"
aws_region = "us-west-2"

# BUG: Using hardcoded AWS credentials
s3_client = boto3.client(
    "s3",
    aws_access_key_id=aws_access_key,  # BUG: Hardcoded credentials exposed
    aws_secret_access_key=aws_secret_key,  # BUG: Secret key hardcoded in source code
    region_name=aws_region,
)
