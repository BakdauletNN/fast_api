from app.database import Base
from sqlalchemy import Column, Integer, String, JSON


class Hotels(Base): # table for hotels database. Parent -> class Base from database.py
    __tablename__ = "hotels"

    id = Column(Integer, primary_key=True)               #define values as a column
    name = Column(String, nullable=False)
    location = Column(String, nullable=False)
    services = Column(JSON)
    rooms_qty = Column(Integer, nullable=False)
    image_id = Column(Integer)