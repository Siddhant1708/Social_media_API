from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from dotenv import load_dotenv
import os

load_dotenv()

DB_USER = os.getenv("DB_USER")
DB_PASSWORD = os.getenv("DB_PASSWORD")
DB_NAME = os.getenv("DB_NAME")
DB_HOST = os.getenv("DB_HOST")


#connection string, which tells us, where is our postgress DB is located
# SQLALCHEMY_DATABASE_URL = 'postgresql://<username>:<password>@<ip-address/hostname>/<database_name>'  #Format of a Connection string
SQLALCHEMY_DATABASE_URL = f"postgresql://{DB_USER}:{DB_PASSWORD.replace('@', '%40')}@{DB_HOST}/{DB_NAME}"


#we need to create an engine, which is responsible for connecting the DB with Sqlalchemy
engine = create_engine(SQLALCHEMY_DATABASE_URL)

#for talking to sql DB, we need to use a Session
SessionLocal = sessionmaker(autocommit=False,autoflush=False,bind=engine)

#all of the classes which will define the table in DB, are going to extend this 'Base' class
Base = declarative_base()

#Beacuse of this ORM , we don't need to create table by going to pgadmin, rather we can create those using this ORM

def get_db():  # whenever a request comes, we call this to get a session for a db, and at the end, session is closed
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()    
