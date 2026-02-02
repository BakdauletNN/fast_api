from fastapi import Request, Depends, status
from jose import jwt, JWTError
from app.config import stgs
from datetime import datetime
from app.users.dao import UserDAO
from app.users.models import Users
from app.exceptions import ExceptionExists, IncorrectLoginOrPassException, \
   ExpiredTokenException, NotTokenException, IncorrectFormatTokenException,\
    UserNotPresentException



def get_token(request: Request):
    token = request.cookies.get("booking_access_token")
    if not token:
        raise NotTokenException
    return token


async def get_cur_user(user_tkn: str = Depends(get_token)):
    try:
        payload = jwt.decode(user_tkn, stgs.SECRET_KEY, stgs.HASH_ALGO)
    except JWTError:
        raise IncorrectFormatTokenException
    expire: str = payload.get('exp')
    if (not expire) or (int(expire) < datetime.utcnow().timestamp()):
        raise ExpiredTokenException

    user_id: str = payload.get("sub")
    if not user_id:
        raise UserNotPresentException
    user = await UserDAO.find_by_id(int(user_id))
    if not user:
        raise UserNotPresentException
    return user


async def get_cur_admin(current_user: Users = Depends(get_cur_user)):
    # if current_user.role != "admin":
    #     raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED)
    return current_user







