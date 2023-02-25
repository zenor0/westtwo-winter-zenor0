from sqlalchemy.orm import Session
from . import schemas, models, utils
import jwt


def register_user(data: schemas.RegisterItem, db: Session):
    dataDict = data.dict()
    dataDict.pop('checkPassword')
    dataDict.pop('captcha')

    # TO-DO
    # deal with the captcha

    dbItem = models.UserTable(**dataDict)
    dbItem.register_time = utils.Timestamp2FormattedDate()

    db.add(dbItem)
    db.commit()
    return True


def update_user_password_by_email(email, newPassword, db: Session):
    user = get_user_by_email(email, db)
    user.password = newPassword
    return


def get_user_by_name(username, db: Session):
    result = db.query(models.UserTable).filter(
        models.UserTable.username == username).first()
    return result


def get_user_by_email(email, db: Session):
    result = db.query(models.UserTable).filter(
        models.UserTable.email == email).first()
    return result


def get_captcha_by_email(email, db: Session):
    currentTime = utils.time.time()
    result = db.query(models.CaptchaTable).filter(
        models.CaptchaTable.email == email).first()

    if result == None:
        return None
    if utils.FormattedDate2Timestamp(result.expire_time) < currentTime:
        return None

    return result.captcha


def save_captcha(email, captcha, db: Session):
    user = get_user_by_email(email, db)
    if user == None:
        return False

    dbItem = models.CaptchaTable(
        email=email, captcha=captcha, userid=user.id)
    dbItem.generate_time = utils.Timestamp2FormattedDate()
    dbItem.expire_time = utils.Timestamp2FormattedDate(utils.time.time() + 3600)
    
    db.add(dbItem)
    return True


def get_history_by_token(token, db: Session, skip: int = 0, limit: int = 100):
    dbToken = db.query(models.TokenTable).filter(
        models.TokenTable.token == token).first()
    user = db.query(models.UserTable).filter(
        models.UserTable.id == dbToken.userid).one()

    result = db.query(models.HistoryTable).filter(
        models.HistoryTable.userid == user.id, models.HistoryTable.deleted == 0).offset(skip).limit(limit)

    return result.all()


def get_history_total_by_token(token, db: Session):
    dbToken = db.query(models.TokenTable).filter(
        models.TokenTable.token == token).first()
    user = db.query(models.UserTable).filter(
        models.UserTable.id == dbToken.userid).one()

    result = db.query(models.HistoryTable).filter(
        models.HistoryTable.userid == user.id, models.HistoryTable.deleted == 0)

    return result.count()


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
