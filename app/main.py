# from typing import Optional, List
# from fastapi import FastAPI, Response, status, HTTPException, Depends
# from fastapi.params import Body
# from pydantic import BaseModel
# from random import randrange
# import psycopg2
# from psycopg2.extras import RealDictCursor
# import time
# from sqlalchemy.orm import Session
# from sqlalchemy.sql.functions import mode
# from . import models, schemas, utils
# from .database import engine, get_db
from fastapi import FastAPI
from . import models
from .database import engine
from .routers import post, user, auth, vote
from .config import env_settings
from fastapi.middleware.cors import CORSMiddleware

# After Alembic implementation
# models.Base.metadata.create_all(bind=engine)

app = FastAPI()

# For CORS Policy

# origins=["https://www.google.com"]
# For all public domain
origins=["*"]

app.add_middleware(CORSMiddleware,allow_origins=origins,allow_credentials=True,allow_methods=["*"],allow_headers=["*"],)




print(env_settings.database_hostname)
# my_posts = [{"title": "title of post 1", "content": "content of post 1", "id": 1}, {
#     "title": "favorite foods", "content": "I like Pizza", "id": 2}]


# def find_post(id):
#     for p in my_posts:
#         if p['id'] == id:
#             return p


# def find_index_post(id):
#     for i, p in enumerate(my_posts):
#         if p['id'] == id:
#             return i


app.include_router(post.router)
app.include_router(user.router)
app.include_router(auth.router)
app.include_router(vote.router)


@app.get("/")
async def root():
    return {"message": "Hello World"}
