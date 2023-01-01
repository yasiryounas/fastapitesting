from typing import Optional, List
from fastapi import FastAPI, Response, status, HTTPException, Depends
from fastapi.params import Body
from pydantic import BaseModel
from random import randrange
import psycopg2
from psycopg2.extras import RealDictCursor
import time
from sqlalchemy.orm import Session
from . import models, schemas, utils
from .database import engine, get_db

models.Base.metadata.create_all(bind=engine)

app = FastAPI()


while True:
    try:
        conn = psycopg2.connect(host='localhost', database='fastapi',
                                user='postgres', password='yasirhome', cursor_factory=RealDictCursor)
        cursor = conn.cursor()
        print("Database connection successfully!")
        break
    except Exception as error:
        print("Connection to database failed")
        print("Error:", error)
        time.sleep(2)


my_posts = [{"title": "title of post 1", "content": "content of post 1", "id": 1}, {
    "title": "favorite foods", "content": "I like Pizza", "id": 2}]


def find_post(id):
    for p in my_posts:
        if p['id'] == id:
            return p


def find_index_post(id):
    for i, p in enumerate(my_posts):
        if p['id'] == id:
            return i


@app.get("/")
async def root():
    return {"message": "Hello World"}


@app.get("/posts", response_model=list[schemas.Post])
# def get_posts():
#    cursor.execute("""select * from posts """)
#    posts = cursor.fetchall()
#    return {"data": posts}
def get_posts(db: Session = Depends(get_db)):
    extractedposts = db.query(models.Post).all()
    return extractedposts

# title str, content str


@app.post("/posts", status_code=status.HTTP_201_CREATED, response_model=schemas.Post)
# just fetching the body param
# def create_post(payLoad: dict = Body(...)):
# print(payLoad)
# return{"NewData":f"Title {payLoad['title']} Content: {payLoad['content']}"}
# def create_post(post: Post):
#    cursor.execute("""INSERT INTO posts (title,content,published) VALUES(%s,%s,%s) RETURNING *""",
#                   (post.title, post.content, post.published))
#    post = cursor.fetchone()
#    conn.commit()
# print(post.title)
# post_dict = post.dict()
# post_dict['id'] = randrange(0,100000)
# my_posts.append(post_dict)
#    return {"data": post}
def create_post(post: schemas.PostCreate, db: Session = Depends(get_db)):
    # new_post = models.Post(title=post.title, content=post.content, published=post.published)
    # **post.dict() automatically transfer it to json format, like above
    new_post = models.Post(**post.dict())
    db.add(new_post)
    db.commit()
    db.refresh(new_post)
    return new_post


@app.get("/posts/latest", response_model=schemas.Post)
# def get_latest_post():
#    cursor.execute("""SELECT * FROM posts ORDER BY id DESC LIMIT 1""")
#    post = cursor.fetchone()
# post = my_posts[len(my_posts)-1]
#    return {"latest_post": post}
def get_latest_post(db: Session = Depends(get_db)):
    extractedposts = db.query(models.Post).order_by(
        models.Post.id.desc()).first()
    return extractedposts


@app.get("/posts/{id}", response_model=schemas.Post)
# def get_post(id: int, response: Response):
# post = find_post(id)
#    cursor.execute("""SELECT * FROM posts WHERE id = %s""", (str(id),))
#    text_post = cursor.fetchone()
#    if not text_post:
#       raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
#                            detail=f"Post with id: {id} was not found")
# response.status_code = status.HTTP_404_NOT_FOUND
# return {'message': f"Post with id: {id} was not found"}
#    return {"post_detail": text_post}
def get_post(id: int, db: Session = Depends(get_db)):
    extracted_post = db.query(models.Post).filter(models.Post.id == id).first()
    if not extracted_post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"Post with id: {id} was not found")
    return extracted_post


@app.delete("/posts/{id}", status_code=status.HTTP_204_NO_CONTENT)
# def delete_post(id: int):
# deleting the post
# find the index in the array that has required ID
# my_posts.pop(index)
#    cursor.execute("""DELETE FROM posts WHERE id = %s RETURNING *""", (str(id)))
#    deleted_post = cursor.fetchone()
#    conn.commit()
#    if deleted_post == None:
#        raise HTTPException(
#            status_code=status.HTTP_404_NOT_FOUND, detail="id does not exist")
# index = find_index_post(id)
# if index == None:
#    raise HTTPException(
#        status_code=status.HTTP_404_NOT_FOUND, detail="id does not exist")
# my_posts.pop(index)
#   return Response(status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id: int, db: Session = Depends(get_db)):
    extracted_post = db.query(models.Post).filter(models.Post.id == id)
    if extracted_post.first() == None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="id does not exist")
    extracted_post.delete(synchronize_session=False)
    db.commit()
    return Response(status_code=status.HTTP_204_NO_CONTENT)


@app.put("/posts/{id}", response_model=schemas.Post)
# def update_post(id: int, post: Post):
#   cursor.execute("""UPDATE posts SET (title,content,published) = (%s,%s,%s) WHERE id = %s RETURNING *""",
#                   (post.title, post.content, post.published, str(id),))
#    updated_post = cursor.fetchone()
#    conn.commit()
#    if updated_post == None:
#        raise HTTPException(
#            status_code=status.HTTP_404_NOT_FOUND, detail="id does not exist")
# index = find_index_post(id)
# if index == None:
#    raise HTTPException(
#        status_code=status.HTTP_404_NOT_FOUND, detail="id does not exist")
# post_dict = post.dict()
# post_dict['id'] = id
# my_posts[index] = post_dict
#    return {'message': updated_post}
def update_post(id: int, post: schemas.PostCreate, db: Session = Depends(get_db)):
    extracted_post = db.query(models.Post).filter(models.Post.id == id)
    if extracted_post.first() == None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="id does not exist")
    extracted_post.update(post.dict(), synchronize_session=False)
    db.commit()
    return extracted_post.first()


@app.post("/users", status_code=status.HTTP_201_CREATED, response_model=schemas.UserOut)
def create_user(user: schemas.UserCreate, db: Session = Depends(get_db)):
    # Hash the password - user.password
    hashed_password = utils.hash(user.password)
    user.password = hashed_password
    new_user = models.User(**user.dict())
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user


@app.get("/users/{id}", response_model=schemas.UserOut)
def get_user(id: int, db: Session = Depends(get_db)):
    extratced_user = db.query(models.User).filter(models.User.id == id).first()
    if extratced_user == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"id: {id} does not exist")
    return extratced_user
