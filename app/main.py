from fastapi import FastAPI, status, HTTPException, Response, Depends #type:ignore
from fastapi.params import Body #type: ignore
from pydantic import BaseModel, Field #type: ignore  
#we use this to ensure, the data we got the client should be in our desired format

import psycopg2
from psycopg2.extras import RealDictCursor
from typing import Optional
from random import randrange
import time 
from sqlalchemy.orm import Session
from . import models  # here . refers to current directory
from .database import engine,get_db

models.Base.metadata.create_all(bind=engine) #for table creation based on the classes present in the model 

app = FastAPI()







#So what we want from client for creating the post, we need title, Content 
class Post_(BaseModel):
    title : str = Field(...,min_length=3)
    content: str
    published: Optional[bool] = True  ## or we can just give a default value and it beomes optional i.e, pub : bool=True

my_posts = []

while True: #if our connection to DB is failed, then the starting of server becomes irrelevent, so if connection failed , we don't run our server, beacuse of that we used while loop 
    try:
        conn = psycopg2.connect(host='localhost',database='fastapi_DB',user='postgres',password='IIT@1708', cursor_factory=RealDictCursor)
        cursor = conn.cursor()
        print("DB connection successfull")
        break
    except Exception as error:
        print("Connection to DB failed") 
        print(f'error was {error}')   
        time.sleep(2)


@app.get('/')
async def root():
    return {'message':"Welcome to API"}

@app.get('/posts')
async def get_posts():
    cursor.execute(""" SELECT * from posts""")
    posts = cursor.fetchall()
    
    return {"detail":posts}

@app.get('/posts/{id}')
def get_post(id: int):  # by passing 
    
    # for post in my_posts:
    #     if post['id']==id:
    #         return {"detail":post}

    # raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="ID was not found")

    cursor.execute(""" SELECT * FROM posts WHERE id = %s """,(str(id)))
    post = cursor.fetchone()
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="ID was not found")

     
    return {"post":post}




@app.post("/posts", status_code=status.HTTP_201_CREATED)
async def create_post(post : Post_):  #Validate and extracts all the field from Body of the post request and convert to Post Model and store that dict in newpost
    # Since our my_posts contains array of posts and each post is a dictionary

    # # post_dict = new_post.dict() # Sinc this new_post is Pydantic model, so if we want to convert this to dic than we can do so by using .dict()

    # post_dict['id'] = randrange(1,10000000)
    # my_posts.append(post_dict)


    cursor.execute(""" INSERT INTO posts (title,content,published)  VALUES (%s,%s,%s) RETURNING * """,(post.title,post.content,post.published))
    post = cursor.fetchone()
    conn.commit() # To save the data to DB

    return {"data":post}



@app.delete('/posts/{id}')
async def delete_post(id: int):
    cursor.execute(''' DELETE FROM posts WHERE id = %s RETURNING *''',(str(id),))
    deleted_post = cursor.fetchone()
    conn.commit()

    if deleted_post ==None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail =f'Post with ID {id} in not Found')    
    
    return {"message": "Post Deleted"}


#update Post, it will take ID as path param and the data for Update from the body of the request
@app.put('/posts/{id}')
def update_post(id : int, post : Post_):
    cursor.execute(''' UPDATE posts SET title = %s, content = %s, published = %s where id = %s  returning *''',(post.title,post.content,post.published,str(id)))
    updated_post = cursor.fetchone()
    conn.commit()

    # new_data = new_data.dict()
    # for post in my_posts:
    #     if post['id']==id: 
    #         #since we are sending title and Content for updation
    #         post['title'] = new_data['title']
    #         post['Content'] = new_data['Content']
    #         return {"message":"Post Updated"}
    if updated_post == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f'Post with ID {id} is not Found')     

    return {'Updated Post': updated_post}   

@app.get('/test')
def test(db: Session = Depends(get_db)):
    posts = db.query(models.Post).all()
    return {"posts": posts}




