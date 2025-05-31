from sqlalchemy.orm import Session
from fastapi import FastAPI, Response, status, HTTPException, Depends, APIRouter, Form
from app.database import engine, get_db
from fastapi.security import OAuth2PasswordRequestForm
from .. import schemas, utils, models
from . import Oauth2

router=APIRouter(tags=['auth'])

@router.post("/login")
def login(User_Credentials: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    user=db.query(models.User).filter(models.User.email== User_Credentials.username).first()
    if not user:
        raise HTTPException(status_code=401, detail=f"Invalid Credentials")
    passwd =  utils.passwd_verify(User_Credentials.password, user.password)
    if not passwd:
        raise HTTPException(status_code=401, detail=f"Invalid Credentials")
    Access_Token = Oauth2.create_token(data = {"user_id": user.id})
    return {"JWT":Access_Token, "type": "bearer"}

    

