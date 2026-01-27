from app.database import Base
from sqlalchemy import Column, Integer, String, JSON


class Rooms(Base):
    __tablename__ = "rooms"

    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    hotel_id = Column(Integer)
    description = Column(String)
    price = Column(Integer, nullable=False)
    services = Column(JSON)
    quantity = Column(Integer, nullable=False)
    image_id = Column(Integer)

