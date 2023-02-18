from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

import requests, urllib.parse
from ..database import get_db
from .. import auth, schemas, crud, utils, auth
from ..schemas import ResponseBase


def search_query(keyword, page=1, limit=10):
    keyword = urllib.parse.quote(keyword)
    SEARCH_URL = f'http://www.kuwo.cn/api/www/search/searchMusicBykeyWord?key={keyword}&pn={page}&rn={limit}'
    HEADER = {
        'Cookie': 'kw_token=KUWO',
        'Referer': f'http://www.kuwo.cn/search/list?key={keyword}',
        'csrf': 'KUWO'
    }

    ret = []
    responseJson = requests.get(SEARCH_URL, headers=HEADER).json()
    for item in responseJson['data']['list']:
        new = schemas.SongItem(name=item['name'],
                                artist=item['artist'],
                                album=item['album'],
                                duration=item['songTimeMinutes'],
                                rid=item['rid']).dict()
        ret.append(new)
        
    # print(ret)
    return ret


router = APIRouter()


@router.get('/search', tags=['search'])
def search(text: str):
    ret = {'list': search_query(text)}
    return ResponseBase(data=ret)


@router.get('/search/download/{rid}', tags=['search'])
def download(rid):

    return ResponseBase()
