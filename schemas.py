# pydantic models
from pydantic import BaseModel
from datetime import datetime
from pydantic import EmailStr, Field
from typing import Optional
from pydantic.types import conint
        
class UserCreate(BaseModel):
    email: EmailStr
    password: str

        
class UserResponse(BaseModel):
    id: int
    email: EmailStr
    created_at: datetime
    class Config:
        orm_mode = True
        
class UserLogin(BaseModel):
    email: EmailStr
    password: str
    
    

class Post(BaseModel):
    title: str = None
    content: str
    published: bool = True
    
    class Config:
        orm_mode = True
    
class PostResponse(Post):
    id: int
    created_at: datetime
    owner_id: int
    owner : UserResponse
    class Config:
        orm_mode = True

class PostOut(BaseModel):
    Post: Post
    votes: int
    class Config:
        orm_mode = True

class Token(BaseModel):
    access_token : str
    token_type : str
    
    
class TokenData(BaseModel):
    id : Optional[int] = None
    
    
class Vote(BaseModel):
    post_id: int
    dir: conint(ge=0, le=1)
    
