from pydantic import BaseModel, EmailStr
from datetime import datetime
from typing import Optional

class PostBase(BaseModel):
    title: str
    content: str
    published: bool = True


class PostCreate(PostBase):
    pass


class Post(PostCreate):
    id: int
    created_at: datetime
    owner_id: int
    class Config:
        orm_mode = True


class UserCreate(BaseModel):
    email: EmailStr
    password: str


class UserOut(BaseModel):
    id: int
    email: EmailStr
    created_at: datetime
    class Config:
        orm_mode = True


class UserLogin(BaseModel):
    email: EmailStr
    password: str


class LoginOut(BaseModel):
    id: int
    email: EmailStr
    token: str
    created_at: datetime
    class Config:
        orm_mode = True


class Token(BaseModel):
    access_token: str
    token_type: str

class Tokendata(BaseModel):
    id:Optional[str]