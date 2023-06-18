from typing import List, Optional
from datetime import date
from fastapi import APIRouter, Query, Depends, HTTPException, status
from sqlalchemy.orm import Session
from src.database.db import get_db
from src.database.models import Image, Tag, Rating
from src.schemas import ImageResponse

router = APIRouter(prefix="/search_filtering", tags=["search_filtering"])


@router.get("/", response_model=List[ImageResponse])
async def search_images_by_tags(tags: List[str] = Query(...), rating: Optional[int] = None, date: Optional[date] = None, db: Session = Depends(get_db)):
    try:
        images = db.query(Image).join(Image.tags).filter(Tag.name.in_(tags)).all()

        if rating is not None:
            images = [image for image in images if image.rating >= rating]

        if date is not None:
            images = [image for image in images if image.date == date]

        image_responses = []
        for image in images:
            image_responses.append(ImageResponse(
                id=image.id,
                image=image.image,
                description=image.description,
                tags=[tag.name for tag in image.tags],
                comments=[comment.content for comment in image.comments]
            ))

        return image_responses
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))


@router.get("/search-by-description", response_model=List[ImageResponse])
async def search_images_by_description(description: str = Query(...), rating: Optional[int] = None, date: Optional[date] = None, db: Session = Depends(get_db)):
    try:
        images = db.query(Image).filter(Image.description.ilike(f"%{description}%")).all()

        if rating is not None:
            images = [image for image in images if image.rating >= rating]

        if date is not None:
            images = [image for image in images if image.date == date]

        image_responses = []
        for image in images:
            image_responses.append(ImageResponse(
                id=image.id,
                image=image.image,
                description=image.description,
                tags=[tag.name for tag in image.tags],
                comments=[comment.content for comment in image.comments]
            ))

        return image_responses
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))


@router.get("/filter-by-rating", response_model=List[ImageResponse])
async def filter_images_by_rating(min_rating: int = Query(...), db: Session = Depends(get_db)):
    try:
        images = db.query(Image).filter(Image.rating >= min_rating).all()

        image_responses = []
        for image in images:
            image_responses.append(ImageResponse(
                id=image.id,
                image=image.image,
                description=image.description,
                tags=[tag.name for tag in image.tags],
                comments=[comment.content for comment in image.comments]
            ))

        return image_responses
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))


@router.get("/filter-by-date", response_model=List[ImageResponse])
async def filter_images_by_date(date_param: date = Query(...), db: Session = Depends(get_db)):
    try:
        images = db.query(Image).filter(Image.date == date_param).all()

        image_responses = []
        for image in images:
            image_responses.append(ImageResponse(
                id=image.id,
                image=image.image,
                description=image.description,
                tags=[tag.name for tag in image.tags],
                comments=[comment.content for comment in image.comments]
            ))

        return image_responses
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))

