from sqlalchemy import Boolean, Column, ForeignKey, Integer, String
from .database import Base




class User(Base):
    __tablename__ = "user"

    id = Column(Integer, primary_key=True)
    name = Column(String)


class users(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True)
    username = Column(String)
    hashed_password = Column(String)

