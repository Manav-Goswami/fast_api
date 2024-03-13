#import libraries

from fastapi import FastAPI, Response, status, HTTPException
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

def find_post_index(id):
    for i, p in enumerate(my_posts):
        if p['id'] == id:
            return i

# retrieve an individual post
# path parameter will always be returned as string
 
# not an optimized approach to raise an exception 
# @app.get("/posts/{id}")
# def get_post(id: int, response: Response):
#     post = find_post(int(id))
#     if not post:
#         response.status_code = status.HTTP_404_NOT_FOUND
#         return {"message": f"post id: {id} not found"}
#     return {"post_details": f"Here is your post  {post}"}
        
@app.get("/posts/{id}")
def get_post(id: int):
    post = find_post(int(id))
    if not post:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND
            , detail= f"post id: {id} not found"
        )
    return {"post_details": f"Here is your post  {post}"}

@app.post("/posts", status_code=status.HTTP_201_CREATED)
def create_posts(post: Post):
    post_dict = post.model_dump()
    post_dict['id'] = randrange(0,1000000)
    my_posts.append(post_dict)
    return f"title : {post.title} content: {post.content} published: {post.published} rating: {post.rating}"


@app.delete("/posts/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id: int):
    #deleting the post
    #since we are not using any database right now.
    #Let's just find the index and delete that post
    index = find_post_index(id)
    if index == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND
                            , detail=f"post {id} does not exist")
    #In fast API, we do not return any content while deleting a post
    #Let's just return response.
    my_posts.pop(index)
    return Response(status_code=status.HTTP_204_NO_CONTENT)
