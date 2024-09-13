from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from datetime import date

from app.data.forecast import get_temp_summary
from app.db import get_db
from app.schemas import TempSummarySchema


router = APIRouter(prefix="/temperature", tags=["Temperature Endpoints"])


@router.get(
    "",
    status_code=status.HTTP_200_OK,
    summary="Gets min and max temperatures at a given location and time",
)
async def get_temp_data(
    latitude: float,
    longitude: float,
    date: date,
    hour: int,
    db: Session = Depends(get_db),
) -> TempSummarySchema | None:
    data = get_temp_summary(db, latitude, longitude, date, hour)

    if data is None:
        detail = f"No matching data found for ({latitude}, {longitude}) at {date} on hour {hour}"
        raise HTTPException(status_code=404, detail=detail)

    return data
