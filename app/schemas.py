from pydantic import BaseModel
from datetime import datetime


class PointSchema(BaseModel):
    """
    Metadata on a latitude and longitude point
    """

    gridId: str
    gridX: int
    gridY: int


class PointResponseSchema(BaseModel):
    """
    Point Metadata response from the Weather API
    """

    properties: PointSchema


class HourSchema(BaseModel):
    """
    Temperature data for one hour
    """

    startTime: datetime
    endTime: datetime
    temperature: int
    number: int


class ForecastSchema(BaseModel):
    """
    Hourly forecast data for a location
    """

    periods: list[HourSchema]


class ForecastResponseSchema(BaseModel):
    """
    Hourly forecast response from the Weather API
    """

    properties: ForecastSchema


class TempSummarySchema(BaseModel):
    """
    Min and max recorded temperature
    """

    min_temp: int
    max_temp: int
