from pydantic import BaseModel, EmailStr


class UserCreate(BaseModel):
    name: str
    email: EmailStr        # EmailStr -- avtomatik "bu haqiqatan email formatimi" tekshiradi
    username: str
    password: str


class UserLogin(BaseModel):
    username: str
    password: str


class ChannelCreate(BaseModel):
    channel_username: str   # masalan "@mening_kanalim"


class PostCreate(BaseModel):
    text: str
    channel_id: int