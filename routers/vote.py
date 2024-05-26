
import sys
sys.path.append("/Users/admin/Desktop/self study/api/app")
import models, schemas

from database import engine, get_db

from fastapi import FastAPI, Response, status, HTTPException, Depends, APIRouter
from sqlalchemy.orm import Session
from typing import Optional, List
from oath2 import get_current_user


router = APIRouter(
    prefix="/vote",
    tags=["Vote"]
)


@router.post('/', status_code=201)
def vote(vote: schemas.Vote, db: Session=Depends(get_db), current_user:int=Depends(get_current_user)):
    post = db.query(models.Post).filter_by(id = vote.post_id).first()
    if not post:
        raise HTTPException(status_code=404, detail="Post doesn't exits.")
    
    
    vote_query = db.query(models.Vote).filter(models.Vote.post_id == vote.post_id, models.Vote.user_id == current_user.id)
    found_vote = vote_query.first()
    if (vote.dir == 1):
        # if the user want to like the post but we already found the post, it already liked this post
        if found_vote:
            raise HTTPException(status_code=409, detail=f"User {current_user.id} has already voted on post {vote.post_id}")
        new_vote = models.Vote(post_id = vote.post_id, user_id = current_user.id)
        db.add(new_vote)
        db.commit()
        return {"message": "successfully added vote."}
    else:
        if not found_vote:
            raise HTTPException(status_code=404, detail="Vote doesn't exits.")
        vote_query.delete(synchronize_session=False)
        db.commit()
        return{"message": "successfully deleted vote."}