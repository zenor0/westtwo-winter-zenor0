from sqlalchemy.orm import Session
from datetime import timedelta, datetime
from . import crud, models, schemas, utils
import jwt

SECRET_KEY = "Mu51CD0WnLO4D_5EcrE7keY!" 
ALGORITHM = "HS256"
DEFAULT_SIGN_PERIOD = 60*24

def create_token(id, db: Session):
    access_token_expires = timedelta(minutes=DEFAULT_SIGN_PERIOD)
    expire = datetime.utcnow() + access_token_expires

    payload = {
                "sub": id,
                "exp": expire
                    }
    
    access_token = jwt.encode(payload, SECRET_KEY, algorithm=ALGORITHM)
    
    tokenItem = schemas.TokenItem(userid=id, 
                                  token=access_token, 
                                  hmac_key=SECRET_KEY, 
                                  sign_time=utils.Timestamp2FormattedDate(datetime.utcnow().timestamp()),
                                  expire_time=utils.Timestamp2FormattedDate(expire.timestamp())
                                  )
    dbTokenItem = models.TokenTable(**tokenItem.dict())
    db.add(dbTokenItem)
    
    return access_token


def authorized_user(token, db: crud.Session):
    payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
    username: str = payload.get("sub")
    
    user = db.query(models.TokenTable).filter(models.TokenTable.token == token).one()
    
    return user.userid


