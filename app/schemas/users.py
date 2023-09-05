from pydantic import BaseModel, EmailStr, Field


class CreateUsers(BaseModel):

    email: EmailStr
    hashed_password: str = Field(alias='password')


class UsersDB(CreateUsers):

    id: int
    hashed_password: str


