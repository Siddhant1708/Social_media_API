from .. import models,schemas,utils  # here . refers to current directory
from fastapi import FastAPI, status, HTTPException, Response, Depends, APIRouter #type:ignore
from sqlalchemy.orm import Session
from ..database import get_db
from .. import oauth2,schemas, models  
from typing import List,Optional

router = APIRouter(
    prefix="/vote",
    tags=['Vote']
)

@router.post('/',status_code=status.HTTP_201_CREATED)
def vote(vote_ : schemas.Vote,db : Session = Depends(get_db),current_user: int = Depends(oauth2.get_current_user)):


    post = db.query(models.Post).filter(models.Post.id == vote_.post_id).first()
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Post with id {vote_.post_id} not found")

    #but first check weather the post is already liked by the same user
    vote_query = db.query(models.Vote).filter(models.Vote.post_id == vote_.post_id,models.Vote.user_id==current_user.id)
    found_vote = vote_query.first()
    if(vote_.dir==1):
        if found_vote:
            raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=f"User with id:{current_user.id} has already voted on post with id: {vote_.post_id}")
        newvote = models.Vote(post_id = vote_.post_id, user_id = current_user.id)
        db.add(newvote)
        db.commit()
        return {"message":"Succesfully added Vote"}
    else:
        if not found_vote:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Vote does not exist")
        
        vote_query.delete()
        db.commit()

        return {"message" : "Succesfully Vote Deleted"}


    