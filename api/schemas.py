from pydantic import BaseModel


class TodoItem(BaseModel):
    title: str = 'Untitled'
    content: str = ''
    status: bool = False
    add_time: int | None = None
    end_time: int | None = None
    
    class Config:
        orm_mode = True


class ResponseBase(BaseModel):
    code: int = 200
    msg: str = 'success'
    data: list = []
    
    
    class Config:
        orm_mode = True
