from pydantic import BaseModel, Field, PositiveInt


class HotelsDB(BaseModel):

    id: int
    name: str
    location: str
    services: list[str]
    rooms_quantity: int
    image_id: int


class HotelCreate(BaseModel):
    name: str = Field(example='Название отеля')
    location: str = Field(example='Локация отеля')
    services: list[str] = Field(example=['Сервисы отеля'])
    rooms_quantity: PositiveInt = Field(example=10)
    image_id: int = Field(example=1)


class HotelsRoomsLeft(HotelsDB):
    rooms_left: int
