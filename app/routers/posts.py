from typing import List, Optional
from fastapi import FastAPI, Response, status, Depends, APIRouter
from fastapi.exceptions import HTTPException

from sqlalchemy import func

from ..routers import oauth2
from .. import models, schemas
from sqlalchemy.orm import Session
from ..database import get_db


router = APIRouter(
    prefix="/api/posts",
    tags=['Posts']
)


@router.get("/", response_model=List[schemas.PostWithLike])
def get_posts(
    db: Session = Depends(get_db),
    current_user: int = Depends(oauth2.get_current_user),
    limit: int = 10,
    skip: int = 0,
    search: Optional[str] = ""
):
    posts = db.query(models.Post, func.count(models.Like.post_id).label("likes")).join(models.Like, models.Like.post_id == models.Post.id,
                                                                                       isouter=True).group_by(models.Post.id).filter(models.Post.title.contains(search)).limit(limit).offset(skip).all()
    return posts


@router.get("/my-posts", response_model=List[schemas.PostWithLike])
def get_my_posts(db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):
    results = db.query(models.Post, func.count(models.Like.post_id).label("likes")).join(models.Like, models.Like.post_id == models.Post.id, isouter=True).group_by(models.Post.id).filter(
        models.Post.owner_id == current_user.id).all()
    return results

# Getting single post


@router.get("/my-posts/{id}", response_model=schemas.PostWithLike)
def get_post(id: int, db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):
    post = db.query(models.Post, func.count(models.Like.post_id).label("likes")).join(models.Like, models.Like.post_id == models.Post.id,
                                                                                      isouter=True).group_by(models.Post.id).filter(models.Post.owner_id == current_user.id).filter(models.Post.id == id).first()
    if not post:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"post with id {id} not found"
        )
    return post


@router.get("/{id}", response_model=schemas.PostWithLike)
def get_post(id: int, db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):
    post = db.query(models.Post, func.count(models.Like.post_id).label("likes")).join(
        models.Like, models.Like.post_id == models.Post.id, isouter=True).group_by(models.Post.id).filter(models.Post.id == id).first()
    if not post:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"post with id {id} not found"
        )
    return post


# Create post
@router.post("/", status_code=status.HTTP_201_CREATED, response_model=schemas.Post)
def create_post(post: schemas.PostCreate, db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):
    new_post = models.Post(owner_id=current_user.id, **post.dict())
    db.add(new_post)
    db.commit()
    db.refresh(new_post)
    return new_post


# Update post
@router.put("/{id}", response_model=schemas.Post)
def update_post(id: int, updated_post: schemas.PostCreate, db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):
    post_query = db.query(models.Post).filter(models.Post.id == id)
    post = post_query.first()
    if post == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"Post with id {id} does not exist")
    if post.owner_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                            detail=f"Sorry not authorized")
    post_query.update(updated_post.dict(), synchronize_session=False)
    db.commit()
    return post_query.first()

    # Deleting post


@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id: int, db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):
    post_query = db.query(models.Post).filter(models.Post.id == id)
    post = post_query.first()
    if post == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"Post with id {id} does not exist")
    if post.owner_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                            detail=f"Sorry not authorized")

    post_query.delete(synchronize_session=False)
    db.commit()
    return Response(status_code=status.HTTP_204_NO_CONTENT)
