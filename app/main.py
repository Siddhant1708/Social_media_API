from fastapi import FastAPI #type:ignore
from fastapi.params import Body #type: ignore
import psycopg2
from psycopg2.extras import RealDictCursor
from random import randrange
import time 
from . import models # here . refers to current directory
from .database import engine,get_db
from .routers import post,user,auth


models.Base.metadata.create_all(bind=engine) #for table creation based on the classes present in the model 

app = FastAPI()


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



app.include_router(post.router) # includes the router object from post routers
app.include_router(user.router)
app.include_router(auth.router)

@app.get('/')
async def root():
    return {'message':"Welcome to API"}

