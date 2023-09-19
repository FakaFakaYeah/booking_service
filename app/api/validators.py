from typing import Optional

from fastapi import HTTPException, status

from app.models import Users, Bookings


def is_author_or_admin(obj: Bookings, user: Users) -> Optional[bool]:
    if not (user.is_superuser or user.id == obj.user_id):
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN)
