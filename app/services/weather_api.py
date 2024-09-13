import requests
import logging
from datetime import datetime
from datetime import timezone, timedelta

from app.schemas import (
    PointResponseSchema,
    PointSchema,
    ForecastResponseSchema,
    ForecastSchema,
)


class WeatherApiService:
    def __init__(self, lat: float, long: float, url: str):
        self.lat = lat
        self.long = long
        self.url = url

    def get_point_metadata(self) -> PointSchema | None:
        """
        Get metadata for longitude and latitude, needed to call hourly forecast API
        """
        try:
            res = requests.get(f"{self.url}/points/{self.lat},{self.long}")
            res.raise_for_status()

            data = res.json()
            point = PointResponseSchema.model_validate(data)
            return point.properties

        except requests.HTTPError as err:
            logging.error(
                f"Error fetching endpoints. Network response is {err.response.text}"
            )

    def filter_by_days_ahead(
        self, days_ahead: int, forecast: ForecastResponseSchema, time: datetime
    ) -> ForecastSchema:
        max_time = time + timedelta(days_ahead)

        logging.info(f"Getting forecast until {max_time}")
        result = []

        for hour in forecast.properties.periods:
            if hour.startTime <= max_time:
                result.append(hour)

        return ForecastSchema(periods=result)

    def get_forecast(self, days_ahead: int) -> ForecastSchema | None:
        """
        Get hourly forecast until a specified time
        """
        metadata = self.get_point_metadata()

        if metadata is None:
            logging.error(
                "Invalid latitude and longitude! Please check your environment variables"
            )
            return

        office = metadata.gridId
        x = metadata.gridX
        y = metadata.gridY

        try:
            res = requests.get(
                f"{self.url}/gridpoints/{office}/{x},{y}/forecast/hourly"
            )
            res.raise_for_status()

            data = res.json()

            logging.info("Successfully received data from Weather API")

            forecast = ForecastResponseSchema.model_validate(data)
            now = datetime.now(timezone.utc)
            result = self.filter_by_days_ahead(days_ahead, forecast, now)

            return result

        except requests.HTTPError as err:
            logging.error(
                f"Error fetching forecast. Network response is {err.response.text}"
            )
