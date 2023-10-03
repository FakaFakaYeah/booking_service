from typing import Optional

from pydantic import BaseModel, Extra, PositiveInt


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


class RoomsCreate(BaseModel):

    hotel_id: PositiveInt
    name: str
    description: str
    price: PositiveInt
    services: list[str]
    quantity: PositiveInt
    image_id: PositiveInt

    class Config:
        extra = Extra.forbid
        json_schema_extra = {
            'example': {
                'hotel_id': 1,
                'name': 'Название номера',
                'description': 'Описание номера',
                'price': 1000,
                'services': ['Сервисы номера'],
                'quantity': 10,
                'image_id': 1
            }
        }