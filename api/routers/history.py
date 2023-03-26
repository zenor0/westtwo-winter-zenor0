from fastapi import APIRouter, Depends, Request
from sqlalchemy.orm import Session

from support.database import get_db
from support import auth, schemas, crud, utils, auth
from support.schemas import ResponseBase
import math

router = APIRouter()
PAGE_ITEMS_COUNT = 10


def calculate_offset(page):
    if page <= 0:
        return (0, PAGE_ITEMS_COUNT)
    skip = (page - 1) * PAGE_ITEMS_COUNT
    return (skip, PAGE_ITEMS_COUNT)


@router.get('/user/history', tags=['history'])
async def get_history(page: int, request: Request, db: Session = Depends(get_db)):
    if not auth.authorized_user(request=request, db=db):
        return ResponseBase(code=201, message='Token expired')
    
    skip, limit = calculate_offset(page)
    token = request.headers.get('Authorization')
    result = crud.get_history_by_token(token, db, skip, limit)
    count = crud.get_history_total_by_token(token=token, db=db)
    
    return ResponseBase(data={'list': result, 'count': math.ceil(count / PAGE_ITEMS_COUNT)})


@router.put('/user/history/lc', tags=['history'])
async def modify(data: schemas.MarkRequestItem, request: Request, db: Session = Depends(get_db)):
    if not auth.authorized_user(request=request, db=db):
        return ResponseBase(code=201, message='Token expired')

    crud.mark_history(data.id, data.fav, db)
    return ResponseBase()


@router.delete('/user/history', tags=['history'])
async def delete(data: schemas.DeleteHistoryRequestItem, request: Request, db: Session = Depends(get_db)):
    if not auth.authorized_user(request=request, db=db):
        return ResponseBase(code=201, message='Token expired')

    if data.type == 0:
        crud.softdelete_single_history(data.id, db)
    elif data.type == 1:
        crud.softdelete_list_of_history(data.list, db)

    return ResponseBase()
