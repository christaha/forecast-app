from typing import Optional
from sqlalchemy import ForeignKey
from sqlalchemy.orm import relationship, mapped_column, Mapped
from datetime import datetime
from sqlalchemy.orm import declarative_base
from app.db import engine

Base = declarative_base()


class Location(Base):
    __tablename__ = "location"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    latitude: Mapped[Optional[float]]
    longitude: Mapped[Optional[float]]

    forecasts: Mapped[list["Forecast"]] = relationship(back_populates="location")


class Forecast(Base):
    __tablename__ = "forecast"
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    added_date: Mapped[datetime]
    start_time: Mapped[datetime]
    end_time: Mapped[datetime]
    temperature: Mapped[int]
    location_id: Mapped[int] = mapped_column(ForeignKey("location.id"))

    location: Mapped["Location"] = relationship(back_populates="forecasts")


Base.metadata.create_all(engine)
