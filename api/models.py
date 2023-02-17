from typing import Optional, List
from sqlalchemy import String, create_engine, TIMESTAMP, BOOLEAN, INTEGER, ForeignKey
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship


class Base(DeclarativeBase):
    pass

class UserTable(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(INTEGER, primary_key=True, autoincrement=True)
    username: Mapped[str] = mapped_column(String(30))
    password: Mapped[str] = mapped_column(String(256))
    email: Mapped[Optional[str]] = mapped_column(String(299))
    register_time: Mapped[str] = mapped_column(TIMESTAMP)
    
    history: Mapped[List["HistoryTable"]] = relationship()

    def __repr__(self) -> dict:
        return {'id': self.id, 'title': self.username, 'pwd': self.password}
    
class HistoryTable(Base):
    __tablename__ = "history"

    uid: Mapped[int] = mapped_column(INTEGER, primary_key=True, autoincrement=True)
    download_time: Mapped[str] = mapped_column(TIMESTAMP)
    userid: Mapped[int] = mapped_column(ForeignKey("UserTable.id"))
    rid: Mapped[int] = mapped_column(INTEGER)
    favorite: Mapped[bool] = mapped_column(BOOLEAN)
    deleted: Mapped[bool] = mapped_column(BOOLEAN)
    
    
    def __repr__(self) -> dict:
        return {'download_time': self.download_time, 'userid': self.userid, 'rid': self.rid}
    
    
class TokenTable(Base):
    __tablename__ = "token"

    uid: Mapped[int] = mapped_column(INTEGER, primary_key=True, autoincrement=True)
    userid: Mapped[int] = mapped_column(INTEGER)
    token: Mapped[str] = mapped_column(String(512))
    sign_time: Mapped[str] = mapped_column(TIMESTAMP)
    expire_time: Mapped[str] = mapped_column(TIMESTAMP)
    
    def __repr__(self) -> dict:
        return {'uid': self.userid, 'token': self.token, 'exp_time': self.expire_time}
    
    