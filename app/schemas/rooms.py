from pydantic import BaseModel


class RoomsPriceDB(BaseModel):

    id: int
    hotel_id: int
    name: str
    description: str
    price: int
    services: list[str]
    quantity: int
    rooms_left: int
    image_id: int
    total_coast: int
