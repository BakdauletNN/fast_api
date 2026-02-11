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
    async def get_hotel_by_city(cls, location: str, date_from: date, date_to: date):
        async with session_maker() as session:
            # basic query for DB without  subquery
            base_query = (
                select(
                    Hotels.id,
                    Hotels.name,
                    Hotels.location,
                    Hotels.services,
                    Hotels.rooms_qty,
                    Hotels.image_id
                )
                .where(Hotels.location.ilike(f"%{location}%"))
            )

            # get hotels
            hotels_result = await session.execute(base_query)
            hotels_data = hotels_result.mappings().all()

            # for each hotel counting free rooms
            result = []
            for hotel_row in hotels_data:
                # Counting booked rooms for a specific hotel
                booked_query = (
                    select(func.count(Bookings.room_id))
                    .join(Rooms, Rooms.id == Bookings.room_id)
                    .where(
                        Rooms.hotel_id == hotel_row.id,
                        or_(
                            and_(Bookings.date_from >= date_from, Bookings.date_from <= date_to),
                            and_(Bookings.date_from <= date_from, Bookings.date_to >= date_from),
                        )
                    )
                )

                booked_count = await session.execute(booked_query)
                total_booked = booked_count.scalar()
                # General amount of rooms in a hotel
                rooms_query = (
                    select(func.sum(Rooms.quantity))
                    .where(Rooms.hotel_id == hotel_row.id)
                )
                total_rooms_result = await session.execute(rooms_query)
                total_rooms = total_rooms_result.scalar() or 0
                rooms_left = total_rooms - (total_booked or 0)

                if rooms_left > 0:
                    result.append({
                        **dict(hotel_row),
                        "rooms_left": rooms_left
                    })

            return result

