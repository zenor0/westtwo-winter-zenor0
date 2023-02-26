from fastapi import FastAPI, Request

from .routers import users, search, history
from .schemas import ResponseBase
from fastapi.middleware.cors import CORSMiddleware

# FastAPI Configuration
app = FastAPI(title='MusicDownload-simple',
              description='西二冬令营项目. Developed by zenor0. Powered by FastAPI & SQLalchemy')


origins = ["http://localhost:5173/*", '*']
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(users.router)
app.include_router(search.router)
app.include_router(history.router)


# @app.exception_handler(Exception)
# async def func(request: Request, exc: Exception):
#     return ResponseBase(code=222)


@app.get("/")
async def home_page():
    return "Hi! This is music APIs website, please visit /docs or /redocs for more interactive information."
