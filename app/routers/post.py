from .. import models,schemas,utils  # here . refers to current directory
from fastapi import FastAPI, status, HTTPException, Response, Depends, APIRouter #type:ignore
from sqlalchemy.orm import Session
from ..database import get_db
from typing import List

router = APIRouter()


@router.get('/posts',response_model=List[schemas.Post])
async def get_posts(db: Session = Depends(get_db)):
    #sql way
    # cursor.execute(""" SELECT * from posts""")
    # posts = cursor.fetchall()

    #through ORM
    posts = db.query(models.Post).all()
    return posts

@router.get('/posts/{id}', response_model=schemas.Post)
def get_post(id: int,db: Session = Depends(get_db)):  # by passing 
    #sql 
    # cursor.execute(""" SELECT * FROM posts WHERE id = %s """,(str(id)))
    # post = cursor.fetchone()
    # if not post:
    #     raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="ID was not found")

    #ORM
    post = db.query(models.Post).filter(models.Post.id == id).first()

     
    return post




@router.post("/posts", status_code=status.HTTP_201_CREATED,response_model=schemas.Post)
async def create_post(post : schemas.PostCreate, db: Session = Depends(get_db)):  #Validate and extracts all the field from Body of the post request and convert to Post Model and store that dict in newpost
    #Sql way
    # cursor.execute(""" INSERT INTO posts (title,content,published)  VALUES (%s,%s,%s) RETURNING * """,(post.title,post.content,post.published))
    # post = cursor.fetchone()
    # conn.commit() # To save the data to DB

    #ORM way
    
    # new_post = models.Post(title = post.title,content=post.content,published=post.published)
    new_post = models.Post(**post.dict()) # this ** did the unpacking of the dictionary
    db.add(new_post) # add this new post to the DB
    db.commit()
    db.refresh(new_post) # it retrieves the newly added post form DB and store it in new_post

    return new_post



@router.delete('/posts/{id}')
async def delete_post(id: int,db: Session = Depends(get_db)):
    #sql
    # cursor.execute(''' DELETE FROM posts WHERE id = %s RETURNING *''',(str(id),))
    # deleted_post = cursor.fetchone()
    # conn.commit()

    #ORMs
    post = db.query(models.Post).filter(models.Post.id==id)

    if post.first() ==None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail =f'Post with ID {id} in not Found')    
    
    post.delete()
    db.commit()
    
    return Response(status_code=status.HTTP_204_NO_CONTENT)


#update Post, it will take ID as path param and the data for Update from the body of the request
@router.put('/posts/{id}',response_model=schemas.Post)
def update_post(id : int, post : schemas.PostCreate,db: Session = Depends(get_db)):
    #sql
    # cursor.execute(''' UPDATE posts SET title = %s, content = %s, published = %s where id = %s  returning *''',(post.title,post.content,post.published,str(id)))
    # updated_post = cursor.fetchone()
    # conn.commit()

    #ORMs
    post_query = db.query(models.Post).filter(models.Post.id==id)
    post_ = post_query.first()
    
    if post_ == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f'Post with ID {id} is not Found')  

    # post_query.update({'title': "my new one",'content': "post.content"},synchronize_session=False)
    post_query.update(post.dict(),synchronize_session=False)  
    db.commit() 

    return post_query.first()   

