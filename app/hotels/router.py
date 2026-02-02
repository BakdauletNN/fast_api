from app.hotels.dao import HotelDAO
from fastapi import APIRouter
from datetime import date
from typing import Optional


router = APIRouter(
    prefix="/hotels",
    tags=["Hotels"]
)


@router.get("/{location}")
async def get_hotels(location: str, date_from: Optional[date] = None, date_to: Optional[date] = None):
    return await HotelDAO.find_all(location=location)