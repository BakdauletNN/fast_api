from app.service.base import Base
from app.hotels.models import Hotels
from datetime import date
from app.database import session_maker
from sqlalchemy import and_, or_, select, func
from app.hotels.rooms.models import Rooms
from app.bookings.models import Bookings


class HotelDAO(Base):
    model = Hotels

    @classmethod
    async def get_hotel_by_city(cls, location: str,  date_from: date, date_to: date):
        """
        subquery for bookings which intersection with booked_rooms
        """
        async with session_maker() as session:
            booked_rooms = (
                select(Bookings.room_id).where(
                    or_(
                        and_(
                            Bookings.date_from >= date_from,
                            Bookings.date_from <= date_to
                        ),
                        and_(
                            Bookings.date_from <= date_from,
                            Bookings.date_to >= date_from
                        ),
                    )
                ).subquery()
            )

            rooms_left_expr = (
                    func.sum(Rooms.quantity) - func.count(booked_rooms.c.room_id)
            ).label("rooms_left")

            query = (
                select(
                    Hotels.id,
                    Hotels.name,
                    Hotels.location,
                    Hotels.services,
                    Hotels.rooms_qty,
                    Hotels.image_id,
                    rooms_left_expr
                )
                .select_from(Hotels)
                .join(Rooms, Rooms.hotel_id == Hotels.id)
                .outerjoin(
                    booked_rooms,
                    booked_rooms.c.room_id == Rooms.id
                )
                .where(Hotels.location == location)
                .group_by(
                    Hotels.id,
                    Hotels.name,
                    Hotels.location,
                    Hotels.services,
                    Hotels.rooms_qty,
                    Hotels.image_id
                )
                .having(
                    func.sum(Rooms.quantity) - func.count(booked_rooms.c.room_id) > 0
                )

            )

            result = await session.execute(query)
            return result.mappings().all()




