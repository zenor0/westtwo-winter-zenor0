from pydantic import BaseModel
import builtins


class UserItem(BaseModel):
    username: str
    password: str
    remember: bool


class RegisterItem(BaseModel):
    username: str
    password: str
    captcha: str
    email: str
    checkPassword: str


class SongItem(BaseModel):
    name: str
    artist: str
    album: str
    duration: str
    rid: int


class DeleteHistoryRequestItem(BaseModel):
    type: bool
    id: int = 0
    list: builtins.list = []


class MarkRequestItem(BaseModel):
    id: int
    fav: bool


class ResetRequestItem(BaseModel):
    email: str
    captcha: str
    password: str

class TokenItem(BaseModel):
    userid: int
    token: str
    hmac_key: str
    sign_time: str
    expire_time: str


class TokenFeedback(BaseModel):
    id: int
    username: str
    token: str


class ResponseBase(BaseModel):
    code: int = 200
    message: str = 'success'
    data: dict = {}

    class Config:
        orm_mode = True
