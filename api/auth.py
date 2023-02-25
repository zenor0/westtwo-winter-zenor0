from fastapi import Request
from sqlalchemy.orm import Session
from datetime import timedelta, datetime
from . import crud, models, schemas, utils
import jwt

import smtplib
from email.mime.text import MIMEText
from email.header import Header
from . import config


def create_token(id, db: Session):
    access_token_expires = timedelta(minutes=config.LOGIN_TOKEN_EXPIRE_MINUTES)
    expire = datetime.utcnow() + access_token_expires

    payload = {
        "sub": id,
        "exp": expire
    }

    access_token = jwt.encode(payload, config.SECRET_KEY, algorithm=config.ALGORITHM)

    tokenItem = schemas.TokenItem(userid=id,
                                  token=access_token,
                                  hmac_key=config.SECRET_KEY,
                                  sign_time=utils.Timestamp2FormattedDate(
                                      datetime.utcnow().timestamp()),
                                  expire_time=utils.Timestamp2FormattedDate(
                                      expire.timestamp())
                                  )
    dbTokenItem = models.TokenTable(**tokenItem.dict())
    db.add(dbTokenItem)

    return {"access_token": access_token, "token_type": "bearer"}


def authorized_user(request: Request, db: crud.Session):
    token = request.headers.get('Authorization')
    if token == None:
        return None
    
    payload = jwt.decode(token, config.SECRET_KEY, algorithms=[config.ALGORITHM])
    # username: str = payload.get("sub")

    dbToken = db.query(models.TokenTable).filter(
        models.TokenTable.token == token).first()

    if dbToken == None:
        return None
    else:
        user = db.query(models.UserTable).filter(
            models.UserTable.id == dbToken.userid).first()
        return user.id


def send_captcha_email(captcha, recv):
    message = MIMEText(
        f'[音乐下载室] 您的验证码为 {captcha}. 验证码在 15 分钟内有效, 请尽快认证.\n若非本人操作, 请忽略此邮件.', 'plain', 'utf-8')
    message['From'] = Header("zenor0-dev", 'utf-8')
    message['To'] = Header(recv, 'utf-8')
    message['Subject'] = Header('[音乐下载室] 验证请求', 'utf-8')

    smtpObj = smtplib.SMTP()
    smtpObj.connect(config.MAIL_HOST, 25)
    smtpObj.login(config.MAIL_USER, config.MAIL_PASSWORD)
    smtpObj.sendmail(config.sender, recv, message.as_string())
    

def authorize_captcha(captcha, email, db: Session):
    dbCaptcha = crud.get_captcha_by_email(email, db)
    currentTime = utils.time.time()
    
    if currentTime > utils.time.mktime(dbCaptcha.expire_time.timetuple()):
        return False
    
    if captcha != dbCaptcha.captcha:
        return False
    
    return True


def check_email_if_exist(email, db: Session):
    result = db.query(models.UserTable).filter(
    models.UserTable.email == email).first()

    if result == None:
        return False
    else:
        return True