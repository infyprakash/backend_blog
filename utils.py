import os
from passlib.context import CryptContext
from fastapi.security import HTTPBearer
from datetime import datetime, timedelta
from jose import jwt


pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
oauth2_scheme = HTTPBearer()

JWT_SECRET_KEY = "18e0fe2dadf7aedcd03f485ad1cc91d271ed33e7e25847cce3881869318f6e9f"
ALGORITH = "HS256"
TOKEN_EXPIRES_MINUTE = 30


def get_password_hash(password: str):
    return pwd_context.hash(password)


def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)


def create_access_token(data: dict):
    to_encode = data.copy()
    expire = datetime.utcnow() + timedelta(minutes=int(TOKEN_EXPIRES_MINUTE))
    to_encode.update({'exp': expire})
    encoded_token = jwt.encode(to_encode, JWT_SECRET_KEY, algorithm=ALGORITH)
    return encoded_token
