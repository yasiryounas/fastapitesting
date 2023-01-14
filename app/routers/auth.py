from fastapi import APIRouter, Depends, status, HTTPException, responses
from fastapi.security.oauth2 import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session

from .. import database, schemas, models, utils, oauth2


router = APIRouter(tags=['Authentication'])


@router.post("/login", response_model=schemas.Token)
# def login(user_credentials: schemas.UserLogin, db: Session = Depends(database.get_db)):
def login(user_credentials: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(database.get_db)):
    # OAuth2PasswordRequestForm will return username and password =
    saved_user_login = db.query(models.User).filter(
        # models.User.email == user_credentials.email).first()
        models.User.email == user_credentials.username).first()
    if saved_user_login == None:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN, detail="Invalid Credential")

    if not utils.verify(user_credentials.password, saved_user_login.password):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN, detail=f"Invalid Credential")
    access_token = oauth2.create_access_token(
        data={"user_id": saved_user_login.id})
    return {"access_token": access_token, "token_type": "token"}
