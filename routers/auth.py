import sys
sys.path.append("/Users/admin/Desktop/self study/api/app")

from fastapi import FastAPI, Response, status, HTTPException, Depends, APIRouter
from sqlalchemy.orm import Session
from database import engine, get_db
import models, schemas, utils, oath2
from fastapi.security.oauth2 import OAuth2PasswordRequestForm


router = APIRouter(
    tags=["Authentication"]
)

@router.post('/login', response_model=schemas.Token)
def login(user_credentials: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    print("fdfsjojwiewiiewji")
    user = db.query(models.User).filter(
        models.User.email == user_credentials.username).first()
    print(user)
    if not user:
        raise HTTPException(status_code=403, detail="Invalid Credentials")
    if not utils.verify(user_credentials.password, user.password):
        raise HTTPException(status_code=403, detail="Invalid Credentials")
    
    # pwd matched, logged in successfully
    # create a token, then return a token
    
    access_token = oath2.create_access_token(data = {"user_id": user.id})
    return {"access_token" : access_token, "token_type" : "bearer"}
    
    