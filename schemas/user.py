from pydantic import BaseModel
from typing import Optional


class UserBase(BaseModel):
    username: str
    fname: str
    lname: str
    email: str
    is_active: bool
    is_superuser: bool
    is_verified: bool


class UserCreate(UserBase):
    password: str
    created_at: str
    updated_at: str


class UserUpdate(UserBase):
    updated_at: str


class ChangeUserPassword(BaseModel):
    current_password: str
    new_password: str


class UserLogin(BaseModel):
    username: Optional[str]
    email: Optional[str]
    password: str


class UserShow(UserBase):
    id: str
    created_at: str
    updated_at: str

    class Config:
        from_attributes = True
