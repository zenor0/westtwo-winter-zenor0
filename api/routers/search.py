from fastapi import APIRouter, Depends, Request
from fastapi.responses import FileResponse
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
        new = schemas.SongItem(name=item['name'].replace('&nbsp;', ' '),
                                artist=item['artist'].replace('&nbsp;', ' '),
                                album=item['album'].replace('&nbsp;', ' '),
                                duration=item['songTimeMinutes'].replace('&nbsp;', ' '),
                                rid=item['rid']).dict()
        ret.append(new)
        
    return ret

def get_song_info(rid):
    SEARCH_URL = f'http://www.kuwo.cn/api/www/music/musicInfo?mid={rid}'
    HEADER = {
        'Cookie': 'kw_token=KUWO',
        'Referer': f'http://www.kuwo.cn/play_detail/{rid}',
        'csrf': 'KUWO'
    }
    
    responseJson = requests.get(SEARCH_URL, headers=HEADER).json()
    ret = schemas.SongItem(name=responseJson['data']['name'].replace('&nbsp;', ' '),
                           artist=responseJson['data']['artist'].replace('&nbsp;', ' '),
                           album=responseJson['data']['album'].replace('&nbsp;', ' '),
                           duration=responseJson['data']['songTimeMinutes'].replace('&nbsp;', ' '),
                           rid=responseJson['data']['rid']
                           )
    return ret


router = APIRouter()


@router.get('/search', tags=['search'])
def search(text: str):
    ret = {'list': search_query(text)}
    return ResponseBase(data=ret)


@router.get('/search/download/{rid}', tags=['search'])
def download(rid, request: Request, db: Session = Depends(get_db)):
    userid = auth.authorized_user(request=request, db=db)
    if not userid:
        return ResponseBase(code=201, message='Token expired')
    
    downTmp = requests.get(f'https://link.hhtjim.com/kw/{rid}.mp3')
    with open(f'./tmp/music/{rid}.mp3', 'wb') as file:
        file.write(downTmp.content)
    
    crud.create_history(get_song_info(rid), userid, db)
    return FileResponse(f'./tmp/music/{rid}.mp3', media_type='audio/mpeg')
