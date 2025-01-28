import dataclasses
import requests
from botocore.config import Config

# Load the exceptions for error handling
from botocore.exceptions import ClientError, ParamValidationError
import requests
import json


@dataclasses.dataclass
class WeatherDashboard:
    """Class representing Weather Dashboard"""

    def __init__(self, logger, api_key, config):
        """AWS WeatherDashboard __init__ class method"""
        try:
            self.base_url = config["baseURL"]
            self.api_version = config["apiVersion"]
            self.api_url = f"{self.base_url}/{self.api_version}/weather"
            self.api_key = api_key

        except Exception as e:
            logger.error(
                f"s3_bucket.WeatherDashboard.__init__ -> Exception: {e}", exc_info=True
            )
            raise RuntimeError(
                f"weather_dashboard.WeatherDashboard.__init__ -> Exception: {e}"
            ) from e

    def get_weather_data(self, logger, city):
        """Get the weather data from using the open weather API"""
        try:
            params = {"q": city, "appid": self.api_key, "units": "imperial"}
            response = requests.get(url=self.api_url, params=params)
            response.raise_for_status()
            return response.json()

        except ParamValidationError as e:
            logger.info(f"secret.Secret.get_secret -> ParamValidationError: {e}")
            raise RuntimeError(
                f"secret.Secret.get_secret -> ParamValidationError: {e}"
            ) from e
        except ClientError as e:
            logger.info(f"secret.Secret.get_secret -> ClientError: {e}")
            raise RuntimeError(f"secret.Secret.get_secret -> ClientError: {e}") from e

    # ----------------------------------------------------------------------------------------------
