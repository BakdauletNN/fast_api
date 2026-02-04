from app.hotels.rooms.dao import RoomDAO
from datetime import date
from fastapi import APIRouter


router = APIRouter(
    prefix="/hotels",
    tags=["Rooms"]
)


@router.get("/{hotel_id}/rooms")
async def get_rooms(hotel_id: int, date_from: date, date_to: date):
    return await RoomDAO.find_all(hotel_id=hotel_id, date_from=date_from, date_to=date_to)