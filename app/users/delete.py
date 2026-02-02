# from passlib.context import CryptContext
# from jose import jwt
# from datetime import datetime, timedelta
#
#
# pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
#
#
# def create_acces_token(data: dict) -> str:
#     to_encode = data.copy()
#     expire = datetime.utcnow() + timedelta(minutes=30)
#     to_encode.update({"exp": expire})
#     encoded_jwt = jwt.encode(
#         to_encode, "keyforsignature", "HS256"
#     )
#     return encoded_jwt
#
#
# def get_pass_hash(password: str) -> str:
#     return pwd_context.hash(password)
#
#
# def verify_pass(plain_pass, hashed_pass) -> bool:
#     return pwd_context.verify(plain_pass, hashed_pass)
#
#
# test = create_acces_token({"user": "someone"})
# print(test)
