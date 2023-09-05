from typing import Optional

from sqlalchemy import JSON
from sqlalchemy.orm import relationship, Mapped, mapped_column

from app.core import Base


class Hotels(Base):

    name: Mapped[str]
    location: Mapped[str]
    services: Mapped[Optional[list[str]]] = mapped_column(JSON)
    rooms_quantity: Mapped[int]
    image_id: Mapped[Optional[int]]
    rooms = relationship("Rooms", collection_class=list)
