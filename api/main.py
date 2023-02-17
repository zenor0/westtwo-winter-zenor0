from fastapi import FastAPI, Depends
from sqlalchemy.orm import Session

from . import schemas, utils
from .database import SessionLocal, engine
from .routers import users, search, history
from fastapi.middleware.cors import CORSMiddleware

# FastAPI Configuration
app = FastAPI(title='MusicDownload-simple', description='西二冬令营项目. Developed by zenor0. Powered by FastAPI & SQLalchemy')

app.include_router(users.router)
app.include_router(search.router)
app.include_router(history.router)

origins = ["http://localhost:5173","*"]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.commit()
        db.close()
        



@app.get("/")
async def home_page():
    return "Hi! This is music APIs website, please visit /docs or /redocs for more interactive information."

@app.post('/user/login')
def log():
    return {
	"code": 200,
	"message": "success",
	"data": {
		"id": 1,
		"username": "admin",
		"token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiJ0ZXN0IiwiZXhwIjoxNjczNDQ4NTcyfQ.UVcR7CULoyQ101mZ5B1FmaXb9fpZ-2k4hX_ueW4Qe2I"
	}
}