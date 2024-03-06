#import libraries

from fastapi import FastAPI
from typing import Union, Optional
from pydantic import BaseModel
from random import randrange

#Create an instance of FastAPI
app = FastAPI()

#Create a Schema to be followed while posting content
class Post(BaseModel):
    title: str
    content: str
    published: bool = True
    rating: Optional[int] =  None


my_posts = [{"title": "title of post 1", "content": "content of post 1", "id": 1}]

@app.get("/")
def get_posts():
    return {"message": "Get Request Successful"}

@app.get("/posts")
def get_posts():
    # return {"data": "These are your posts"}
    return {"data": my_posts}

# find a post using it's id
def find_post(id):
    for p in my_posts:
        if p["id"] == id:
            return p

# retrieve an individual post
# path parameter will always be returned as string
 
@app.get("/posts/{id}")
def get_post(id: int):
    post = find_post(int(id))
    return {"post_details": f"Here is your post  {post}"}

@app.post("/posts")
def create_posts(post: Post):
    post_dict = post.model_dump()
    post_dict['id'] = randrange(0,1000000)
    my_posts.append(post_dict)
    return f"title : {post.title} content: {post.content} published: {post.published} rating: {post.rating}"
