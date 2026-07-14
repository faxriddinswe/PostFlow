from dotenv import load_dotenv
load_dotenv()

import bcrypt

def hash_password(password: str) -> str:
    """
    Xom parolni bcrypt hash'iga aylantiradi.
    bcrypt.gensalt() -- har safar tasodifiy "salt" (tuz) yaratadi,
    shu tufayli bir xil parol har safar BOSHQA hash beradi (xavfsizlik uchun muhim).
    """
    password_bytes = password.encode("utf-8")          # bcrypt matn emas, bayt (bytes) kutadi
    hashed = bcrypt.hashpw(password_bytes, bcrypt.gensalt())
    return hashed.decode("utf-8")                       # database'da matn sifatida saqlash uchun qaytadan decode qilamiz


def verify_password(plain_password: str, hashed_password: str) -> bool:
    """Login vaqtida: user kiritgan parol bilan database'dagi hash mos keladimi tekshiradi."""
    return bcrypt.checkpw(
        plain_password.encode("utf-8"),
        hashed_password.encode("utf-8"),
    )


import os
from datetime import datetime, timedelta, timezone
from jose import jwt, JWTError

SECRET_KEY = os.getenv("SECRET_KEY")
ALGORITHM = "HS256"                    # imzolash algoritmi -- standart tanlov
ACCESS_TOKEN_EXPIRE_MINUTES = 60 * 24  # token 24 soat amal qiladi


def create_access_token(data: dict) -> str:
    """
    Payload'ni (masalan {"sub": "faxriddin"}) qabul qiladi,
    unga tugash vaqtini (expiry) qo'shadi, keyin SECRET_KEY bilan imzolaydi.
    """
    to_encode = data.copy()
    expire = datetime.now(timezone.utc) + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})   # "exp" -- JWT standartida "tugash vaqti" degani
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


def decode_access_token(token: str) -> dict | None:
    """
    Token'ni ochadi va tekshiradi: imzo to'g'rimi, muddati o'tmaganmi?
    Xato bo'lsa None qaytaradi.
    """
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        return payload
    except JWTError:
        return None
    

from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from sqlalchemy.orm import Session

from database import get_db
from models import User

# OAuth2PasswordBearer -- FastAPI'ga "token 'Authorization: Bearer <token>' header'ida keladi" deb aytadi
# tokenUrl -- shunchaki Swagger UI'da "Authorize" tugmasi qayerga so'rov yuborishini bildiradi
bearer_scheme = HTTPBearer()


def get_current_user(
    credentials: HTTPAuthorizationCredentials = Depends(bearer_scheme),
    db: Session = Depends(get_db),
) -> User:
    token = credentials.credentials
    """
    Bu funksiya har bir HIMOYALANGAN endpoint'da ishlatiladi.
    1. Header'dan tokenni oladi (FastAPI buni avtomatik qiladi, OAuth2PasswordBearer tufayli)
    2. Tokenni ochadi (decode_access_token)
    3. Token ichidagi user_id bo'yicha database'dan userni topadi
    4. Topilmasa yoki token yaroqsiz bo'lsa -- 401 xato qaytaradi
    """
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Token yaroqsiz yoki muddati o'tgan",
        headers={"WWW-Authenticate": "Bearer"},
    )

    payload = decode_access_token(token)
    if payload is None:
        raise credentials_exception

    user_id = payload.get("user_id")
    if user_id is None:
        raise credentials_exception

    user = db.query(User).filter(User.id == user_id).first()
    if user is None:
        raise credentials_exception

    return user