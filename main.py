from fastapi import FastAPI
from fastapi.params import Body

app=FastAPI()

@app.get("/")
def root():
    return {"message": "api development"}

@app.get("/posts")
def get_posts():
    return {"message":"this is first post"}


@app.post("/createpost")
def create_post(payload: dict=Body(...)):
    print(payload)
    return {"new_post": f"tile :{payload['title']} content: {payload['content']}"}