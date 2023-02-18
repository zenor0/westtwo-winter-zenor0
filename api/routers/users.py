from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from ..database import get_db
from .. import auth, schemas, crud, utils, auth
from ..schemas import ResponseBase

router = APIRouter()

@router.post('/user/login', tags=['user'])
def login(data: schemas.UserItem, db: Session = Depends(get_db)):
    
    cipherPassword = utils.HashSaltPwd(data.password)
    user = crud.get_user_by_name(data.username, db)
    
    if user == None or user.password != cipherPassword:
        return ResponseBase(code=201, message="用户名或密码错误")
    
    # Give a token back, and store the token into db
    token = auth.create_token(user.id, db)
    feedback = schemas.TokenFeedback(id=user.id, username=user.username, token=token)
    
    return ResponseBase(data=feedback)

@router.post('/user', tags=['user'])
def register(data: schemas.RegisterItem, db: Session = Depends(get_db)):
    if data.password != data.checkPassword:
        return ResponseBase(code=201, message='两次输入的密码不一致')
    
    result = crud.get_user_by_name(data.username, db)
    if result != None:
        return ResponseBase(code=201, message='用户已存在')
    
    data.password = utils.HashSaltPwd(data.password)
    crud.register_user(data, db)
    
    user = crud.get_user_by_name(username=data.username, db=db)

    return ResponseBase(data={'id': user.id, 'username': user.username})