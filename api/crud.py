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
    result = db.query(models.UserTable).filter(
        models.UserTable.username == username).first()
    return result


def get_history_by_token(token, db: Session, skip: int = 0, limit: int = 100):
    dbToken = db.query(models.TokenTable).filter(
        models.TokenTable.token == token).first()
    user = db.query(models.UserTable).filter(
        models.UserTable.id == dbToken.userid).one()

    ret = db.query(models.HistoryTable).filter(
        models.HistoryTable.userid == user.id, models.HistoryTable.deleted == 0).offset(skip).limit(limit).all()
    return ret

def create_history(data: schemas.SongItem, userid, db: Session):
    dbItem = models.HistoryTable(**data.dict())
    dbItem.userid = userid
    dbItem.download_time = utils.Timestamp2FormattedDate()
    
    db.add(dbItem)
    return

def mark_history(id, fav, db: Session):
    return db.query(models.HistoryTable).filter(models.HistoryTable.id == id).update({models.HistoryTable.fav: fav})


def softdelete_single_history(id, db: Session):
    return db.query(models.HistoryTable).filter(models.HistoryTable.id == id).update({models.HistoryTable.deleted: 1})


def softdelete_list_of_history(list, db: Session):
    cnt = 0
    for item in list:
        softdelete_single_history(item, db)
        cnt += 1

    return cnt
