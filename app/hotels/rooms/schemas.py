from pydantic import BaseModel, Json


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
