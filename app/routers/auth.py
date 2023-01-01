from fastapi import APIRouter, Depends, status, HTTPException, responses
from sqlalchemy.orm import Session

from .. import database, schemas, models, utils


router = APIRouter(tags=['Authentication'])


@router.post("/login")
def login(user_credentials: schemas.UserLogin, db: Session = Depends(database.get_db)):
    saved_user_login = db.query(models.User).filter(
        models.User.email == user_credentials.email).first()
    if saved_user_login == None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Invalid Credential")

    if not utils.verify(user_credentials.password, saved_user_login.password):
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail=f"Invalid Credential")
    return {"Token": "12343"}
