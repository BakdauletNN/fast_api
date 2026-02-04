from app.hotels.dao import HotelDAO
from fastapi import APIRouter, Query
from datetime import date, datetime
from app.hotels.schemas import SHotel
from app.hotels.rooms.schemas import SRooms


router = APIRouter(
    prefix="/hotels",
    tags=["Hotels"]
)


@router.get("/{location}")
async def get_hotel_by_location_and_time(
         location: str,
         date_from: date = Query(..., description=f"Example, {datetime.now().date()}"),
         date_to: date = Query(..., description=f"Example, {datetime.now().date()}")
        ) -> list[SHotel]:
    hotels = await HotelDAO.get_hotel_by_city(location=location, date_from=date_from, date_to=date_to)
    return hotels


@router.get("{hotel_id}/rooms")
async def get_rooms_by_time(
        hotel_id: int,
        date_from: date = Query(..., description=f"Example, {datetime.now().date()}"),
        date_to: date = Query(..., description=f"Example, {datetime.now().date()}")
    ) -> list[SRooms]:
    rooms = await HotelDAO.get_hotel_by_city(hotel_id, date_from, date_to)
    return rooms
