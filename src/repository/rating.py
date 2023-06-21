from typing import List

from sqlalchemy.orm import Session
from sqlalchemy import and_, func

from src.database.models import User, Image, RatingImage, Rating


async def calculate_total_rating(image_id: int, db: Session):
    list_rating = db.query(Rating).filter(Rating.image_id == image_id).all()
    rating_image = db.query(RatingImage).filter(RatingImage.image_id == image_id).first()
    sum_r = 0
    if list_rating is None:
        db.delete(rating_image)
        db.commit()
        return None
    for i in list_rating:
        sum_r = sum_r + i.numbers_rating
    if rating_image is None:
        new_total_rating = RatingImage(now_number_rating=list_rating[0].numbers_rating, image_id=image_id)
        db.add(new_total_rating)
        db.commit()
    db.refresh(rating_image)
    rating_image.now_number_rating = sum_r / len(list_rating)
    db.commit()