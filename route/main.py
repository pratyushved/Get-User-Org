from datetime import timedelta
import jwt
import uvicorn
from fastapi import Depends, FastAPI, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from jwt import InvalidTokenError
from sqlalchemy.orm import Session
from database import engine, get_db
from models import models
from models.models import users
from models.schemas import ItemCreate, Token, TokenData
from security.security import ACCESS_TOKEN_EXPIRE_MINUTES, create_access_token, oauth2_scheme, ALGORITHM, \
    SECRET_KEY
from service.service import create_user_service, get_user_service, authenticate_user, get_user_


app = FastAPI()

models.Base.metadata.create_all(bind=engine)


def get_current_user(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            raise credentials_exception
        token_data = TokenData(username=username)
    except InvalidTokenError:
        raise credentials_exception
    user = get_user_(db, username)
    if user is None:
        raise credentials_exception
    return user


# Dependency
@app.post("/token")
def login_for_access_token(
        form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)
) -> Token:
    user = authenticate_user(db, form_data.username, form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user.username}, expires_delta=access_token_expires
    )
    return Token(access_token=access_token, token_type="bearer")


@app.post("/user/")
def create_user(comp: ItemCreate, db: Session = Depends(get_db), current_user: users = Depends(get_current_user)):
    return create_user_service(db, comp.name)


@app.get("/users/")
def read_user(db: Session = Depends(get_db), current_user: users = Depends(get_current_user)):
    return get_user_service(db)


if __name__ == '__main__':
    uvicorn.run(app)
