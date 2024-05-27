from typing import Union, List

from pydantic import BaseModel




class ItemBase(BaseModel):
    name: str



class ItemCreate(ItemBase):
    pass



class ItemRead(ItemBase):
    id: int



class Token(BaseModel):
    access_token: str
    token_type: str



class TokenData(BaseModel):
    username: Union[str, None] = None




class User(BaseModel):
    username: str


class UserInDB(User):
    hashed_password: str


class Config:
    orm_mode = True
