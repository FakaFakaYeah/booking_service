from pydantic import BaseModel


class RoomDB(BaseModel):
    id: int
    hotel_id: int
    name: str
    description: str
    price: int
    services: list[str]
    quantity: int
    image_id: int


class RoomsPriceDB(RoomDB):

    rooms_left: int
    total_coast: int
