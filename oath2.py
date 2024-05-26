import fastapi
from jose import JWTError, jwt
from datetime import datetime, timedelta
import schemas, database, models
from fastapi import Depends, status, HTTPException
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session

oauth2_scheme = OAuth2PasswordBearer(tokenUrl='login')

#  secret, algorithm, expiration

SECRET_KEY = "01a3659ad701df4254f3ad7590aec1f0b825af604afd06607a7fb4e98598f306"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

def create_access_token(data: dict):
    to_encode = data.copy()
    expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp" : expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt 

def verify_access_token(token: str, credential_exception):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        id : int = payload.get("user_id")
        print(f"test: {type(id)}")
        if id is None:
            raise credential_exception
        
        token_data = schemas.TokenData(id = (id))
    except JWTError as e:
        raise credential_exception
    return token_data
 
# take the token from the request automatically and verify it, extract the id, 
# fetch the user from the database and add it into as a parameter into our path operation function.
def get_current_user(token: str = Depends(oauth2_scheme), db:Session = Depends(database.get_db) ):
    credential_exception = HTTPException(status_code=401, detail=f"Could not validate credentials", headers={'WWW-Authenticate':'bearer'})
    
    token = verify_access_token(token, credential_exception)
    user = db.query(models.User).filter_by(id = token.id).first()
    return user