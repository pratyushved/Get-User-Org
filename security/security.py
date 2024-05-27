from datetime import datetime, timezone, timedelta
from typing import Union, List
import jwt
from fastapi.security import OAuth2PasswordBearer
from passlib.context import CryptContext

# to get a string like this run:
# openssl rand -hex 32
SECRET_KEY = "577c4233a81bb765a759a24475f1578dbd83db1e5c34dbf9afeef13e60a0ae74"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")


def create_access_token(data: dict, expires_delta: Union[timedelta, None] = None) -> List:
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.now(timezone.utc) + expires_delta
    else:
        expire = datetime.now(timezone.utc) + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


def verify_password(plain_password, hashed_password) -> bool:
    return pwd_context.verify(plain_password, hashed_password)


def get_password_hash(password):
    return pwd_context.hash(password)
