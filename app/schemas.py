from pydantic import BaseModel, Field
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