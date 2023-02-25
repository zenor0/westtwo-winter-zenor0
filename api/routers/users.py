from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
import re

from ..database import get_db
from .. import auth, schemas, crud, utils, auth
from ..schemas import ResponseBase


def check_email(email):
    res = re.search(
        '^[a-zA-Z0-9_.-]+@[a-zA-Z0-9-]+(\\.[a-zA-Z0-9-]+)*\.[a-zA-Z0-9]{2,6}$', email)
    if res:
        return True
    else:
        return False


router = APIRouter()


@router.post('/user/login', tags=['user'])
async def login(data: schemas.UserItem, db: Session = Depends(get_db)):
    cipherPassword = utils.HashSaltPwd(data.password)
    user = crud.get_user_by_name(data.username, db)

    if user == None or user.password != cipherPassword:
        return ResponseBase(code=201, message="用户名或密码错误")

    # Give a token back, and store the token into db
    token = auth.create_token(user.id, db)['access_token']
    feedback = schemas.TokenFeedback(
        id=user.id, username=user.username, token=token)

    return ResponseBase(data=feedback)


@router.post('/user', tags=['user'])
async def register(data: schemas.RegisterItem, db: Session = Depends(get_db)):
    if data.password != data.checkPassword:
        return ResponseBase(code=201, message='两次输入的密码不一致')

    if len(data.password) < 8 or len(data.password) > 18:
        return ResponseBase(code=201, message='密码长度不合法')

    result = crud.get_user_by_name(data.username, db)
    if result != None:
        return ResponseBase(code=201, message='用户已存在')

    data.password = utils.HashSaltPwd(data.password)
    crud.register_user(data, db)

    user = crud.get_user_by_name(username=data.username, db=db)

    return ResponseBase(data={'id': user.id, 'username': user.username})


@router.put('/user', tags=['user'])
async def reset_password(data: schemas.ResetRequestItem, db: Session = Depends(get_db)):
    # verify captcha (can be non-existed)
    # check if user exist
    
    
    return ResponseBase(code=201, message='test interface')
    pass


@router.post('/user/captcha/{email}', tags=['user'])
async def request_captcha(email, db: Session = Depends(get_db)):
    if not check_email(email):
        return ResponseBase(code=201, message='邮箱地址不合法')

    # TO-DO
    # check if email exist in the database
    # check if already sent and not expired

    # generate captcha then send to corresponding email
    
    
    return ResponseBase(code=200, message=f'已向 {email} 发送验证码, 请及时查收.')
