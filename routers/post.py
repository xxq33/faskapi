
import sys
sys.path.append("/Users/admin/Desktop/self study/api/app")
import models, schemas

from database import engine, get_db
from sqlalchemy import func
from fastapi import FastAPI, Response, status, HTTPException, Depends, APIRouter
from sqlalchemy.orm import Session
from typing import Optional, List
from oath2 import get_current_user

router = APIRouter(
    prefix="/posts",
    tags=['Posts']
)



@router.get("/", response_model=List[schemas.PostOut])
# @router.get("/")
def get_posts( db: Session = Depends(get_db), current_user:int=Depends(get_current_user), limit:int=10,skip:int=0, search:Optional[str] = ""):

    # cursor.execute("SELECT * FROM public.posts ORDER BY id ASC ;")
    # results = cursor.fetchall()

    # posts = db.query(models.Post).filter_by(owner_id = current_user.id).limit(limit).offset(skip).all()
    # posts = db.query(models.Post).filter(models.Post.title.contains(search)).limit(limit).offset(skip).all()
    
    results= db.query(models.Post, func.count(models.Vote.post_id).label("votes")).join(models.Vote, models.Vote.post_id == models.Post.id, isouter=True).group_by(models.Post.id).filter(models.Post.title.contains(search)).limit(limit).offset(skip).all()
    print(results)
    
    return results


@router.post("/", status_code=status.HTTP_201_CREATED, response_model=schemas.PostResponse)
def create_posts(post: schemas.Post, db: Session = Depends(get_db),current_user:int=Depends(get_current_user)):
    # cursor.execute(f""" 
    #                 INSERT INTO public.posts (title, content, published) VALUES (%s, %s, %s) returning *
    #                """, (
    #                    post.title, post.content, post.published
    #                ))
    
    # results = cursor.fetchall()
    # conn.commit()
    
    # new_post = models.Post(title = post.title, content = post.content, published = post.published)
    print(type(current_user))
    new_post = models.Post(title = post.title, content = post.content, published = post.published, owner_id=current_user.id)
    db.add(new_post)
    db.commit()
    # retrieve the new post we just created
    db.refresh(new_post)
    return new_post




@router.get('/{id}',response_model=List[schemas.PostOut])
def get_post(id: int, response: Response, db: Session = Depends(get_db),current_user:int=Depends(get_current_user),limit: int = 10, skip: int = 0, search: Optional[str] = ""):
    # cursor.execute('''
    #                 SELECT * FROM public.posts where id = %s
    #                ''', (id, ))
    # result = cursor.fetchall()
    
    
    # post = db.query(models.Post).filter(models.Post.id == id)
    # result = db.query(models.Post).filter_by(id = id).first()
    result = db.query(models.Post, func.count(models.Vote.post_id).label("votes")).join(
        models.Vote, models.Vote.post_id == models.Post.id, isouter=True).group_by(models.Post.id).filter(models.Post.title.contains(search)).limit(limit).offset(skip).all()
   

    
    if not result:
        raise HTTPException(status_code=404, detail="Post not found")
    # if result.owner_id != current_user.id:
    #     raise HTTPException(status_code=403, detail="Not authenticated.")
    return result

@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id:int, db: Session = Depends(get_db),current_user:schemas.TokenData=Depends(get_current_user)):
    
    # cursor.execute("""
    #                 DELETE FROM public.posts WHERE id = %s RETURNING *;
    #                """, (id, ))
    # results = cursor.fetchall()
    # conn.commit()
    results = db.query(models.Post).filter_by(id=id)
    if results.first() == None:
        raise HTTPException(status_code=404, detail="Post not found.")
    if results.first().owner_id != current_user.id:
        raise HTTPException(status_code=403, detail="Not authorized to perform requested action.")
    results.delete()
    db.commit()
    
    return results

@router.put("/{id}", response_model=schemas.PostResponse)
def update_post(id: int, post: schemas.Post,status_code=200, db: Session = Depends(get_db),current_user:int=Depends(get_current_user)):
    # cursor.execute("""
    #                UPDATE public.posts SET title = %s, content = %s, published = %s WHERE id = %s RETURNING *;
    #                """ , (post.title, post.content, post.published, id))
    # results = cursor.fetchall()
    # conn.commit()
    results=db.query(models.Post).filter_by(id=id).first()
    if results == None:
        raise HTTPException(status_code=404, detail=f"the post with id: {id} does not exist.")
    if results.owner_id != current_user.id:
        raise HTTPException(status_code=403, detail="Not authorized to perform requested action.")
    results.title = post.title
    results.content = post.content
    results.published = post.published

    db.commit()
    return results


    