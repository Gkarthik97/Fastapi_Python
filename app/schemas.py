from pydantic import BaseModel, Field, EmailStr

from datetime import datetime
from typing import Optional



class Post(BaseModel):
    
    name: str
    content : str
    

class responce(BaseModel):
    name: str
    content : str
    created_time : datetime
    owner_id : int

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
