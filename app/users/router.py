from fastapi import APIRouter, Response, Depends
from app.users.schemas import SUserRegister
from app.users.dao import UserDAO
from app.users.auth import get_pass_hash, verify_pass, check_user, create_acces_token
from app.users.models import Users
from app.users.dependencies import get_cur_admin
from app.exceptions import ExceptionExists, IncorrectLoginOrPassException


router = APIRouter(
    prefix="/auth",
    tags=["Authentication & Users"]
)


@router.post("/register")
async def register_user(user_data: SUserRegister):
    exist_user = await UserDAO.find_one_or_none(email=user_data.email)
    if exist_user:
        raise ExceptionExists
    hashed_password = get_pass_hash(user_data.password)
    await UserDAO.add(email=user_data.email, hashed_password=hashed_password)


@router.post("/login")
async def login_user(response: Response, user_data: SUserRegister):
    user = await check_user(input_email=user_data.email, input_pass=user_data.password)
    if not user:
        return IncorrectLoginOrPassException
    acces_token = create_acces_token({"sub":str(user.id)})
    response.set_cookie(key="booking_access_token", value=acces_token, httponly=True)
    return {"acces_token":acces_token}


@router.post("/logout")
async def logout_user(response: Response):
    response.delete_cookie("booking_access_token")


@router.get("/all")
async def read_users(cur_user: Users = Depends(get_cur_admin)):
    return await UserDAO.find_all()
