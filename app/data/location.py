from sqlalchemy.orm import Session
from sqlalchemy import and_, select
from app.models import Location


def get_location(db: Session, lat: float, long: float) -> Location | None:
    """
    Get location for a latitude and longitude point.
    """
    query = select(Location).where(
        and_(Location.latitude == lat, Location.longitude == long)
    )
    return db.scalars(query).first()


def create_location(db: Session, lat: float, long: float) -> Location | None:
    """
    Create location for a latitude and longitude point.
    """
    location = Location(latitude=lat, longitude=long)

    db.add(location)
    db.commit()

    return location
