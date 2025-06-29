from .database import Base
from sqlalchemy.orm import relationship 
from sqlalchemy import Column, Integer, String, Boolean, ForeignKey
from sqlalchemy.sql.sqltypes import TIMESTAMP
from sqlalchemy.sql.expression import text



class Post(Base):
    __tablename__ = 'posts'         # this name is for postgress for the table 

    id = Column(Integer, primary_key=True, nullable=False)
    title = Column(String, nullable=False)
    content = Column(String, nullable=False)
    published = Column(Boolean, server_default = 'TRUE', nullable=False)
    created_at = Column(TIMESTAMP(timezone=True),nullable=False,server_default=text('now()'))
    owner_id = Column(Integer,ForeignKey("users.id",ondelete="CASCADE"),nullable=False)  #we have introduced a froeign key, which is pointing to the id coloumn of user.
    # because now we want to assign a user to each post, i.e the user which creates post.

    owner = relationship("User") #what it does is, it sets up a realtionship with User class, in such way it return the user based on owner_id
    #"Each Post is related to one User (the owner), and I want to be able to access that User object through post.owner."
    #Behind the scenes, SQLAlchemy uses the owner_id foreign key to automatically query and link the User object for you.


class User(Base):
    __tablename__ = 'users'

    id = Column(Integer,primary_key=True, nullable=False)
    email = Column(String,nullable=False,unique=True)
    password = Column(String,nullable=False) 
    created_at = Column(TIMESTAMP(timezone=True),nullable=False,server_default=text('now()'))


class Vote(Base):
    __tablename__ = 'votes'
    #here we are ahving composite primary key as we have two coloums as primary key
    post_id = Column(Integer,ForeignKey('posts.id',ondelete="CASCADE"),primary_key = True)
    user_id = Column(Integer,ForeignKey("users.id",ondelete="CASCADE"),primary_key = True)    
