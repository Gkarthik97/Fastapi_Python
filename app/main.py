from fastapi.params import Body
from pydantic import BaseModel, Field
from random import randrange
from typing import Optional, List
from fastapi import status
from passlib.context import CryptContext
from fastapi import FastAPI, Response, status, HTTPException, Depends
import psycopg2
from psycopg2.extras import RealDictCursor
from datetime import datetime
from . import models, schemas, utils
from sqlalchemy.orm import Session
from .database import engine 
models.Base.metadata.create_all(bind=engine)
from .routers import  user, posts









app = FastAPI()






try:
    connection=psycopg2.connect( host='localhost', database='Fastapi', user='postgres',password='postgres', cursor_factory=RealDictCursor)
    cursor=connection.cursor()
    print("DataBase Connection was successful")
except Exception as error:
    print("DataBase connection is unsuccessful")
    print("Error is", error)

app.include_router(posts.router)
app.include_router(user.router)



    
    

   

    




