from app.service.base import Base
from app.hotels.rooms.models import Rooms


class RoomDAO(Base):
    model = Rooms