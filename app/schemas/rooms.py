from pydantic import BaseModel


class RoomDB(BaseModel):
    id: int
    hotel_id: int
    name: str
    description: str
    price: int
    services: list[str]
    quantity: int
    rooms_left: int
    image_id: int


class RoomsPriceDB(RoomDB):

    total_coast: int
