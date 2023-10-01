import pytest

from app.crud import UsersCrud
from app.api.exceptions import ObjNotFound
from tests.constants import NOT_FOUND_ID


async def test_user_get_by_id(session, user_db_1):

    user = await UsersCrud.get_by_id(session=session, obj_id=user_db_1.id)
    assert user.id == user_db_1.id
    assert user.email == user_db_1.email


async def test_user_get_by_id_with_not_found_id(session):

    with pytest.raises(ObjNotFound) as exception:
        await UsersCrud.get_by_id(session=session, obj_id=NOT_FOUND_ID)
    assert exception.value.detail == "Объект не найден"

