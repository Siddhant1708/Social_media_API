from .database import Base
from sqlalchemy.orm import relationship 
from sqlalchemy import Column, Integer, String, Boolean, ForeignKey
from sqlalchemy.sql.sqltypes import TIMESTAMP
from sqlalchemy.sql.expression import text



#one of the drawback of sqlalchemy is, if our table is created then we can not add, modify or update any coloumn.
# so what happens is when our server starts, sqlalchemy checks whther a table with name "posts" is present or not., if it is, then it doesnot do anything.
# so for making changes, we need to drop all the tables and create tables from scratch, ** which we can't do.**
# it only creates a table, if it has not seen a table with a given name


# so we got a tool (**Alembic**, a database migration tool) , which allows us to do these things 
# since dev can track changes to code and rollback easily, so why can't we do the same for DB's.
# a DB migration tool allow us to incrementally track changes to DB schema and rollback changes to any point of time.
# so we will use tool callled Alembic to make changes to out DB.
# alembic can automatically pull databases model's from sqlalchemy and generate proper tables


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
