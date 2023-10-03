from .base import CRUDBase
from app.models import Rooms

RoomsCrud = CRUDBase(Rooms)
