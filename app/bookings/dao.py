from app.hotels.rooms.models import Rooms
from app.service.base import Base
from app.bookings.models import Bookings
from datetime import date
from sqlalchemy import select, delete, insert, and_, or_, func
from app.database import engine, session_maker


class BookingService(Base):
    model = Bookings

    @classmethod
    async def add_booking(cls, user_id: int, room_id: int, date_from: date, date_to: date):

        """
        -- Example input datas

        -- Date_from '2023-05-15'
        -- Date_to '2023-06-20'
        -- Room id 1
        WITH booked_rooms AS(
            SELECT * FROM bookings
            WHERE room_id = 1 AND
            (date_from >= '2033-05-15' AND date_from <= '2023-06-20') OR
            (date_from <= '2033-05-15' AND date_to >  '2023-05-15')
        )
        """
        async with session_maker() as session:
            booked_rooms = select(Bookings).where(
                and_(
                    Bookings.room_id == room_id,
                    or_(
                        and_(
                            Bookings.date_from >= date_from,
                            Bookings.date_from <= date_to

                        ),
                        and_(
                            Bookings.date_from <= date_from,
                            Bookings.date_to >= date_from

                        )

                    )
                )
            ).cte("booked_rooms")


            """
                SELECT rooms.quantity - COUNT(booked_rooms.room_id) FROM rooms
                LEFT JOIN booked_rooms ON booked_rooms.room_id = rooms.id
                WHERE rooms.id = 1
                GROUP BY rooms.quantity, booked_rooms.room_id
            """
            get_rooms_left = select(Rooms.quantity - func.count(booked_rooms.c.room_id).label("rooms_left")
                                ).select_from(Rooms).join(
                booked_rooms, booked_rooms.c.room_id == Rooms.id, isouter=True
            ).where(Rooms.id == room_id).group_by(
                Rooms.quantity, booked_rooms.c.room_id
            )
            print(get_rooms_left.compile(engine, compile_kwargs={"literal_binds" : True}))
            rooms_left = await session.execute(get_rooms_left)
            rooms_left: int = rooms_left.scalar()
            if rooms_left > 0:
                get_price = select(Rooms.price).filter_by(id=room_id)
                price = await session.execute(get_price)
                price: int = price.scalar()
                add_booking = insert(Bookings).values(
                    room_id=room_id,
                    user_id=user_id,
                    date_from=date_from,
                    date_to=date_to,
                    price=price
                ).returning(Bookings)
                new_booking = await session.execute(add_booking)
                await session.commit()
                return new_booking.scalar()

            else:
                return None

    @classmethod
    async def find_all_info_booking(cls, **filter_by):
        async with session_maker() as session:
            user_id = filter_by.get('user_id')

            query = (
                select(
                    Bookings.id,
                    Bookings.room_id,
                    Bookings.user_id,
                    Bookings.date_from,
                    Bookings.date_to,
                    Bookings.price,
                    Rooms.image_id,
                    Rooms.name,
                    Rooms.description,
                    Rooms.services,
                )
                .select_from(Bookings)
                .join(Rooms, Rooms.id == Bookings.room_id)
                .where(Bookings.user_id == user_id)
            )

            result = await session.execute(query)
            bookings = result.mappings().all()
            print(f"Raw bookings: {bookings}")

            # Calculate total_days & total_cost
            processed_bookings = []
            for booking in bookings:
                total_days = (booking["date_to"] - booking["date_from"]).days
                total_cost = total_days * booking["price"]
                processed_bookings.append({
                    "id": booking["id"],
                    "room_id": booking["room_id"],
                    "user_id": booking["user_id"],
                    "date_from": booking["date_from"].isoformat(),
                    "date_to": booking["date_to"].isoformat(),
                    "price": booking["price"],
                    "image_id": booking["image_id"],
                    "name": booking["name"],
                    "description": booking["description"],
                    "services": booking["services"],
                    "total_cost": total_cost,
                    "total_days": total_days,
                })

            return processed_bookings