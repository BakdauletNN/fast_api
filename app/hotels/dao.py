from app.service.base import Base
from app.hotels.models import Hotels


class HotelDAO(Base):
    model = Hotels
