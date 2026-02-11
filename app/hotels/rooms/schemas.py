from pydantic import BaseModel, Json, Field
from typing import List, Optional


class SRooms(BaseModel):
    id: int
    name: str
    hotel_id: int
    description: str
    price: int
    services: Json
    quantity: int
    image_id: int

    class Config:
        from_attributes = True


class SRoomsList(BaseModel):
    id: int
    hotel_id: int
    name: str
    description: Optional[str] = None
    services: List[str] = Field(default_factory=list)
    price: int
    quantity: int
    image_id: int
    rooms_left: Optional[int] = None
    total_cost: Optional[int] = None

    class Config:
        from_attributes = True
