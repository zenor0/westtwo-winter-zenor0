from pydantic import BaseModel

class UserItem(BaseModel):
    username: str
    password: str
    remember: bool

class RegisterItem(BaseModel):
    username: str
    password: str
    checkPassword: str
    
class HistoryRequestItem(BaseModel):
    type: bool
    id: int
    list: list

class MarkRequestItem(BaseModel):
    id: int
    fav: bool


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
