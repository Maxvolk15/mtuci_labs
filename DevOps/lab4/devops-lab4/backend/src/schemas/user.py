from typing import List, Optional

from pydantic import BaseModel


class CreateUser(BaseModel):
    name: str
    age: int
    male: bool = True


class UserInfo(BaseModel):
    id: int
    name: str
    age: int
    male: bool


class UpdateUser(BaseModel):
    name: Optional[str] = None
    age: Optional[int] = None
    male: Optional[bool] = None