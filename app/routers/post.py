from fastapi import FastAPI, Response, status, HTTPException, Depends, APIRouter
from sqlalchemy.orm import Session
from typing import Optional, List
from ..database import get_db
from .. import models, schemas, oauth2

router = APIRouter(
    prefix="/posts", tags=['Posts']
)


@router.get("/", response_model=list[schemas.Post])
# def get_posts():
#    cursor.execute("""select * from posts """)
#    posts = cursor.fetchall()
#    return {"data": posts}
def get_posts(db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user), limit: int = 10, skip: int = 0, search: Optional[str] = ""):
    extractedposts = db.query(models.Post).filter(
        models.Post.title.contains(search)).limit(limit).offset(skip).all()
    return extractedposts

# title str, content str


@router.post("/", status_code=status.HTTP_201_CREATED, response_model=schemas.Post)
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
def create_post(post: schemas.PostCreate, db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):
    # new_post = models.Post(title=post.title, content=post.content, published=post.published)
    # **post.dict() automatically transfer it to json format, like above
    print(current_user)
    # new_post = models.Post(**post.dict())
    new_post = models.Post(owner_id=current_user.id, **post.dict())
    db.add(new_post)
    db.commit()
    db.refresh(new_post)
    return new_post


@router.get("/latest", response_model=schemas.Post)
# def get_latest_post():
#    cursor.execute("""SELECT * FROM posts ORDER BY id DESC LIMIT 1""")
#    post = cursor.fetchone()
# post = my_posts[len(my_posts)-1]
#    return {"latest_post": post}
def get_latest_post(db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):
    extractedposts = db.query(models.Post).order_by(
        models.Post.id.desc()).first()
    return extractedposts


@router.get("/{id}", response_model=schemas.Post)
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
def get_post(id: int, db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):
    extracted_post = db.query(models.Post).filter(models.Post.id == id).first()
    if not extracted_post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"Post with id: {id} was not found")
    if extracted_post.owner_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                            detail="Not authorized to perform requested action")
    return extracted_post


@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
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
def delete_post(id: int, db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):
    extracted_post = db.query(models.Post).filter(models.Post.id == id)
    if extracted_post.first() == None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="id does not exist")
    if extracted_post.first().owner_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                            detail="Not authorized to perform requested action")
    extracted_post.delete(synchronize_session=False)
    db.commit()
    return Response(status_code=status.HTTP_204_NO_CONTENT)


@router.put("/{id}", response_model=schemas.Post)
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
def update_post(id: int, post: schemas.PostCreate, db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):
    extracted_post = db.query(models.Post).filter(models.Post.id == id)
    if extracted_post.first() == None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="id does not exist")
    if extracted_post.first().owner_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                            detail="Not authorized to perform requested action")
    extracted_post.update(post.dict(), synchronize_session=False)
    db.commit()
    return extracted_post.first()
