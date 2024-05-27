from sqlalchemy.orm import Session
import models
from repository.crud import create_user, get_user, get_userbyusername
from security.security import verify_password


def get_user_service(db: Session):
    return get_user(db)


def create_user_service(db: Session, user: str):
    org = models.User(name=user)
    return create_user(db, org)


def get_user_(db: Session, username: str):
    user = get_userbyusername(db, username)
    if user:
        return user
    return None


def authenticate_user(db: Session, username: str, password: str):
    user = get_userbyusername(db, username)
    if not user:
        return False
    if not verify_password(password, user.hashed_password):
        return False
    return user
