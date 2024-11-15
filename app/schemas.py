from pydantic import BaseModel


class UserRegister(BaseModel):
    username: str
    email: str
    phone: str
    password: str


class LoginUser(BaseModel):
    username: str
    password: str


class CreatePost(BaseModel):
    title: str
    content: str


class Post(BaseModel):
    id: int
    title: str
    content: str
    owner_id: int

    class Config:
        orm_mode: True
