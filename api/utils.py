import time, hashlib
from . import config

def Timestamp2FormattedDate(timestamp: str | None = None) -> str:
    if timestamp == None:
        timestamp = time.time()
    
    timeArray = time.localtime(timestamp + 1)
    otherStyleTime = time.strftime("%Y-%m-%d %H:%M:%S", timeArray)
    return otherStyleTime

def FormattedDate2Timestamp(str):
    timeArray = time.strptime(str, "%Y-%m-%d %H:%M:%S")
    timestamp = time.mktime(timeArray)
    return timestamp

def String2Boolean(input):
    if input in [True, 'true', 'True', 'checked']:
        return True
    if input in [False, 'false', 'False', 'unchecked']:
        return False

def Boolean2String(val: bool):
    if val:
        return 'checked'
    else:
        return 'unchecked'
    
def HashSaltPwd(plain):
	salted = plain + config.SALT
	ret = hashlib.sha256()
	ret.update(salted.encode())

	return ret.hexdigest()