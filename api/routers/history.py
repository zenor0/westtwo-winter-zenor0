from fastapi import APIRouter
from ..schemas import ResponseBase

router = APIRouter()

@router.post('/history/login', tags=['history'])
def history():
    return ResponseBase()