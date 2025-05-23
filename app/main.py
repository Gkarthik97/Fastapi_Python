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

from .database import get_db







app = FastAPI()




my_posts = [{"name" :"karthikeyudu", "initial":"Galla", "age" : 27, "id": 1},
            {"name":"vinay", "initial":"konda", "age":26, "id":2}]

try:
    connection=psycopg2.connect( host='localhost', database='Fastapi', user='postgres',password='postgres', cursor_factory=RealDictCursor)
    cursor=connection.cursor()
    print("DataBase Connection was successful")
except Exception as error:
    print("DataBase connection is unsuccessful")
    print("Error is", error)

@app.get("/posts",response_model=List[schemas.responce])
def get_post(db: Session = Depends(get_db)):
    post = db.query(models.Post).all()
    return  post



# @app.post("/posts")
# def get_posts():
#     # cursor.execute("select * from posts")
#     # posts= cursor.fetchall()
#     return {"message":posts}





    


@app.post("/createpost",response_model=schemas.responce)
def create_post(post: schemas.Post, db: Session = Depends(get_db)):
      new_post=models.Post(**post.dict())
      db.add(new_post)
      db.commit()
      db.refresh(new_post)
     
     
    # cursor.execute("insert into posts (title,content,posted_by) values (%s,%s,%s) RETURNING *", (post.title,post.content,post.posted_by))
    # connection.commit()
    # new_post=cursor.fetchone()
      return  new_post

def find_post(id: int):
    for post in my_posts:
        if post["id"] == id:
            return post
        


@app.post("/latest_post") 
def get_latest_post():
    post=my_posts[len(my_posts)-1]
    return {"latest_post": post}       
        



@app.post("/post/{id}")
def get_post(id: int, db: Session = Depends(get_db) ):
   
    post= db.query(models.Post).filter(models.Post.id == id).first()
    # cursor.execute("select * from posts where id=%s", (id,))
    # post=cursor.fetchone()
    if not post:
        raise HTTPException(status_code=404, detail=f"your post with id  {id} is not found  ")
    return {"data": post}

def find_index(id):
    for  index, p in enumerate (my_posts):
        if p['id'] == id:
            return index
    return None


@app.delete("/delete/{id}")
def delete_post(id: int , db: Session = Depends(get_db)):
    post = db.query(models.Post).filter(models.Post.id == id).first()
    if not post:
        raise HTTPException(status_code=404, detail=f"your post with id  {id} is not found  ")
    db.delete(post)
    db.commit()


    # cursor.execute("DELETE FROM posts WHERE id = %s RETURNING *", (id,))
    # deleted_post=cursor.fetchone()
    # connection.commit()
    return {"message" : f"your post with, {id}, is deleted"}




@app.put("/update/{id}")

def update_post(id: int, post_data: schemas.Post ,db: Session = Depends(get_db)):
    query= db.query(models.Post).filter(models.Post.id == id)
    if query == None:
        raise HTTPException(status_code=404, detail=f"your post with id  {id} is not found  ")
    post=query.first()
  
    query.update(post_data.dict())
    db.commit()
    db.refresh(post)



    # cursor.execute("update posts  set posted_by = %s where id = %s RETURNING * ",(post.posted_by,id))
    # updated_post=cursor.fetchone() 
    # connection.commit() 
    return {"message": post}  

@app.post("/user",status_code=status.HTTP_201_CREATED, response_model=schemas.userresponce)
def create_user(User: schemas.user , db: Session = Depends(get_db)):
   hashed_password= utils.passwd_hash(User.password)
   User.password=hashed_password
   new_user=models.User(**User.dict())
   db.add(new_user)
   db.commit()
   db.refresh(new_user)
   return new_user

@app.get("/user/{id}", response_model=schemas.userresponce)
def get_user(id: int, db: Session = Depends(get_db)):
    user = db.query(models.User).filter(models.User.id == id).first()
    if not user:
        raise HTTPException(status_code=404, detail=f"your user with id  {id} is not found  ")
    return user

@app.post("/userupdate/{id}",response_model=schemas.userresponce)
def upadte_user(id: int , User: schemas.userupdate , db: Session = Depends(get_db)):
    query = db.query(models.User).filter(models.User.id == id)
    if not query.first():
        raise HTTPException(status_code=404, detail=f"your user with id  {id} is not found  ")
    
    query.update(User.dict(exclude_unset=True), synchronize_session=False)

    db.commit()
    updated_user=query.first()
    
    
    return updated_user

    
    

   

    




