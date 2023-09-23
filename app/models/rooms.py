from typing import Optional

from sqlalchemy import JSON, ForeignKey
from sqlalchemy.orm import relationship, mapped_column, Mapped

from app.core import Base


class Rooms(Base):

    hotel_id: Mapped[int] = mapped_column(ForeignKey('hotels.id'))
    name: Mapped[str]
    description: Mapped[Optional[str]]
    price: Mapped[int]
    services: Mapped[Optional[list[str]]] = mapped_column(JSON)
    quantity: Mapped[int]
    image_id: Mapped[Optional[int]]
    bookings = relationship("Bookings", backref='room')
    hotel = relationship("Hotels", back_populates='rooms', uselist=False)

    def __repr__(self):
        return f'{self.name}'
