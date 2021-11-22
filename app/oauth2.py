from jose import JWTError, jwt
from datetime import datetime, timedelta
from . import schema, database, models
from fastapi import Depends, status, HTTPException
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session
from .config import settings

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")
# SECRET KEY
SECRET_KEY = settings.secret_key
# Algorithm
ALGORITHM = settings.algorithm
# Exprition time
ACCESS_TOKEN_EXPIRE_MINUTES = settings.access_token_ex

def create_access_token(data: dict):
    to_encode = data.copy()
    
    expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})

    encode_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

   
    return encode_jwt

def verify_access_token(token: str, creadentials_exception):

    try:
        
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        
        id: str = payload.get("user_id")
       
        if id is None:
            print(2)
            raise creadentials_exception
       
        token_data = schema.TokenData(id=id)
        

    except JWTError:
        raise creadentials_exception

    return token_data

def get_current_user(token: str = Depends(oauth2_scheme),db: Session =  Depends(database.get_db)):
    
    creadentials_exception = HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, 
                                            detail=f"Could not validate creadentials", 
                                            headers={"WWW-Authenticate": "Bearer"})

    token = verify_access_token(token, creadentials_exception)

    user = db.query(models.User).filter(models.User.id == token.id).first()
    
    return user 