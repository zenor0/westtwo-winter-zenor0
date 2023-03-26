from sqlalchemy import create_engine, text
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from . import config

engine = create_engine(config.SQLALCHEMY_DATABASE_URL, echo=True)
init = engine.connect()
init.execute(text("CREATE DATABASE IF NOT EXISTS music_down_site"))
init.execute(text("USE music_down_site"))
engine = create_engine(config.SQLALCHEMY_DATABASE_URL+"/music_down_site", echo=True)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.commit()
        db.close()
