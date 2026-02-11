from app.service.base import Base
from datetime import date
from app.database import session_maker
from sqlalchemy import and_, select, func
from app.hotels.rooms.models import Rooms
from app.bookings.models import Bookings


class RoomDAO(Base):
    model = Rooms

    @classmethod
    async def find_room_by_id(cls, hotel_id: int, date_from: date, date_to: date):
        async with session_maker() as session:
            # 1. Берем все комнаты отеля
            rooms_query = (
                select(Rooms)
                .where(Rooms.hotel_id == hotel_id)
            )
            rooms_result = await session.execute(rooms_query)
            rooms = rooms_result.scalars().all()

            # 2. Для каждой комнаты считаем забронированные
            result = []
            days_diff = (date_to - date_from).days

            for room in rooms:
                # Подсчет броней для конкретной комнаты
                booked_query = (
                    select(func.count(Bookings.id))
                    .where(
                        Bookings.room_id == room.id,
                        and_(
                            Bookings.date_from <= date_to,
                            Bookings.date_to >= date_from
                        )
                    )
                )
                booked_count_result = await session.execute(booked_query)
                booked_count = booked_count_result.scalar() or 0

                rooms_left = room.quantity - booked_count

                if rooms_left > 0:  # Только свободные комнаты
                    result.append({
                        "id": room.id,
                        "hotel_id": room.hotel_id,
                        "name": room.name,
                        "description": room.description,
                        "services": room.services,
                        "price": room.price,
                        "quantity": room.quantity,
                        "image_id": room.image_id,
                        "rooms_left": rooms_left,
                        "total_cost": days_diff * room.price
                    })

            return result



