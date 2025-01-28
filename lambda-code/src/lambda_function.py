"" "Lambda function to get weather data for a list of cities and save it to S3" ""
import os
import json
from datetime import datetime
from helper import json_logger
from helper import helper

logger = json_logger.setup_logger()

# Open and read the JSON file
with open(f"{os.getcwd()}/config.json", "r", encoding="utf-8") as file:
    config = json.load(file)


def lambda_handler(event, context):
    """Lambda function to get weather data for a list of cities and save it to S3"""

    try:
        secret_string = helper.get_secret(logger=logger, config=config)
        date = datetime.now().strftime("%Y-%m-%d")
        time = datetime.now().strftime("%H-%M-%S")
        cities = event.get("cities", [])
        for city in cities:
            weather_data = helper.get_weather_data(
                logger=logger, city=city, api_key=secret_string["APIKey"], config=config
            )

            response = helper.save_to_s3(
                logger=logger,
                key=f"weather-data/{date}/{time}/{city.replace(' ','-').lower()}.json",
                data=json.dumps(weather_data),
                config=config,
            )

        response = {
            "statusCode": response["statusCode"],
            "awsRequestId": context.aws_request_id,
        }
        return response
    except RuntimeError as e:
        logger.error("An error occurred: %s", e)
        response = {"statusCode": 500}
        return response
