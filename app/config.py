from pydantic import Field
from pydantic_settings import BaseSettings
from dotenv import load_dotenv

load_dotenv()


class Settings(BaseSettings):
    latitude: float
    longitude: float
    days_ahead: int = Field(default=3)
    interval: float = Field(default=60)
    pg_password: str
    pg_username: str
    pg_host: str
    pg_port: int = Field(default=5432)
    pg_database: str
    weather_api_url: str
    version: str


settings = Settings()
