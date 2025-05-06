from fastapi.params import Body
from pydantic import BaseModel
from random import randrange
from fastapi import status
from fastapi import FastAPI, Response, status, HTTPException


app = FastAPI()


my_posts = [{"name" :"karthikeyudu", "initial":"Galla", "age" : 27, "id": 1},
            {"name":"vinay", "initial":"konda", "age":26, "id":2}]

@app.get("/")
def root():
    return {"message": "api development"}

@app.post("/posts")
def get_posts():
    return {"message":my_posts}




class post(BaseModel):
    title : str
    content : str
    rating : int


@app.post("/createpost")
def create_post(post : post):
    post_dict=post.dict()
    post_dict['id']=randrange(1,100)
    my_posts.append(post_dict)
    
    return {"message" : post_dict}

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
    post=find_post(id)
    if not post:

        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                           detail=f"the post with id: {id} not found")
    
    return {"post_detail": post}

def find_index(id):
    for  index, p in enumerate (my_posts):
        if p['id'] == id:
            return index
    return None


@app.delete("/delete/{id}")
def delete_post(id: int):
    index=find_index(id)
    if index is None:
        raise HTTPException(status_code=404, detail=f"your post with id {id} did not found")
    my_posts.pop(index)
    return {"message" : f"your post with id {id} is deleted"}



