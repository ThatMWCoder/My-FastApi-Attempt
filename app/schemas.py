from pydantic import BaseModel, EmailStr
from pydantic.types import conint
from sqlalchemy import orm
from datetime import datetime
from typing import Optional

from app.database import Base


class Post(BaseModel):
    title: str
    content: str
    


class PostBase(BaseModel):
    title: str
    content: str


class PostCreate(PostBase):
    pass

class UserResponse(BaseModel):
    id: int
    email: EmailStr
    firstname: str
    lastname: str
    class Config:
        orm_mode = True

class Post(PostBase):
    id: int
    created_at: datetime
    owner_id: int
    owner: UserResponse

    class Config:
        orm_mode = True

class PostWithLike(BaseModel):
    Post: Post
    likes: int

    class Config:
        orm_mode = True

class Like(BaseModel):
    post_id: int
    dir: conint(le=1)


class UserCreate(BaseModel):
    email: EmailStr
    firstname: str
    lastname: str
    password: str
    

class UserLogin(BaseModel):
    email : EmailStr
    password: str

class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    id: Optional[str] = None
