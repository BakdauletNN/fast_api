from app.database import session_maker
from sqlalchemy import select, insert, delete, and_


class Base:
    model = None

    @classmethod
    async def find_by_id(cls, model_id: int):
        async with session_maker() as session:
            query = select(cls.model).filter_by(id=model_id)
            res = await session.execute(query)
            return res.scalar_one_or_none()

    @classmethod
    async def find_one_or_none(cls, **filter_by):
        async with session_maker() as session:
            query = select(cls.model).filter_by(**filter_by)
            res = await session.execute(query)
            return res.scalar_one_or_none()

    @classmethod
    async def find_all(cls, **filter_by):
        async with session_maker() as session:
            query = select(cls.model).filter_by(**filter_by)
            bookings = await session.execute(query)
            return bookings.scalars().all()

    @classmethod
    async def add(cls, **data):
        async with session_maker() as session:
            query = insert(cls.model).values(**data)
            await session.execute(query)
            await session.commit()

    @classmethod
    async def delete(cls, id_model: int, user_id: int):
        async with session_maker() as session:
            # delete booking only current user
            query = (
                delete(cls.model)
                .where(
                    and_(
                        cls.model.id == id_model,
                        cls.model.user_id == user_id  # check user
                    )
                )
                .returning(cls.model.id)  # returning id deleted model
            )

            result = await session.execute(query)
            await session.commit()

            # checking that record deleted
            deleted_id = result.scalar()
            return deleted_id is not None

