import asyncio

from app.services.weather_api import WeatherApiService
from app.config import settings
from app.data.forecast import save_temp_data
from app.data.location import get_location, create_location
from app.db import SessionLocal
import logging


class ForecastTracker:
    async def track_forecast(self):
        """
        Collect forecast data from the Weather API
        """
        forecast_service = WeatherApiService(
            settings.latitude, settings.longitude, settings.weather_api_url
        )

        data = forecast_service.get_forecast(settings.days_ahead)

        if data is None:
            return

        with SessionLocal() as db:
            # Create location in the db if it hasn't been seen yet
            location = get_location(db, settings.latitude, settings.longitude)

            if location is None:
                location = create_location(db, settings.latitude, settings.longitude)

            # Save temperature data from the forecast
            save_temp_data(db, data, location)

    async def start(self):
        """
        Start forecast tracker to run on an interval
        """
        logging.info(
            f"Starting forecast tracker to run every {settings.interval} minutes"
        )

        while True:
            await self.track_forecast()
            await asyncio.sleep(settings.interval * 60)
