from fastapi import APIRouter,Depends, status, HTTPException, Response
from fastapi.security.oauth2 import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from .. database import get_db
from .. import schemas,models,utils,oauth2


router = APIRouter(
    tags=['Authentication']
)

@router.post('/login')
def login(user_credentials: OAuth2PasswordRequestForm = Depends() ,db:Session = Depends(get_db)):
    #now the user_credentials will be in OAuth2PasswordRequestForm's format
    #Like it is a dictionary with fields {"username": "", "password": ""} 
    # In our case we are getting email and password, so "username" field will contain email and "password" will contain password

    user = db.query(models.User).filter(models.User.email == user_credentials.username).first()

    if not user:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,detail=f"Invalid Credentials")
    
    if not utils.verify(user_credentials.password,user.password):
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,detail=f"Invalid Credentials")
    
    #Creating a Token
    access_token = oauth2.create_access_token(data={"user_id" : user.id})



    return {"Access_Token": access_token, "token_type": "bearer"}
    

