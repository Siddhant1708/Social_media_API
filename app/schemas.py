from pydantic import BaseModel, Field, EmailStr, conint
from typing import Optional
from datetime import datetime





#So what we want from client for creating the post, we need title, Content 
#we use this to ensure, the data we got the client should be in our desired format
class PostBase(BaseModel):
    title : str = Field(...,min_length=3)
    content: str
    published: bool = True  # make the dafualt value as True
    # published: Optional[bool] = True  ## or we can just give a default value and it beomes optional i.e, pub : bool=True


class PostCreate(PostBase):
    pass

#this model is for data we require form user to create it in our DB 

class UserCreate(BaseModel):
    email : EmailStr
    password : str 

class UserLogin(BaseModel):
    email : EmailStr
    password : str    

class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    id: Optional[str] = None    



class Vote(BaseModel):
    post_id : int
    dir: conint(le=1) # allows only integers <= 1 becoz 0 means to dislike and 1 means like.




#---------------------------------------------------
#above models are responsible the handling data for us, i.e the data we want to recieve
#below model are responsible for handling the data for user, i.e structuring the response for the user OR the data we want to send

class UserOut(BaseModel):
    id : int
    email : EmailStr


class Post(PostBase):
    id: int
    created_at: datetime 
    owner_id: int
    owner: UserOut
 
    

class Postout(BaseModel):
    Post: Post
    votes: int
    
    


    