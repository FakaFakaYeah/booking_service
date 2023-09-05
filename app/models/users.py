from sqlalchemy.orm import relationship, Mapped, mapped_column

from app.core import Base


class Users(Base):

    email: Mapped[str] = mapped_column(unique=True)
    hashed_password: Mapped[str]
    bookings = relationship("Bookings", collection_class=list)
