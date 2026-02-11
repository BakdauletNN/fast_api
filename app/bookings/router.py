from fastapi import APIRouter, Depends, Response, HTTPException
from app.users.models import Users
from app.bookings.dao import BookingService
from app.users.dependencies import get_cur_user
from app.bookings.schemas import SBookingsList, SBookings
from datetime import date
from app.exceptions import RoomCannorBeCooked
from pydantic import parse_obj_as
from app.tasks.tasks import send_booking_confrim_email


router = APIRouter(
    prefix="/bookings",
    tags=["Bookings"],
)


@router.get("")
async def get_bookings(user: Users = Depends(get_cur_user)) -> list[SBookingsList]:
    return await BookingService.find_all_info_booking(user_id=user.id)


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
    booking_dict = parse_obj_as(SBookings, booking).dict()
    send_booking_confrim_email.delay(booking_dict, user.email)
    return booking_dict


@router.delete("/{id_booking}")
async def del_booking(
    id_booking: int,
    user: Users = Depends(get_cur_user)  # authorization
):
    result = await BookingService.delete(id_model=id_booking, user_id=user.id)
    if result:
        return Response(status_code=204)  # no content
    raise HTTPException(status_code=404, detail="Booking not found")
