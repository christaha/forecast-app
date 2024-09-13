import logging

from sqlalchemy.orm import Session
from sqlalchemy import and_, func
from datetime import datetime, timezone
from app.schemas import ForecastSchema, TempSummarySchema
from app.models import Location, Forecast
from datetime import date


def save_temp_data(db: Session, forecast: ForecastSchema, location: Location):
    """
    Parse and save temperature data from a forecast
    """
    logging.info(f"Saving temperature data for {len(forecast.periods)} hours")
    result = []
    current_time = datetime.now(timezone.utc)

    for hour in forecast.periods:
        new_hour = Forecast(
            added_date=current_time,
            start_time=hour.startTime,
            end_time=hour.endTime,
            temperature=hour.temperature,
            location_id=location.id,
        )
        result.append(new_hour)

    db.add_all(result)
    db.commit()


def get_temp_summary(
    db: Session, lat: float, long: float, date: date, hour: int
) -> TempSummarySchema | None:
    """
    Get minumum and maximum recorded temperature for a date, hour, and location
    """
    startTime = datetime(date.year, date.month, date.day, hour)

    query = (
        db.query(
            func.min(Forecast.temperature).label("min_temp"),
            func.max(Forecast.temperature).label("max_temp"),
        )
        .join(Location, Forecast.location_id == Location.id)
        .where(
            and_(
                Location.latitude == lat,
                Location.longitude == long,
                Forecast.start_time == startTime,
            )
        )
        .group_by(Location.longitude, Location.latitude, Forecast.start_time)
    )

    result = query.first()

    if result is None:
        return None

    return TempSummarySchema(min_temp=result.min_temp, max_temp=result.max_temp)
