from fastapi import FastAPI, Response, status, HTTPException, Depends, APIRouter
from sqlalchemy.orm import Session
from typing import Optional, List
from .. import oauth2, schemas, database, models

router = APIRouter(prefix="/vote", tags=['Vote'])


@router.post("/", status_code=status.HTTP_201_CREATED)
def vote(request_vote: schemas.Vote, db: Session = Depends(database.get_db), current_user: int = Depends(oauth2.get_current_user)):
    post_found = db.query(models.Post).filter(models.Post.id == request_vote.post_id).first()
    if not post_found:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f"Post ID {request_vote.post_id} does not exist")
    vote_query = db.query(models.Vote).filter(
        models.Vote.post_id == request_vote.post_id, models.Vote.user_id == current_user.id)
    found_vote = vote_query.first()
    if request_vote.dir == 1:
        if found_vote:
            raise HTTPException(status_code=status.HTTP_409_CONFLICT,
                                detail=f"user {current_user.id} has already voted on post {request_vote.post_id}")
        new_vote = models.Vote(
            post_id=request_vote.post_id, user_id=current_user.id)
        db.add(new_vote)
        db.commit()
        return {"message": "successfully added vote"}
    else:
        if not found_vote:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="Vote does not exist")
        vote_query.delete(synchronize_session=False)
        db.commit()
        return {"message": "Successfully deleted the post"}
