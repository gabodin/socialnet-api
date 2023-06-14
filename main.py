from fastapi import Body, FastAPI
from pydantic import BaseModel

app = FastAPI()


class Post(BaseModel):
    title: str
    content: str


@app.get('/')
async def root():
    return {"message": "Welcome to my API!"}


@app.get('/posts')
def get_posts():
    return {'data': "These are your posts"}


@app.post("/createposts")
def create_posts(new_post: Post):
    print(new_post)
    return {'data': 'new_post'}

# title str, content str, category,
