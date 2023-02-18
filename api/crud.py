from sqlalchemy.orm import Session
from . import schemas, models, utils
import jwt

def register_user(data: schemas.RegisterItem, db: Session):
    dataDict = data.dict()
    dataDict.pop('checkPassword')
    
    dbItem = models.UserTable(**dataDict)
    dbItem.register_time = utils.Timestamp2FormattedDate()
    
    db.add(dbItem)
    db.commit()
    return True

def get_user_by_name(username, db: Session):
    result = db.query(models.UserTable).filter(models.UserTable.username == username).first()
    return result

def check_pwd_by_name() -> bool:
    pass

def get_history_by_token(token, db: Session):
    result = db.query(models.TokenTable).filter(models.TokenTable.token == token).first()
    user = db.query(models.UserTable).filter(models.UserTable.id == result.userid).one()
    return user.history