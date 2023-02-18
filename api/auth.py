from fastapi import Request
from sqlalchemy.orm import Session
from datetime import timedelta, datetime
from . import crud, models, schemas, utils
import jwt

SECRET_KEY = "Mu51CD0WnLO4D_5EcrE7keY!"
ALGORITHM = "HS256"
DEFAULT_EXPIRE_MINUTES = 60*24


def create_token(id, db: Session):
    access_token_expires = timedelta(minutes=DEFAULT_EXPIRE_MINUTES)
    expire = datetime.utcnow() + access_token_expires

    payload = {
        "sub": id,
        "exp": expire
    }

    access_token = jwt.encode(payload, SECRET_KEY, algorithm=ALGORITHM)

    tokenItem = schemas.TokenItem(userid=id,
                                  token=access_token,
                                  hmac_key=SECRET_KEY,
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
    payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
    # username: str = payload.get("sub")

    dbToken = db.query(models.TokenTable).filter(
        models.TokenTable.token == token).first()

    if dbToken == None:
        return None
    else:
        user = db.query(models.UserTable).filter(
            models.UserTable.id == dbToken.userid).first()
        return user.id
