# Database setting
SQLALCHEMY_DATABASE_URL = "mysql+pymysql://root:zenor0@localhost:3306/musictest"

# Mail server setting
MAIL_HOST = "smtp.163.com"  # 设置服务器
MAIL_USER = "zenor0@163.com"  # 用户名
MAIL_PASSWORD = "YXUZDNHZAIYPKNQV"  # 口令
sender = 'zenor0@163.com'

SALT = 'Mu5!c-W3B5ite-7Est.$'

SECRET_KEY = "Mu51CD0WnLO4D_5EcrE7keY!"
ALGORITHM = "HS256"
LOGIN_TOKEN_EXPIRE_MINUTES = 60*24

CAPTCHA_LENGTH = 8
CAPTCHA_EXPIRE_SECONDS = 60