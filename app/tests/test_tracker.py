from app.services.weather_api import WeatherApiService
from app.schemas import ForecastResponseSchema, ForecastSchema, HourSchema
from datetime import datetime, timezone


def test_time_filter():
    now1 = datetime(2024, 8, 8, 12, 0, 0, tzinfo=timezone.utc)
    now2 = datetime(2024, 8, 8, 12, 50, 0, tzinfo=timezone.utc)
    now3 = datetime(2024, 8, 8, 11, 0, 0, tzinfo=timezone.utc)

    api = WeatherApiService(50, -50, "https://api.weather.gov")

    forecast = ForecastResponseSchema(
        properties=ForecastSchema(
            periods=[
                HourSchema(
                    startTime=datetime(2024, 8, 8, 12, 0, 0, tzinfo=timezone.utc),
                    endTime=datetime(2024, 8, 8, 13, 0, 0, tzinfo=timezone.utc),
                    temperature=70,
                    number=1,
                ),
                HourSchema(
                    startTime=datetime(2024, 8, 8, 13, 0, 0, tzinfo=timezone.utc),
                    endTime=datetime(2024, 8, 8, 14, 0, 0, tzinfo=timezone.utc),
                    temperature=70,
                    number=2,
                ),
                HourSchema(
                    startTime=datetime(2024, 8, 10, 12, 0, 0, tzinfo=timezone.utc),
                    endTime=datetime(2024, 8, 10, 13, 0, 0, tzinfo=timezone.utc),
                    temperature=71,
                    number=3,
                ),
                HourSchema(
                    startTime=datetime(2024, 8, 10, 14, 0, 0, tzinfo=timezone.utc),
                    endTime=datetime(2024, 8, 10, 15, 0, 0, tzinfo=timezone.utc),
                    temperature=72,
                    number=4,
                ),
                HourSchema(
                    startTime=datetime(2024, 8, 11, 13, 0, 0, tzinfo=timezone.utc),
                    endTime=datetime(2024, 8, 11, 14, 0, 0, tzinfo=timezone.utc),
                    temperature=72,
                    number=5,
                ),
            ]
        )
    )

    result1 = api.filter_by_days_ahead(2, forecast, now1)
    result2 = api.filter_by_days_ahead(2, forecast, now2)
    result3 = api.filter_by_days_ahead(2, forecast, now3)

    assert len(result1.periods) == 3
    assert result1.periods[0].number == 1
    assert result1.periods[1].number == 2
    assert result1.periods[2].number == 3

    assert len(result2.periods) == 3
    assert result1.periods[0].number == 1
    assert result1.periods[1].number == 2
    assert result1.periods[2].number == 3

    assert len(result3.periods) == 2
    assert result1.periods[0].number == 1
    assert result1.periods[1].number == 2
