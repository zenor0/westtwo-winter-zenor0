from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from support import config

from support.database import get_db
from support import auth, schemas, crud, utils, auth
from support.schemas import ResponseBase

router = APIRouter()

# init admin account

def init(db: Session = Depends(get_db)):
    if crud.get_user_by_name('admin', db) == None:
        user = schemas.RegisterItem(
            username='admin',
            password=utils.HashSaltPwd('123456'),
            captcha='init',
            email='zenor0@outlook.com',
            checkPassword='fill',
        )
        crud.register_user(user, db)

# init()

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

    if len(data.password) < 6 or len(data.password) > 18:
        return ResponseBase(code=201, message='密码长度不合法')

    result = crud.get_user_by_name(data.username, db)
    if result != None:
        return ResponseBase(code=201, message='用户已存在')

    data.password = utils.HashSaltPwd(data.password)
    
    if not auth.authorize_captcha(data.captcha, data.email, db):
        return ResponseBase(code=201, message='验证码错误或过期')


    crud.register_user(data, db)
    crud.delete_verified_captcha(data.email, data.captcha, db)
    user = crud.get_user_by_name(username=data.username, db=db)

    return ResponseBase(data={'id': user.id, 'username': user.username})


@router.put('/user', tags=['user'])
async def reset_password(data: schemas.ResetRequestItem, db: Session = Depends(get_db)):
    if crud.get_user_by_email(data.email, db) == None:
        return ResponseBase(code=201, message='用户不存在')

    # verify captcha (can be non-existed)
    if not auth.authorize_captcha(data.captcha, data.email, db):
        return ResponseBase(code=201, message='验证码错误或过期')

    crud.reset_password_by_email(
        data.email, utils.HashSaltPwd(data.password), db)

    crud.delete_verified_captcha(data.email, data.captcha, db)
    return ResponseBase(code=200, message='重置成功')


@router.get('/user/captcha/{email}', tags=['user'])
async def request_captcha(email, method, db: Session = Depends(get_db)):
    if method not in ['register', 'reset']:
        return ResponseBase(code=201, message='非法调用')
    if not utils.CheckEmail(email) or not email:
        return ResponseBase(code=201, message='邮箱地址不合法')
    if method == 'reset':
        if crud.get_user_by_email(email, db) == None:
            return ResponseBase(code=201, message='该邮箱未注册')
    if method == 'register':
        if crud.get_user_by_email(email, db):
            return ResponseBase(code=201, message='该邮箱已注册')
        
    # check if already sent and not expired
    dbCaptcha = crud.get_captcha_by_email(email=email, db=db)
    if dbCaptcha != None:
        if utils.time.time() < utils.time.mktime(dbCaptcha.expire_time.timetuple()):
            return ResponseBase(code=202, message='验证码已发送且冷却时间未到')

    # generate captcha then send to corresponding email
    captcha = utils.GenerateCaptcha(config.CAPTCHA_LENGTH)
    print(captcha)

    crud.save_captcha(email, captcha, db)
    auth.send_captcha_email(captcha, email)

    return ResponseBase(code=200, message=f'已向 {email} 发送验证码, 请及时查收.')
