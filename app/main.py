from fastapi import FastAPI #type:ignore
from . import models # here . refers to current directory
from .database import engine,get_db
from .routers import post,user,auth,vote
from .config import settings


# models.Base.metadata.create_all(bind=engine) #for table creation based on the classes present in the model 

app = FastAPI()

app.include_router(post.router) # includes the router object from post routers
app.include_router(user.router)
app.include_router(auth.router)
app.include_router(vote.router)

@app.get('/')
async def root():
    return {'message':"Welcome to API"}

