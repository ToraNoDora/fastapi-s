from typing import Optional

from pydantic import BaseModel, constr, EmailStr


class UserBase(BaseModel):
    first_name: Optional[constr(min_length=2, max_length=50)] = None
    last_name: Optional[constr(min_length=2, max_length=50)] = None
    email: Optional[EmailStr] = None


class UserCreate(UserBase):
    password: str


class UserUpdate(UserBase):
    password: Optional[str] = None


class UserUpdateRestricted(BaseModel):
    id: int


class DisplayUser(BaseModel):
    id: int
    first_name: str
    last_name: str
    email: str

    class Config:
        orm_mode = True


class UserStoreBase(UserBase):
    id: Optional[int] = None

    class Config:
        orm_mode = True


class UserStore(UserStoreBase):
    pass


