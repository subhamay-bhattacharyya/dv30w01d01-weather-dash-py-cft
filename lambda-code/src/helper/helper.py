import json
from awsservices.s3.s3_bucket import S3Bucket
from awsservices.secret.secrets_manager import Secret
from weathermap.weather_dashboard import WeatherDashboard


def get_secret(logger, config):
    """
    Get the secret from AWS Secrets Manager
    """
    try:
        secret = Secret(logger=logger, config=config)
        secret_value = secret.get_secret(logger=logger)
        return json.loads(secret_value)

    except RuntimeError as e:
        logger.error(f"helper.get_secret -> Exception:{e}", exc_info=True)
        raise RuntimeError(f"helper.get_secret -> Exception:{e}") from e


def get_weather_data(logger, city, api_key, config):
    """
    Get weather data using weather map API
    """
    try:
        weather_dashboard = WeatherDashboard(
            logger=logger, api_key=api_key, config=config
        )
        weather_data = weather_dashboard.get_weather_data(logger=logger, city=city)

        if weather_data:
            extra_logging = {
                "custom_logging": {
                    "temp": weather_data["main"]["temp"],
                    "feelsLike": weather_data["main"]["feels_like"],
                    "humidity": weather_data["main"]["humidity"],
                    "description": weather_data["weather"][0]["description"],
                }
            }
            logger.info(
                f"helper.get_weather_data -> Successfully retrieved weather data for {weather_data['name']}, {weather_data['sys']['country']}",
                extra=extra_logging,
            )

            temp = weather_data["main"]["temp"]
            feels_like = weather_data["main"]["feels_like"]
            humidity = weather_data["main"]["humidity"]
            description = weather_data["weather"][0]["description"]
            city_weather = {
                "temp": temp,
                "feelsLike": feels_like,
                "humidity": humidity,
                "description": description,
            }
            return city_weather

    except RuntimeError as e:
        logger.error(f"helper.get_weather_data -> Exception:{e}", exc_info=True)
        raise RuntimeError(f"helper.get_weather_data -> Exception:{e}") from e


def save_to_s3(logger, key, data, config):
    """
    Save an object to S3 bucket
    """
    try:
        s3_bucket = S3Bucket(logger=logger, config=config)
        response = s3_bucket.put_object(logger=logger, key=key, data=data)

        if response["statusCode"] == 200:
            logger.info(
                f"helper.save_to_s3 -> Successfully saved file {key} \
                    to the bucket {s3_bucket.bucket_name}"
            )
            response = {
                "statusCode": 200,
                "message": f"Successfully saved file {key} to the bucket {s3_bucket.bucket_name}.",
            }
        else:
            logger.error(
                f"helper.save_to_s3 -> Failed to save file {key} to \
                    the bucket {s3_bucket.bucket_name}"
            )
            raise RuntimeError(
                f"helper.save_to_s3 -> Failed to save file {key} to the \
                    bucket {s3_bucket.bucket_name}"
            )

        return response

    except Exception as e:
        logger.error(f"helper.save_to_s3 -> Exception:{e}", exc_info=True)
        raise RuntimeError(f"helper.save_to_s3 -> Exception:{e}") from e
