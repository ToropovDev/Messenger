from typing import Optional

from fastapi_users import schemas


class UserRead(schemas.BaseUser[int]):
    username: str
    id: int
    phone_number: str
    email: str
    role_id: int
    is_active: bool = True
    is_superuser: bool = False


class UserCreate(schemas.BaseUserCreate):
    username: str
    phone_number: str
    email: str
    password: str
    role_id: int
    is_active: Optional[bool] = True
    is_superuser: Optional[bool] = False


class UserUpdate(schemas.BaseUserUpdate):
    username: str
    phone_number: str
    email: str
    password: str
    role_id: int
    is_active: Optional[bool] = True
    is_superuser: Optional[bool] = False
