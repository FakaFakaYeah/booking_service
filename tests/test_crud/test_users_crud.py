import pytest

from app.crud import UsersCrud
from app.api.exceptions import ObjNotFound


async def test_user_get_by_id(session, user_db_1):

    user = await UsersCrud.get_by_id(session=session, obj_id=user_db_1.id)
    assert user.id == user_db_1.id
    assert user.email == user_db_1.email


async def test_user_get_by_id_with_not_found_id(session):

    with pytest.raises(ObjNotFound) as exception:
        await UsersCrud.get_by_id(session=session, obj_id=9999)
    assert exception.value.detail == "Объект не найден"


async def test(room_db):
    print(room_db.id)