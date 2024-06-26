from random import randrange
from typing import Optional

from fastapi import Body, FastAPI, HTTPException, Response, status
from pydantic import BaseModel

app = FastAPI()


class Post(BaseModel):
    title: str
    content: str
    publish: bool = True
    rating: Optional[int] = None


my_posts = [{"title": "title1", "content": "content1", "id": 1},
            {"title": "title2", "content": "content2", "id": 2}]


def find_post(id):
    for post in my_posts:
        if post['id'] == id:
            return post
        

def find_index_post(id): 
    for index, item in enumerate(my_posts):
        if item["id"] == id:
            return index


@app.get('/')
async def root():
    return {"message": "Welcome to my socialNet-api!"}


@app.get('/posts')
def get_posts():
    return {'data': my_posts}


@app.get("/posts/latest")
def get_latest_post():
    post = my_posts[len(my_posts) - 1]
    return {'details': post}


@app.get("/posts/{id}")
def get_post(id: int, response: Response):
    post = find_post(id)

    if not post:
        # response.status_code = status.HTTP_404_NOT_FOUND
        # return {'message': f"Post #{id} was not found"}
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"Post #{id} was not found")
    return {"post_details": post}


@app.post("/posts", status_code=status.HTTP_201_CREATED)
def create_posts(post: Post):
    post_dict = post.dict()
    post_dict['id'] = randrange(0, 1000000)

    my_posts.append(post_dict)
    return {'data': post_dict}


@app.delete("/posts/{id}")
def delete_post(id: int):
    post_index = find_index_post(id)

    if not post_index:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"post #{id} was not found")
    my_posts.pop(post_index)

    return Response(status_code=status.HTTP_204_NO_CONTENT)


@app.put("/posts/{id}")
def update_post(id: int, post: Post):
    post_index = find_index_post(id)

    if post_index is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"post #{id} was not found")
    
    post_dict = post.dict()
    post_dict["id"] = id
    my_posts[post_index] = post_dict

    return {"data": post_dict}


# title str, content str, category,
