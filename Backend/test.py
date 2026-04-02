from passlib.context import CryptContext
from dotenv import load_dotenv
import os
from jose import JWTError
from datetime import datetime,timedelta
from jose import jwt

load_dotenv()
SECRET_KEY = os.environ["SECRET_KEY"]
ALGORITHM = os.environ["ALGORITHM"]
ACCESS_TOKEN_EXPIRE_MINUTES = int(os.environ["ACCESS_TOKEN_EXPIRE_MINUTES"])
REFRESH_TOKEN_EXPIRE_DAYS = int(os.environ["REFRESH_TOKEN_EXPIRE_DAYS"])
FORGET_TOKEN_EXPIRE_MINUTES = int(os.environ["FORGET_TOKEN_EXPIRE_MINUTES"])

def create_refresh_token(user_id: str):

    expire = datetime.utcnow() + timedelta(days=REFRESH_TOKEN_EXPIRE_DAYS)

    payload = {
        "user_id": user_id,
        "type": "refresh",
        "exp": expire
    }

    refresh_token = jwt.encode(payload, SECRET_KEY, algorithm=ALGORITHM)

    return refresh_token

print(create_refresh_token("Admin1234"))