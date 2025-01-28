import json
import dataclasses
import boto3
from botocore.config import Config

# Load the exceptions for error handling
from botocore.exceptions import ClientError, ParamValidationError


@dataclasses.dataclass
class S3Bucket:
    """Class representing S3 Buckets"""

    def __init__(self, logger, config):
        """S3 Bucket __init__ class method"""
        try:
            self.bucket_name = config["s3bBucketName"]
            self.kms_key_id = config["kmsKeyId"]
            self.content_type = config["contentType"]
            self.encryption_type = config["encryptionType"]

            # Print the contents of the JSON file
            self.config = Config(
                retries=dict(max_attempts=5),
                connect_timeout=5,
                read_timeout=5,
                region_name="us-east-1",
            )
            self.s3 = boto3.client("s3", config=self.config)
            self.s3_buckets = []

        except Exception as e:
            logger.error(
                f"s3_bucket.S3_Bucket.__init__ -> Exception: {e}", exc_info=True
            )
            raise RuntimeError(f"s3_bucket.S3_Bucket.__init__ -> Exception: {e}") from e

    def put_object(self, logger, key, data):
        """Put an object to the S3 bucket"""
        try:
            response = self.s3.put_object(
                Bucket=self.bucket_name,
                Key=key,
                Body=data,
                ContentType=self.content_type,
                ServerSideEncryption=self.encryption_type,  # Use KMS for server-side encryption
                SSEKMSKeyId=self.kms_key_id,
            )
            logger.info(f"s3_bucket.S3_Bucket.put_object -> response: {response}")

            if response["ResponseMetadata"]["HTTPStatusCode"] == 200:
                return {
                    "statusCode": 200,
                    "message": f"Object :{key} uploaded successfully",
                }
            else:
                return {
                    "statusCode": response["ResponseMetadata"]["HTTPStatusCode"],
                    "message": f"Object :{key} failed to upload !",
                }
        except ParamValidationError as e:
            logger.error(
                f"s3_bucket.S3_Bucket.put_object -> ParamValidationError: {e}",
                exc_info=True,
            )
            raise RuntimeError(
                f"s3_bucket.S3_Bucket.put_object -> ParamValidationError: {e}"
            ) from e
        except ClientError as e:
            logger.error(
                f"s3_bucket.S3_Bucket.put_object -> ClientError: {e}", exc_info=True
            )
            raise RuntimeError(
                f"s3_bucket.S3_Bucket.put_object -> ClientError: {e}"
            ) from e

    # ----------------------------------------------------------------------------------------------
