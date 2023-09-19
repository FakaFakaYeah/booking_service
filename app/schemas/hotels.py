from typing import Optional

from pydantic import BaseModel


class HotelsDB(BaseModel):

    id: int
    name: str
    location: str
    services: list[str]
    rooms_quantity: int
    image_id: int
    rooms_left: Optional[int] = None
