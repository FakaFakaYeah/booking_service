from pydantic import BaseModel, EmailStr, Field, Extra


class UserBase(BaseModel):

    email: EmailStr


class UsersAuth(UserBase):

    email: EmailStr
    hashed_password: str = Field(
        alias='password', min_length=6,
        max_length=16, pattern=r'^[a-zA-Zа-яА-Я0-9]+$'
    )

    class Config:

        extra = Extra.forbid


class UsersDB(UserBase):

    id: int
