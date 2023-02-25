from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
import re
import random
import string

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

    captcha = crud.get_captcha_by_email(data.email, db)
    if captcha == None:
        return ResponseBase(code=201, message='未知错误')
    if data.captcha != captcha:
        return ResponseBase(code=201, message='验证码错误')
    
    crud.register_user(data, db)
    user = crud.get_user_by_name(username=data.username, db=db)

    return ResponseBase(data={'id': user.id, 'username': user.username})


@router.put('/user', tags=['user'])
async def reset_password(data: schemas.ResetRequestItem, db: Session = Depends(get_db)):

    if crud.get_user_by_email(data.email, db) == None:
        return ResponseBase(code=201, message='用户不存在')

    # verify captcha (can be non-existed)
    captcha = crud.get_captcha_by_email(data.email, db)
    if captcha == None:
        return ResponseBase(code=201, message='未知错误')
    if data.captcha != captcha:
        return ResponseBase(code=201, message='验证码错误')

    crud.update_user_password_by_email(
        data.email, utils.HashSaltPwd(data.password), db)

    return ResponseBase(code=200, message='重置成功')
    pass

@router.post('/user/captcha/', tags=['user'])
async def res():
    return ResponseBase(code= 201, message='请输入邮箱')
@router.post('/user/captcha/{email}', tags=['user'])
async def request_captcha(email, db: Session = Depends(get_db)):
    if not check_email(email):
        return ResponseBase(code=201, message='邮箱地址不合法')
    return ResponseBase(code=200, message=f'已向 {email} 发送验证码, 请及时查收.')

    # TO-DO
    # check if already sent and not expired
    if crud.get_captcha_by_email(email, db) != None:
        return ResponseBase(code=202, message='验证码已发送或冷却时间未到')

    # generate captcha then send to corresponding email
    captcha = ''.join(random.sample(string.ascii_letters + string.digits, 8))
    crud.save_captcha(email, captcha, db)

    auth.send_captcha_email(captcha, email)

    return ResponseBase(code=200, message=f'已向 {email} 发送验证码, 请及时查收.')
