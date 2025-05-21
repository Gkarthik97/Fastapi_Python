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
     name : str
     initial : str
     mobile_no : int = Field(..., ge=1000000000, le=9999999999)
     gender : str
     age : int = Field(..., ge=0, le=120)

class userresponce(BaseModel):
     email : EmailStr
     password : str
     name : str
     initial : str
     mobile_no : int = Field(..., ge=1000000000, le=9999999999)
     gender : str
     age : int = Field(..., ge=0, le=120)
     
