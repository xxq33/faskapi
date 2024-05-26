import sys
sys.path.append("/Users/admin/Desktop/self study/api/app")
import models, schemas, database, utils

from database import get_db
from fastapi import FastAPI, Response, status, HTTPException, Depends, APIRouter
from sqlalchemy.orm import Session

router = APIRouter(
    prefix="/users",
    tags=["Users"]
)

# User section:
@router.post("/", status_code=201, response_model=schemas.UserResponse)
def create_user(user: schemas.UserCreate, db: Session = Depends(get_db)):
    
    # hash the password
    hashed_pwd = utils.hash(user.password)
    user.password = hashed_pwd
    
    # new_user = models.User(email = user.email, password = user.password)
    new_user = models.User(**user.model_dump())
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user

@router.get("/{id}" ,response_model=schemas.UserResponse)
def get_user(id : int, db: Session = Depends(get_db)):
    results = db.query(models.User).filter_by(id = id).first()
    if results is None:
        raise HTTPException(status_code=404, detail= f"User with id {id} not found.")
    return results