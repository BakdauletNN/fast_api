from app.service.base import Base
from app.users.models import Users


class UserDAO(Base):
    model = Users

    