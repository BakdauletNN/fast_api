from fastapi import APIRouter, Depends
from app.users.models import Users
from app.bookings.dao import BookingService
from app.users.dependencies import get_cur_user
from app.bookings.schemas import SBookings
from datetime import date
from app.exceptions import RoomCannorBeCooked


router = APIRouter(
    prefix="/bookings",
    tags=["Bookings"],
)


@router.get("")
async def get_bookings(user: Users = Depends(get_cur_user)) -> list[SBookings]:
    return await BookingService.find_all(user_id=user.id)


@router.post("")
async def add_booking(
    room_id: int,
    date_from: date,
    date_to: date,
    user: Users = Depends(get_cur_user)
):
    booking = await BookingService.add_booking(user.id, room_id, date_from, date_to)
    if not booking:
        raise RoomCannorBeCooked


@router.delete("/{id_booking}")
async def del_booking(id_booking: int):
    return await BookingService.delete(id_model=id_booking)
