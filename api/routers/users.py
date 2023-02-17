from fastapi import APIRouter
from ..schemas import ResponseBase
from .. import schemas

import hashlib

router = APIRouter()

def HashSaltPwd(plain):
    SALT = 'Mu5!c-WEB5ite-7Est.$'
    salted = plain + SALT
    ret = hashlib.sha256()
    ret.update(salted.encode())

    return ret.hexdigest()

@router.post('/user/login', tags=['user'])
def login(data: schemas.UserItem):
    cipherPassword = HashSaltPwd(data.password)

    verifyStatus = True
    if not verifyStatus:
        return ResponseBase(code=201, message="用户名或密码错误")
    
    # Give a token back, and store the token into db
    
    
    
    return ResponseBase(code=201, message=cipherPassword, data=schemas.TokenFeedback())

@router.post('/user', tags=['user'])
def register(data: schemas.RegisterItem):
    if data.password != data.checkPassword:
        return ResponseBase(code=201, message='两次输入的密码不一致')

    # Check if username existed
    
    # Hash password
    
    # Store to db