from pydantic import BaseModel, Field, EmailStr

from datetime import datetime



class Post(BaseModel):
    
    name: str
    gender : str
    age : int

class responce(BaseModel):
    name: str
    gender: str
    age : int

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
     
