from sqlalchemy.orm import Session
from fastapi.security import HTTPBearer
from database.models import User, Rating, Image, RatingImage
from database.db import get_db
from configure.config import settings
from fastapi import APIRouter, HTTPException, Depends, status, UploadFile, File, Path
from sqlalchemy import and_
from schemas import RatingResponseModel, RatingRequestModel
from typing import List
from src.repository.rating import calculate_total_rating

router = APIRouter(prefix='/rating', tags=["rating"])

@router.post("/", response_model=RatingResponseModel)
@has_role("user")
async def create_rating(body: RatingRequestModel, image_id: int, db: Session = Depends(get_db), current_user: User = Depends(auth_service.get_current_user)):
    new_rating = db.query(Rating).filter(and_(Rating.image_id == image_id, Rating.user_id == current_user.id)).first()
    if new_rating:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="This rating is exists!")
    image_r = db.query(Image).filter(Image.id == image_id)
    if image_r is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Image not found!')
    new_rating = Rating(**body.dict(), user_id=current_user.id, image_id=image_id)
    db.add(new_rating)
    db.commit()
    db.refresh(new_rating)
    await calculate_total_rating(image_id=image_id, db = db)
    return new_rating

@router.get("/{image_id}", response_model=List[RatingResponseModel])
@has_role("admin", "moderator")
async def get_image_rating(image_id: int, db: Session = Depends(get_db)):
    image_r = db.query(Image).filter(Image.id == image_id)
    if image_r is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Image not found!')
    list_rating = db.query(Rating).filter(Rating.image_id == image_id).all()
    return list_rating


@router.get("/{user_id}", response_model=List[RatingResponseModel])
@has_role("admin", "moderator")
async def get_user_rating(user_id: int, db: Session = Depends(get_db)):
    list_rating = db.query(Rating).filter(Rating.user_id == user_id).all()
    return list_rating

@router.delete("/{rating_id}")
@has_role("admin", "moderator")
async def delete_rating(image_id: int, user_id: int, db: Session = Depends(get_db))
    new_rating = db.query(Rating).filter(and_(Rating.image_id == image_id, Rating.user_id == user_id)).first()
    if new_rating is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Rating not found!')
    db.delete(new_rating)
    db.commit()