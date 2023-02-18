from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from ..database import get_db
from .. import auth, schemas, crud, utils, auth
from ..schemas import ResponseBase

router = APIRouter()

@router.post('/history/login', tags=['history'])
def history():
    return ResponseBase()