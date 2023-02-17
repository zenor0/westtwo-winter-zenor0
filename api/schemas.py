from pydantic import BaseModel

class UserItem(BaseModel):
    username: str
    password: str
    
    class Config:
        orm_mode = True

class TokenFeedback(BaseModel):
    id: int
    username: str
    token: str


class ResponseBase(BaseModel):
    code: int = 200
    msg: str = 'success'
    data: dict = {}
    
    class Config:
        orm_mode = True
