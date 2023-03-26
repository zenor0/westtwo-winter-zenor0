# Database setting
SQLALCHEMY_DATABASE_URL = "mysql+pymysql://root:zenor0@music-db:3306"

# Mail server setting
MAIL_HOST = "smtp.163.com" 
MAIL_USER = "zenor0@163.com"  
MAIL_PASSWORD = "**" 
sender = 'zenor0@163.com'

SALT = 'Mu5!c-W3B5ite-7Est.$'

SECRET_KEY = "Mu51CD0WnLO4D_5EcrE7keY!"
ALGORITHM = "HS256"
LOGIN_TOKEN_EXPIRE_MINUTES = 60*24

CAPTCHA_LENGTH = 8
CAPTCHA_EXPIRE_SECONDS = 60