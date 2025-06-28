from jose import JWTError, jwt
from datetime import *
from app import schemas
from fastapi.security import OAuth2PasswordBearer
from app.config import settings

from fastapi import FastAPI, Response, status, HTTPException, Depends, APIRouter, Form


oauth_schema =OAuth2PasswordBearer('login')


SECRET_KEY = settings.secret_key
ALGORITHM = settings.algorithm
ACCESS_TOKEN_EXPIRE_MINUTES = settings.access_token_expire_minutes

def create_token(data: dict):
    encoded_data =data.copy()

    expiry_time = datetime.now() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    encoded_data.update({"exp": expiry_time})
    jwt_token= jwt.encode(encoded_data,SECRET_KEY,ALGORITHM)
    return jwt_token

def verify_jwt_token(token: dict, credentials_exception):
    try:

       payload= jwt.decode(token, SECRET_KEY,algorithms=[ALGORITHM])
       id: str =payload.get("user_id")
       if id is None:
         raise credentials_exception
       token_Data = schemas.TokenData(id=id)
       return token_Data
    except JWTError:
       raise credentials_exception
    
def get_current_user(token: str = Depends(oauth_schema)):
   credentials_exception=HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,detail=f"your credentials are invalid",headers={"www_Authnticate":'Bearer'})
   return verify_jwt_token(token,credentials_exception)

    
    

