from fastapi import FastAPI
from fastapi.params import Body
from pydantic import BaseModel



app=FastAPI()

@app.get("/")
def root():
    return {"message": "api development"}

@app.get("/posts")
def get_posts():
    return {"message":"this is first post"}

class post(BaseModel):
    title : str
    content : str
    rating : int


@app.post("/createpost")
def create_post(new_post : post):
    print(new_post.dict())
    return {"message" : new_post}