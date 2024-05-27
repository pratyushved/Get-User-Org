from sqlalchemy.orm import Session

from models import models, schemas


def get_user(db: Session):
    return db.query(models.User).all()


def create_user(db: Session, user: schemas.ItemBase):
    db.add(user)
    db.commit()
    db.refresh(user)
    return user


def get_userbyusername(db: Session, username: str):
    return db.query(models.users).filter(models.users.username == username).first()
