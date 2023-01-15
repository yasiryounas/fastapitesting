from jose import JWSError,jwt
from datetime import datetime,timedelta
from . import schemas, database, models
from fastapi import status, HTTPException, Depends
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session
from .config import env_settings

oauth2_scheme = OAuth2PasswordBearer(tokenUrl='login')

#SECRET_KEY
#Algorithm
#Expriation Time

SECRET_KEY = env_settings.secret_key
ALGORITHM = env_settings.algorithm
ACCESS_TOKEN_EXPIRE_TIME = env_settings.access_token_expire_minutes

def create_access_token(data: dict):
    to_encode = data.copy()

    expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_TIME)
    to_encode.update({"exp": expire})

    encoded_jwt = jwt.encode(to_encode,SECRET_KEY,algorithm=ALGORITHM)
    return encoded_jwt



def verify_access_token(token: str, credentials_exception):
    try:
        payoad = jwt.decode(token,SECRET_KEY,algorithms=[ALGORITHM])
        extracted_id: str = payoad.get("user_id")
        if id is None:
            raise credentials_exception
        token_data = schemas.Tokendata(id=extracted_id)
    except JWSError:
        raise credentials_exception
    return token_data

def get_current_user(token: str = Depends(oauth2_scheme), db: Session = Depends(database.get_db)):
    credentials_expection = HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail=f"Could not validate credentials", headers={"WWW-Authenticate":"Bearer"})
    verified_token = verify_access_token(token,credentials_expection)
    user = db.query(models.User).filter(models.User.id == verified_token.id).first()
    return user
