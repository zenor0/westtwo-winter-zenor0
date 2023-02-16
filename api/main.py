from fastapi import FastAPI, Depends
from sqlalchemy.orm import Session

from . import schemas, utils
from .database import SessionLocal, engine

import time
app = FastAPI(title='Todo-simple', description='西二冬令营项目. Developed by zenor0. Powered by FastAPI & SQLalchemy')

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.commit()
        db.close()
        
@app.get("/")
async def home_page():
    return "Hi! This is a To-Do APIs website, please visit /docs or /redocs for more interactive information."

