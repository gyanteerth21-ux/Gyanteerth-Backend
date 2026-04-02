from passlib.context import CryptContext
from dotenv import load_dotenv
import os
from jose import JWTError

load_dotenv()
SECRET_KEY = os.environ["SECRET_KEY"]
ALGORITHM = os.environ["ALGORITHM"]
ACCESS_TOKEN_EXPIRE_MINUTES = int(os.environ["ACCESS_TOKEN_EXPIRE_MINUTES"])
REFRESH_TOKEN_EXPIRE_DAYS = int(os.environ["REFRESH_TOKEN_EXPIRE_DAYS"])
FORGET_TOKEN_EXPIRE_MINUTES = int(os.environ["FORGET_TOKEN_EXPIRE_MINUTES"])

pwd_context = CryptContext(
    schemes=["bcrypt"],
    deprecated="auto",
    bcrypt__rounds=10
)

def hash_password(password: str) -> str:
    return pwd_context.hash(password)


def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)

from jose import jwt
from datetime import datetime, timedelta



def encode_token(data: dict, token_type: str):

    payload = data.copy()

    expire = datetime.utcnow() +timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)

    payload.update({
        "exp": expire,
        "type": token_type
    })

    token = jwt.encode(payload, SECRET_KEY, algorithm=ALGORITHM)

    return token

def decode_token(token: str):

    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        return payload

    except JWTError:
        return None
    
def create_access_token(user_id: str, role: str):

    expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)

    payload = {
        "user_id": user_id,
        "role": role,
        "type": "access",
        "exp": expire
    }

    access_token = jwt.encode(payload, SECRET_KEY, algorithm=ALGORITHM)

    return access_token

def create_forget_token(user_id: str, role: str):

    expire = datetime.utcnow() + timedelta(minutes=FORGET_TOKEN_EXPIRE_MINUTES)

    payload = {
        "user_id": user_id,
        "type": "forget",
        "exp": expire
    }

    forget_token = jwt.encode(payload, SECRET_KEY, algorithm=ALGORITHM)

    return forget_token


def create_refresh_token(user_id: str):

    expire = datetime.utcnow() + timedelta(days=REFRESH_TOKEN_EXPIRE_DAYS)

    payload = {
        "user_id": user_id,
        "type": "refresh",
        "exp": expire
    }

    refresh_token = jwt.encode(payload, SECRET_KEY, algorithm=ALGORITHM)

    return refresh_token