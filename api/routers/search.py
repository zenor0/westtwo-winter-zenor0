from fastapi import APIRouter
from ..schemas import ResponseBase

router = APIRouter()

@router.post('/search/login', tags=['search'])
def search():
    return ResponseBase()