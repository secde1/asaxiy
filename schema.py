from enum import Enum
from pydantic import BaseModel, EmailStr


class UserSchema(BaseModel):
    email: EmailStr
    username: str
    password: str

    # class Config:
    #     orm_mode = True


class Roles(Enum):
    user = "user"
    admin = "admin"