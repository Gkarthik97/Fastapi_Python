
from .. import models, schemas, database, utils
from app.routers import Oauth2
from  app.database import engine, get_db
import psycopg2
from psycopg2.extras import RealDictCursor
from sqlalchemy.orm import Session
from fastapi import FastAPI, Response, status, HTTPException, Depends, APIRouter
from typing import Optional, List
from fastapi import status



router=APIRouter(
    prefix="/posts",
    tags=['posts']
)

try:
    connection=psycopg2.connect( host='localhost', database='Fastapi', user='postgres',password='postgres', cursor_factory=RealDictCursor)
    cursor=connection.cursor()
    print("DataBase Connection was successful")
except Exception as error:
    print("DataBase connection is unsuccessful")
    print("Error is", error)

@router.get("/",response_model=List[schemas.responce])
def get_post(db: Session = Depends(get_db),current_user: int = Depends(Oauth2.get_current_user)):
    post = db.query(models.Post).filter(models.Post.owner_id ==current_user.id ).all()
    return  post



# @app.post("/posts")
# def get_posts():
#     # cursor.execute("select * from posts")
#     # posts= cursor.fetchall()
#     return {"message":posts}





    


@router.post("/create",response_model=schemas.responce)
def create_post(post: schemas.Post, db: Session = Depends(get_db), current_user: int = Depends(Oauth2.get_current_user)):
      new_post=models.Post(owner_id=current_user.id,**post.dict())
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
        


@router.post("/latest_post") 
def get_latest_post():
    post=my_posts[len(my_posts)-1]
    return {"latest_post": post}       
        



@router.post("/{id}")
def get_post(id: int, db: Session = Depends(get_db), current_user: int = Depends(Oauth2.get_current_user) ):
   
    post= db.query(models.Post).filter(models.Post.id == id).first()
    # cursor.execute("select * from posts where id=%s", (id,))
    # post=cursor.fetchone()
    if not post:
        raise HTTPException(status_code=404, detail=f"your post with id  {id} is not found")
    if post.owner_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail=f"you are not authorized to perform this action")

    return {"data": post}

def find_index(id):
    for  index, p in enumerate (my_posts):
        if p['id'] == id:
            return index
    return None


@router.delete("/delete/{id}")
def delete_post(id: int , db: Session = Depends(get_db), current_user: int = Depends(Oauth2.get_current_user)):
    post = db.query(models.Post).filter(models.Post.id == id).first()
    if not post:
        raise HTTPException(status_code=404, detail=f"your post with id  {id} is not found ")
    if post.owner_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail=f"you are not authorized to perform this action")
    db.delete(post)
    db.commit()


    # cursor.execute("DELETE FROM posts WHERE id = %s RETURNING *", (id,))
    # deleted_post=cursor.fetchone()
    # connection.commit()
    return {"message" : f"your post with, {id}, is deleted"}




@router.put("/update/{id}")

def update_post(id: int, post_data: schemas.Post ,db: Session = Depends(get_db), current_user: int = Depends(Oauth2.get_current_user)):
    query= db.query(models.Post).filter(models.Post.id == id)
    if query == None:
        raise HTTPException(status_code=404, detail=f"your post with id  {id} is not found  ")
    
    post=query.first()
    if post.owner_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail=f"you are not authorized to perform this action")
  
    query.update(post_data.dict())
    db.commit()
    db.refresh(post)