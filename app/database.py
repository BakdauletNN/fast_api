from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import DeclarativeBase, sessionmaker
from app.config import stgs


DATABASE_URL = stgs.DB_URL


engine = create_async_engine(DATABASE_URL)
session_maker = sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)

class Base(DeclarativeBase): #class for migration
    pass

