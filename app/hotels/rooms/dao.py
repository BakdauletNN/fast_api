from app.service.base import Base
from datetime import date
from app.database import session_maker
from sqlalchemy import and_, select, func
from app.hotels.rooms.models import Rooms
from app.bookings.models import Bookings


class RoomDAO(Base):
    model = Rooms

    class RoomDAO(Base):
        model = Rooms

        @classmethod
        async def find_all(cls, hotel_id: int, date_from: date, date_to: date):
            async with session_maker() as session:
                booked_rooms = (
                    select(Bookings.room_id)
                    .where(
                        and_(
                            Bookings.date_from <= date_to,
                            Bookings.date_to >= date_from
                        )
                    )
                    .cte("booked_rooms")
                )

                query = (
                    select(
                        Rooms.id,
                        Rooms.hotel_id,
                        Rooms.name,
                        Rooms.description,
                        Rooms.services,
                        Rooms.price,
                        Rooms.quantity,
                        Rooms.image_id,
                        (Rooms.quantity - func.count(booked_rooms.c.room_id)).label("rooms_left"),
                        ((date_to - date_from).days * Rooms.price).label("total_cost"),
                    )
                    .select_from(Rooms)
                    .join(
                        booked_rooms,
                        booked_rooms.c.room_id == Rooms.id,
                        isouter=True
                    )
                    .where(Rooms.hotel_id == hotel_id)
                    .group_by(
                        Rooms.id,
                        Rooms.hotel_id,
                        Rooms.name,
                        Rooms.description,
                        Rooms.services,
                        Rooms.price,
                        Rooms.quantity,
                        Rooms.image_id,
                    )
                )

                res = await session.execute(query)
                return res.mappings().all()

