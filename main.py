from fastapi import FastAPI
import psycopg2
from psycopg2.extras import RealDictCursor
import time
import models
from config import settings
from database import engine, get_db
from fastapi.middleware.cors import CORSMiddleware

from routers import post, user, auth, vote

# create the tables, and binds the table with the engine
models.Base.metadata.create_all(bind=engine)

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=[],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


        
while True:
    try:
        conn = psycopg2.connect(host='localhost', database='fastapi', user='postgres', password='wuhanxxq', cursor_factory=RealDictCursor)
        print("Database connected successfully.")
        break
    except Exception as error:
        print("Database not connected successfully.")
        print("Error: ", error)
        time.sleep(3)
cursor = conn.cursor()

    

my_posts = []



app.include_router(post.router)
app.include_router(user.router)
app.include_router(auth.router)
app.include_router(vote.router)