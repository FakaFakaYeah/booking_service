from pydantic import BaseModel, EmailStr, Field, Extra


class UsersAuth(BaseModel):

    email: EmailStr
    hashed_password: str = Field(
        alias='password', min_length=6,
        max_length=16, pattern=r'^[a-zA-Zа-яА-Я0-9]+$'
    )

    class Config:

        extra = Extra.forbid


class UsersDB(UsersAuth):

    id: int
    hashed_password: str
