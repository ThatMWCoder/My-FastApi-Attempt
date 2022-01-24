from fastapi import FastAPI, Response, status, Depends, APIRouter

from sqlalchemy.orm.session import Session

from .. import schemas, database, models

from . import oauth2

from fastapi.exceptions import HTTPException


router = APIRouter(

    prefix="/api/like",

    tags=['Like']
)



@router.post("/", status_code=status.HTTP_201_CREATED)

def like(like: schemas.Like, db: Session = Depends(database.get_db), current_user: int = Depends(oauth2.get_current_user)):

    like_query = db.query(models.Like).filter(

        models.Like.post_id == like.post_id,
        models.Like.user_id == current_user.id)
    found_like = like_query.first()
    if (like.dir == 1): 
        if found_like:

            raise HTTPException(

                status_code=status.HTTP_409_CONFLICT, detail="Already liked")

        new_like = models.Like(post_id=like.post_id, user_id=current_user.id)
        db.add(new_like)

        db.commit()
        return {"message": "Liked successfully"}
    else:
        if not new_like:

            raise HTTPException(

                status_code=status.HTTP_404_NOT_FOUND, detail="Like does not exist")

        like_query.delete(synchronize_session=False)

        db.commit()

        return {"message": "Unliked successfully"}

