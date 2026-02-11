from fastapi import FastAPI
from sqladmin import Admin
from app.database import engine
from app.admin.views import UserAdmin, BookingsAdmin, RoomsAdmin, HotelsAdmin
from fastapi.middleware.cors import CORSMiddleware
from app.bookings.router import router as booking_router
from app.users.router import router as router_users
from app.hotels.router import router as hotels_router
from app.hotels.rooms.router import router as room_router
from app.pages.router import router as pages_router
from fastapi.staticfiles import StaticFiles
from app.images.router import router as image_router
from fastapi_cache import FastAPICache
from fastapi_cache.backends.redis import RedisBackend
from redis import asyncio as aioredis
from collections.abc import AsyncIterator
from contextlib import asynccontextmanager
from app.admin.auth import authentication_backend


@asynccontextmanager
async def lifespan(_: FastAPI) -> AsyncIterator[None]:
    redis = aioredis.from_url("redis://localhost:6379")
    FastAPICache.init(RedisBackend(redis), prefix="fastapi-cache")
    yield


app = FastAPI(lifespan=lifespan)

admin = Admin(app, engine, authentication_backend=authentication_backend)
admin.add_view(UserAdmin)
admin.add_view(BookingsAdmin)
admin.add_view(HotelsAdmin)
admin.add_view(RoomsAdmin)


app.mount("/static", StaticFiles(directory="app/static"), "static")

app.include_router(router_users)
app.include_router(booking_router)
app.include_router(hotels_router)
app.include_router(room_router)
app.include_router(pages_router)
app.include_router(image_router)


#https://fastapi.tiangolo.com/tutorial/cors/#use-corsmiddleware
origins = [
    "http://localhost.tiangolo.com",
    "https://localhost.tiangolo.com",
    "http://localhost",
    "http://localhost:8080",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

