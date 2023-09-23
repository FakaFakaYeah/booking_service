from datetime import date

from sqlalchemy import ForeignKey, Computed
from sqlalchemy.orm import Mapped, mapped_column

from app.core import Base


class Bookings(Base):

    room_id: Mapped[int] = mapped_column(ForeignKey("rooms.id"))
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"))
    date_from: Mapped[date]
    date_to: Mapped[date]
    price: Mapped[int]
    total_cost: Mapped[int] = mapped_column(
        Computed("(date_to - date_from) * price")
    )
    total_days: Mapped[int] = mapped_column(Computed("date_to - date_from"))

    def __repr__(self):
        return f'Бронирование #{self.id} c {self.date_from} по {self.date_to}'
