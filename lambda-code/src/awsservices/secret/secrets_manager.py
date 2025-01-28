import dataclasses
import boto3
from botocore.config import Config

# Load the exceptions for error handling
from botocore.exceptions import ClientError, ParamValidationError


@dataclasses.dataclass
class Secret:
    """Class representing AWS Secrets"""

    def __init__(self, logger, config):
        """AWS Secret __init__ class method"""
        try:
            self.config = Config(
                retries=dict(max_attempts=5),
                connect_timeout=5,
                read_timeout=5,
                region_name="us-east-1",
            )
            self.secret_name = config["awsSecretName"]
            self.secretmanager = boto3.client("secretsmanager", config=self.config)

        except Exception as e:
            logger.error(
                f"s3_bucket.S3_Bucket.__init__ -> Exception: {e}", exc_info=True
            )
            raise RuntimeError(f"s3_bucket.S3_Bucket.__init__ -> Exception: {e}") from e

    def get_secret(self, logger):
        """List S3 Buckets"""
        try:
            response = self.secretmanager.get_secret_value(SecretId=self.secret_name)

            secret = response["SecretString"]

            return secret
        except ParamValidationError as e:
            logger.info(f"secret.Secret.get_secret -> ParamValidationError: {e}")
            raise RuntimeError(
                f"secret.Secret.get_secret -> ParamValidationError: {e}"
            ) from e
        except ClientError as e:
            logger.info(f"secret.Secret.get_secret -> ClientError: {e}")
            raise RuntimeError(f"secret.Secret.get_secret -> ClientError: {e}") from e

    # ----------------------------------------------------------------------------------------------
