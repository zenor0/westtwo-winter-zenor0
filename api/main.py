from fastapi import FastAPI, Depends
from sqlalchemy.orm import Session

from . import schemas, utils, crud
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

# Create
@app.post("/todo", summary='创建新的 Todo')
def create_todo(item: schemas.TodoItem, db: Session = Depends(get_db)):
    '''    
        该接口以 `application/json` 传入参数. 下面是传入的示例:

        ```json
        {
        "title": "Untitled", // Todo 的标题, 长度限制为256. 
        "content": "",	// Todo 的详细内容, 长度限制为1024.
        "status": false,	// 布尔类型, Todo 的完成状态.
        "add_time": 0,	// 整型. Unix 时间戳, Todo 的开始时间. 若留空将被设置为当前服务器时间.
        "end_time": 0		// 整型, Unix 时间戳, Todo 的截止时间. 若留空将被设置为当前服务器时间 + 1s.
        }
        ```

        除时间戳外, 其余参数留空将被设置为示例中的缺省值.



        | 参数     | 类型         | 缺省值              | 注释                             |
        | -------- | ------------ | ------------------- | -------------------------------- |
        | title    | 字符串(256)  | "Untitled"          | Todo 的标题, 长度限制为256.      |
        | content  | 字符串(1024) | ""                  | Todo 的详细内容, 长度限制为1024. |
        | status   | 布尔类型     | False               | Todo 的完成状态.                 |
        | add_time | 整型         | 当前服务器时间      | Unix 时间戳, Todo 的开始时间.    |
        | end_time | 整型         | 当前服务器时间 + 1s | Unix 时间戳, Todo 的截止时间.    |

        若 Todo 合法, 则创建成功后将会返回此前输入的 JSON 信息以及该条 Todo 的 UID.

        如:

        ```json
        {
        "code": 200,
        "msg": "Created!",
        "data": [
            {
            "title": "Untitled",
            "content": "",
            "status": false,
            "add_time": 0,
            "end_time": 0,
            "id": 1
            }
        ]
        }
        ```

       
    '''    
    if item.add_time == None:
        item.add_time = int(time.time())
    if item.end_time == None:
        item.end_time = item.add_time + 1
        
    if item.end_time < item.add_time:
        return schemas.ResponseBase(msg='Illegal input. End time exceeds add time.')
    
    return_id = crud.create_todo(db, item)
    data = [item.dict()]
    data[0].update(id = return_id)
    return schemas.ResponseBase(msg='Created!', data=data)

# Read
@app.get("/todo", summary='获取 Todo')
def query(status: str = '%%', kw: str = '', skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    '''
        | 参数   | 类型           | 缺省值             | 注释                                  |
        | ------ | -------------- | ------------------ | ------------------------------------- |
        | status | 字符串         | 匹配所有状态       | 限定 Todo 的状态. (checked/unchecked) |
        | kw     | 字符串         | 匹配所有内容       | 限定 Todo 的标题和内容中出现的关键字  |
        | skip   | 整型           | 0                  | 返回列表的起始偏移量                  |
        | limit  | 整型           | 100                | 返回列表 Todo 的总数限制              |
        | db     | 数据库 Session | 默认数据库 Session | 要查询的数据库 session.               |

        接口将返回所有符合匹配条件的 Todo 列表. 
    '''
    result = crud.get_todos(db, status, kw, skip, limit)
    
    return schemas.ResponseBase(data=result)

@app.get("/todo/{id}", summary='获取指定 Todo')
def query_by_id(id: int, db: Session = Depends(get_db)):
    '''
        | 参数 | 类型           | 缺省值             | 注释                    |
        | ---- | -------------- | ------------------ | ----------------------- |
        | id   | 整型           | **必填**           | 需要查询的 Todo ID      |
        | db   | 数据库 Session | 默认数据库 Session | 要查询的数据库 session. |

        接口将返回 ID 为请求值的 Todo 内容.
    '''
    result = crud.get_todo_by_id(db, id)
    return schemas.ResponseBase(data=result)

# Update
@app.put("/todo", summary='批量更新 Todo 状态')
def update_all(method: bool, db: Session = Depends(get_db)):
    '''
        | 参数   | 类型           | 缺省值             | 注释                                       |
        | ------ | -------------- | ------------------ | ------------------------------------------ |
        | method | 布尔类型       | **必填**           | 目标状态 (True=checked, False = unchecked) |
        | db     | 数据库 Session | 默认数据库 Session | 要查询的数据库 session.                    |

        数据库中的所有 Todo 将被更新为目标状态.

        该接口将返回被修改的 Todo 的总数
    '''
    cnt = crud.update_all(db, method)
    return schemas.ResponseBase(msg=f"Change [{utils.Boolean2String(not method)}] to [{utils.Boolean2String(method)}]. {cnt} todo in total.")


@app.put("/todo/{id}", summary='更新指定 Todo 状态')
def update_by_id(id: int, method: bool, db: Session = Depends(get_db)):
    '''
        | 参数   | 类型           | 缺省值             | 注释                                       |
        | ------ | -------------- | ------------------ | ------------------------------------------ |
        | id     | 整型           | **必填**           | Todo 的合法 ID                             |
        | method | 布尔类型       | **必填**           | 目标状态 (True=checked, False = unchecked) |
        | db     | 数据库 Session | 默认数据库 Session | 要查询的数据库 session.                    |

        将指定 ID 的 Todo 状态更新为指定的状态
    '''
    cnt = crud.update_by_id(db, id, method)
    if cnt:
        return schemas.ResponseBase(msg=f'ID {id} has [{utils.Boolean2String(method)}]', data=[crud.get_todo_by_id(db, id)])
    else:
        return schemas.ResponseBase(msg=f"Expected ID {id} doesn't exist!")

# Delete
@app.delete("/todo", summary='批量删除 Todo')
def delete(status: str | None = None, db: Session = Depends(get_db)):
    '''
        | 参数   | 类型           | 缺省值             | 注释                             |
        | ------ | -------------- | ------------------ | -------------------------------- |
        | status | 字符串         | 所有状态           | 指定要删除的状态. 若空则删除全部 |
        | db     | 数据库 Session | 默认数据库 Session | 要查询的数据库 session.          |

        指定需要删除的 Todo 的状态. 

        接口将返回被删除的 Todo 的数量.
    '''
    if status == None:
        result = crud.delete_all(db)
    else:
        result = crud.delete_by_status(db, status)
        
    return schemas.ResponseBase(msg = f'{result} todo have been deleted')

@app.delete("/todo/{id}", summary='删除指定 Todo')
def delete_by_id(id: int, db: Session = Depends(get_db)):
    '''
        | 参数 | 类型           | 缺省值             | 注释                    |
        | ---- | -------------- | ------------------ | ----------------------- |
        | id   | 整型           | **必填**           | 要删除的 Todo 的 ID     |
        | db   | 数据库 Session | 默认数据库 Session | 要查询的数据库 session. |

        若 ID 合法, 接口将返回被删除的 Todo 的信息. 
    '''
    result = crud.delete_by_id(db, id)
    if result:
        return schemas.ResponseBase(msg=f"ID {id} Todo has been deleted", data=result)
    else:
        return schemas.ResponseBase(msg=f"Expected ID {id} doesn't exist!", data=result)
