from passlib.context import CryptContext
from pydantic import EmailStr
from app.users.dao import UserDAO
from jose import jwt
from datetime import datetime, timedelta
from app.config import stgs


pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def get_pass_hash(password: str) -> str:
    return pwd_context.hash(password)


def verify_pass(plain_pass, hashed_pass) -> bool:
    return pwd_context.verify(plain_pass, hashed_pass)


def create_acces_token(data: dict) -> str:
    to_encode = data.copy()
    expire = datetime.utcnow() + timedelta(minutes=30)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(
        to_encode, stgs.SECRET_KEY, stgs.HASH_ALGO
    )
    return encoded_jwt


async def check_user(input_email: EmailStr, input_pass: str):
    user = await UserDAO.find_one_or_none(email=input_email)

    if not user:
        return None

    if not verify_pass(plain_pass=input_pass, hashed_pass=user.password):
        return None

    return user


