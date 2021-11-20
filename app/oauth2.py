from jose import JWTError, jwt
from datetime import datetime, timedelta
from . import schema, database, models
from fastapi import Depends, status, HTTPException
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")
# SECRET KEY
SECRET_KEY = "09d25e094faa6ca2556c818166b7a9563b93f7099f6f0f4caa6cf63b88e8d3e7"

# Algorithm
ALGORITHM = "HS256"

# Exprition time
ACCESS_TOKEN_EXPIRE_MINUTES = 30

def create_access_token(data: dict):
    to_encode = data.copy()
    
    expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})

    encode_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

   
    return encode_jwt

def verify_access_token(token: str, creadentials_exception):

    try:
        print(token)
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        print(payload)
        id: str = payload.get("user_id")
        print(id)
        if id is None:
            print(2)
            raise creadentials_exception
        print(3)
        token_data = schema.TokenData(id=id)
        print("data",token_data)

    except JWTError:
        raise creadentials_exception

    return token_data

def get_current_user(token: str = Depends(oauth2_scheme),db: Session =  Depends(database.get_db)):
    print(222)
    creadentials_exception = HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, 
                                            detail=f"Could not validate creadentials", 
                                            headers={"WWW-Authenticate": "Bearer"})

    token = verify_access_token(token, creadentials_exception)

    user = db.query(models.User).filter(models.User.id == token.id).first()
    print(user)
    return user 