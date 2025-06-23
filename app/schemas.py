from pydantic import BaseModel, Field, EmailStr
from typing import Optional

#So what we want from client for creating the post, we need title, Content 
#we use this to ensure, the data we got the client should be in our desired format
class PostBase(BaseModel):
    title : str = Field(...,min_length=3)
    content: str
    published: bool = True  # make the dafualt value as True
    # published: Optional[bool] = True  ## or we can just give a default value and it beomes optional i.e, pub : bool=True


class PostCreate(PostBase):
    pass

#this model is for data we require form user to create it in out DB 

class UserCreate(BaseModel):
    email : EmailStr
    password : str 



#---------------------------------------------------
#above models are responsible the handling data for us, i.e the data we want to recieve
#below model are responsible for handling the data for user, i.e structuring the response for the user OR the data we want to send

class Post(BaseModel):
    title: str
    content: str
    published: bool

    
class User(BaseModel):
    id : int
    email : EmailStr
    