from fastapi.params import Body
from pydantic import BaseModel, Field
from random import randrange
from fastapi import status
from fastapi import FastAPI, Response, status, HTTPException, Depends
import psycopg2
from psycopg2.extras import RealDictCursor
from datetime import datetime
from . import models
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

@app.get("/sqlalchemy")
def get_post(db: Session = Depends(get_db)):
    post = db.query(models.Post).all()
    return {"message": post}



@app.post("/posts")
def get_posts():
    # cursor.execute("select * from posts")
    # posts= cursor.fetchall()
    return {"message":posts}




class Post(BaseModel):
    
    name: str
    gender : str
    age : int
    


@app.post("/createpost")
def create_post(post: Post, db: Session = Depends(get_db)):
      new_post=models.Post(name=post.name, age=post.age, gender=post.gender)
      db.add(new_post)
      db.commit()
      db.refresh(new_post)
     
     
    # cursor.execute("insert into posts (title,content,posted_by) values (%s,%s,%s) RETURNING *", (post.title,post.content,post.posted_by))
    # connection.commit()
    # new_post=cursor.fetchone()
      return {"data" : new_post}

def find_post(id: int):
    for post in my_posts:
        if post["id"] == id:
            return post
        


@app.post("/latest_post") 
def get_latest_post():
    post=my_posts[len(my_posts)-1]
    return {"latest_post": post}       
        



@app.post("/post/{id}")
def get_post(id: int):
    cursor.execute("select * from posts where id=%s", (id,))
    post=cursor.fetchone()
    if not post:
        raise HTTPException(status_code=404, detail=f"your post with {id} is not found  ")
    return {"post_detail": post}

def find_index(id):
    for  index, p in enumerate (my_posts):
        if p['id'] == id:
            return index
    return None


@app.delete("/delete/{id}")
def delete_post(id: int):
    cursor.execute("DELETE FROM posts WHERE id = %s RETURNING *", (id,))
    deleted_post=cursor.fetchone()
    connection.commit()
    return {"message" : f"your post with, {id}, is deleted"}




@app.put("/update_post/{id}")

def update_post(id: int, post: Post):
    cursor.execute("update posts  set posted_by = %s where id = %s RETURNING * ",(post.posted_by,id))
    updated_post=cursor.fetchone() 
    connection.commit() 
    return {"message": f"your post with {id} is updated"}  




