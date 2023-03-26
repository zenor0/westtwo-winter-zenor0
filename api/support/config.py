import os
env_dist = os.environ

# Database setting
SQLALCHEMY_DATABASE_URL = "mysql+pymysql://root:zenor0@music-db:3306"

# Mail server setting

MAIL_HOST = env_dist.get("MAIL_HOST")
MAIL_USER = env_dist.get("MAIL_USER")
MAIL_PASSWORD = env_dist.get("MAIL_PASSWORD")
sender = MAIL_USER

SALT = 'Mu5!c-W3B5ite-7Est.$'

SECRET_KEY = "Mu51CD0WnLO4D_5EcrE7keY!"
ALGORITHM = "HS256"
LOGIN_TOKEN_EXPIRE_MINUTES = 60*24

CAPTCHA_LENGTH = 8
CAPTCHA_EXPIRE_SECONDS = 60