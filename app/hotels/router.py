import asyncio
from app.hotels.dao import HotelDAO
from fastapi import APIRouter, Query
from datetime import date, datetime
from app.hotels.schemas import SHotelList
from app.hotels.rooms.schemas import SRoomsList
from app.hotels.rooms.dao import RoomDAO
from fastapi_cache.decorator import cache


router = APIRouter(
    prefix="/hotels",
    tags=["Hotels"]
)


@router.get("/{location}")
@cache(expire=20)
async def get_hotel_by_location_and_time(
         location: str,
         date_from: date = Query(..., description=f"Example, {datetime.now().date()}"),
         date_to: date = Query(..., description=f"Example, {datetime.now().date()}")
        ) -> list[SHotelList]:
    await asyncio.sleep(3)
    hotels = await HotelDAO.get_hotel_by_city(location=location, date_from=date_from, date_to=date_to)
    return hotels


@router.get("/{hotel_id}/rooms")
async def get_rooms_by_time(
        hotel_id: int,
        date_from: date = Query(..., description=f"Example, {datetime.now().date()}"),
        date_to: date = Query(..., description=f"Example, {datetime.now().date()}")
    ) -> list[SRoomsList]:
    rooms = await RoomDAO.find_room_by_id(hotel_id, date_from, date_to)
    return rooms
