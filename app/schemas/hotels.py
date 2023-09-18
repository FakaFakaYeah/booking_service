from pydantic import BaseModel


class HotelsLocationDB(BaseModel):

    id: int
    name: str
    location: str
    services: list[str]
    rooms_quantity: int
    image_id: int
    rooms_left: int
