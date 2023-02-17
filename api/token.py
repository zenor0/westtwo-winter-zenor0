from datetime import timedelta, datetime
import jwt


SECRET_KEY = "sdifhgsiasfjaofhslio" # JWY签名所使用的密钥，是私密的，只在服务端保存
ALGORITHM = "HS256" # 加密算法，我这里使用的是HS256


@app.post("/create_token")
def create_token(username,password):
    if username == "123" and password == "123":
        access_token_expires = timedelta(minutes=60)
        expire = datetime.utcnow() + access_token_expires
 
        payload = {
                    "sub": username,
                    "exp": expire
                     }
        # 生成Token,返回给前端
        access_token = jwt.encode(payload, SECRET_KEY, algorithm=ALGORITHM)
        return {"access_token": access_token, "token_type": "bearer"}
 
    else:
        return False
 
 
def authorized_user(token):
    payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
    username: str = payload.get("sub")
    print(username)
    if username == "123":
        return username

