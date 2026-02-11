from pydantic import BaseModel, Json, Field
from typing import List, Optional


class SHotel(BaseModel):
    id: int
    name: str
    location: str
    services: Json
    rooms_qty: int
    image_id: int

    class Config:
        from_attributes = True


class SHotelList(BaseModel):
    id: int
    name: str
    location: str
    services: List[str] = Field(default_factory=list)
    rooms_qty: int
    image_id: int
    rooms_left: Optional[int] = None

    class Config:
        from_attributes = True