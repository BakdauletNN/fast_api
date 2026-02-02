from fastapi import HTTPException, status


class BookingException(HTTPException):
    status_code = 500 #default
    detail = ''

    def __init__(self):
        super().__init__(status_code=self.status_code, detail=self.detail)


class ExceptionExists(BookingException):
    status_code = status.HTTP_409_CONFLICT
    detail = "User already exists"


class IncorrectLoginOrPassException(BookingException):
    status_code = status.HTTP_401_UNAUTHORIZED
    detail = "Incorrect email or password. Please try again."


class ExpiredTokenException(BookingException):
    status_code = status.HTTP_401_UNAUTHORIZED
    detail = "Token expired"


class NotTokenException(BookingException):
    status_code = status.HTTP_401_UNAUTHORIZED
    detail = "Token not found"


class IncorrectFormatTokenException(BookingException):
    status_code = status.HTTP_401_UNAUTHORIZED
    detail = "Inccorect format token"


class UserNotPresentException(BookingException):
    status_code = status.HTTP_401_UNAUTHORIZED

class RoomCannorBeCooked(BookingException):
    status_code = status.HTTP_409_CONFLICT
    detail = "There is no available rooms"

