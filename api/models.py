from typing import Optional
from sqlalchemy import String, TIMESTAMP, INTEGER
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column

from .database import engine


class Base(DeclarativeBase):
    pass


class UserTable(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(
        INTEGER, primary_key=True, autoincrement=True)
    username: Mapped[str] = mapped_column(String(30), nullable=False)
    password: Mapped[str] = mapped_column(String(70), nullable=False)
    email: Mapped[Optional[str]] = mapped_column(String(299))
    register_time: Mapped[str] = mapped_column(TIMESTAMP, nullable=False)

    def __repr__(self) -> dict:
        return {'id': self.id, 'title': self.username, 'pwd': self.password}


class HistoryTable(Base):
    __tablename__ = "history"

    id: Mapped[int] = mapped_column(
        INTEGER, primary_key=True, autoincrement=True)
    download_time: Mapped[str] = mapped_column(TIMESTAMP, nullable=False)

    userid: Mapped[int] = mapped_column(INTEGER)
    rid: Mapped[int] = mapped_column(INTEGER, nullable=False)

    name: Mapped[str] = mapped_column(String(100), nullable=True)
    artist: Mapped[str] = mapped_column(String(100), nullable=True)
    album: Mapped[str] = mapped_column(String(100), nullable=True)
    duration: Mapped[str] = mapped_column(String(100), nullable=True)

    fav: Mapped[int] = mapped_column(INTEGER, default=0)
    deleted: Mapped[int] = mapped_column(INTEGER, default=0)

    def __repr__(self) -> dict:
        return {'download_time': self.download_time, 'userid': self.userid, 'rid': self.rid}


class TokenTable(Base):
    __tablename__ = "token"

    uid: Mapped[int] = mapped_column(
        INTEGER, primary_key=True, autoincrement=True)
    userid: Mapped[int] = mapped_column(INTEGER)
    token: Mapped[str] = mapped_column(String(512))
    hmac_key: Mapped[str] = mapped_column(String(512), nullable=True)
    sign_time: Mapped[str] = mapped_column(TIMESTAMP, nullable=False)
    expire_time: Mapped[str] = mapped_column(TIMESTAMP, nullable=False)

    def __repr__(self) -> dict:
        return {'uid': self.userid, 'token': self.token, 'exp_time': self.expire_time}


class CaptchaTable(Base):
    __tablename__ = "captcha"

    uid: Mapped[int] = mapped_column(
        INTEGER, primary_key=True, autoincrement=True)
    email: Mapped[str] = mapped_column(String(299))
    captcha: Mapped[str] = mapped_column(String(10))
    generate_time: Mapped[str] = mapped_column(TIMESTAMP, nullable=False)
    expire_time: Mapped[str] = mapped_column(TIMESTAMP, nullable=False)

    def __repr__(self) -> dict:
        return {'userid': self.userid, 'captcha': self.captcha, 'exp_time': self.expire_time}


Base.metadata.create_all(engine)
