from fastapi import APIRouter
from ..schemas import ResponseBase

router = APIRouter()

@router.post('/user/login', tags=['user'])
def login():
    return ResponseBase()