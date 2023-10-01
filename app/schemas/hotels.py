from typing import Optional

from pydantic import BaseModel, PositiveInt, Extra


class HotelsDB(BaseModel):

    id: int
    name: str
    location: str
    services: list[str]
    rooms_quantity: int
    image_id: int


class HotelCreate(BaseModel):
    name: str
    location: str
    services: list[str]
    rooms_quantity: PositiveInt
    image_id: int

    class Config:
        extra = Extra.forbid
        json_schema_extra = {
            'example': {
                'name': 'Название отеля',
                'location': 'Локация отеля',
                'services': ['Сервисы отеля'],
                'rooms_quantity': 10,
                'image_id': 1
            }
        }


class HotelUpdate(HotelCreate):
    name: Optional[str] = None
    location: Optional[str] = None
    services: Optional[list[str]] = None
    rooms_quantity: Optional[PositiveInt] = None
    image_id: Optional[int] = None


class HotelsRoomsLeft(HotelsDB):
    rooms_left: int
