from fastapi import FastAPI
from app.bookings.router import router as booking_router
from app.users.router import router as router_users
from app.hotels.router import router as hotels_router


my_app = FastAPI()
my_app.include_router(router_users)
my_app.include_router(booking_router)
my_app.include_router(hotels_router)

