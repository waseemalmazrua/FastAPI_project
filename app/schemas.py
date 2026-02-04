from pydantic import BaseModel , EmailStr , conint , Field , ConfigDict
from typing import Optional , Union 
from typing_extensions import Annotated
from random import randrange
from datetime import datetime


class PostBase(BaseModel):
    title : str
    content : str
    published : bool = True


class PostCreate(PostBase):
    pass

class userCreate(BaseModel):
    email : EmailStr
    password : str



class UserOut(BaseModel):
    id : int
    email : EmailStr
    created_at : datetime

    model_config = ConfigDict(from_attributes=True)




class UserLogin(BaseModel): 
    email : EmailStr
    password: str


class Post(PostBase):
    id : int
    created_at : datetime
    owner_id : int
    owner : UserOut

 
    model_config = ConfigDict(from_attributes=True)

         

class PostOUT(BaseModel):
    Post:Post
    votes:int

    model_config = ConfigDict(from_attributes=True)




class Token(BaseModel):
        access_token : str
        token_type : str

class TokenData(BaseModel):
    id : int  | None = None



class Vote(BaseModel):
    post_id: int
    dir: Annotated[int, Field(ge=0, le=1)]