from .. import models,schemas,utils  # here . refers to current directory
from fastapi import FastAPI, status, HTTPException, Response, Depends, APIRouter #type:ignore
from sqlalchemy.orm import Session
from ..database import get_db

router = APIRouter(
    prefix='/users',
    tags=["Users"]
)


#for creating a new user
@router.post("/", status_code=status.HTTP_201_CREATED,response_model=schemas.UserOut)
def create_user(user : schemas.UserCreate,db:Session = Depends(get_db)):

    #password hashing
    
    user.password = utils.hash(user.password)

    new_user = models.User(**user.dict()) 
    db.add(new_user) 
    db.commit()
    db.refresh(new_user)

    return new_user

@router.get('/{id}',response_model=schemas.UserOut)
def get_user(id:int,db: Session = Depends(get_db)):
    user = db.query(models.User).filter(models.User.id == id).first()

    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f"User with {id} does not exist")
    
    return user