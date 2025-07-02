from pydantic import BaseModel, Field, EmailStr
from pydantic import conint

from datetime import datetime
from typing import Optional



class user(BaseModel):
     email : EmailStr
     password : str



class Post(BaseModel):
    
    name: str
    content : str
    
    

class responce(BaseModel):
    name: str
    content : str
    owner_id : int
    owner : user

class Config:
        orm_mode = True



class user(BaseModel):
     email : EmailStr
     password : str
     
     

class userresponce(BaseModel):
     email : EmailStr
     

class userupdate(BaseModel):
     name: str= None
     email: str = None
     age: int= None

class UserLogin(BaseModel):
     email : EmailStr
     password: str     
     
class TokenData(BaseModel):
     
     id: Optional[int] = None

class Vote(BaseModel):
     post_id: int 
     dir: conint(le=1)