from .. import schemas, models, utils, database
from sqlalchemy.orm import Session
from fastapi import FastAPI, Response, status, HTTPException, Depends, APIRouter
from app.database import engine, get_db



router=APIRouter(
    prefix="/user",
    tags=['Users']
)

@router.post("/",status_code=status.HTTP_201_CREATED, response_model=schemas.userresponce)
def create_user(User: schemas.user , db: Session = Depends(get_db)):
   hashed_password= utils.passwd_hash(User.password)
   User.password=hashed_password
   new_user=models.User(**User.dict())
   db.add(new_user)
   db.commit()
   db.refresh(new_user)
   return new_user

@router.get("/{id}", response_model=schemas.userresponce)
def get_user(id: int, db: Session = Depends(get_db)):
    user = db.query(models.User).filter(models.User.id == id).first()
    if not user:
        raise HTTPException(status_code=404, detail=f"your user with id  {id} is not found  ")
    return user

@router.post("/{id}",response_model=schemas.userresponce)
def upadte_user(id: int , User: schemas.userupdate , db: Session = Depends(get_db)):
    query = db.query(models.User).filter(models.User.id == id)
    if not query.first():
        raise HTTPException(status_code=404, detail=f"your user with id  {id} is not found  ")
    
    query.update(User.dict(exclude_unset=True), synchronize_session=False)

    db.commit()
    updated_user=query.first()
    
    
    return updated_user

@router.delete("/{id}")
def delete_user(id: int, db: Session = Depends(get_db) ):
    user=db.query(models.User).filter(models.User.id == id).first()
    if not user:
        raise HTTPException(status_code=404, detail=f"your user with id  {id} is not found  ")
    db.delete(user)
    db.commit()
    return f"your user with {id} is deleted"