from app.hotels.dao import HotelDAO
from fastapi import APIRouter
from datetime import date


router = APIRouter(
    prefix="/hotels",
    tags=["Hotels"]
)


@router.get("/{location}")
async def get_hotel(location: str, date_from: date, date_to: date):
    return await HotelDAO.get_hotel_by_city(location=location, date_from=date_from, date_to=date_to)