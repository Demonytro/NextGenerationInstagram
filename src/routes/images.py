from typing import List

from fastapi import APIRouter, HTTPException, Depends, Query
from sqlalchemy.orm import Session
from starlette import status

from schemas import ImageCreateRequest, ImageResponse, ImageUpdateImageRequest, ImageUpdateDescriptionRequest, \
    ImageUpdateTagsRequest
from src.database.db import get_db
from src.database.models import Image, Tag

router = APIRouter(prefix="/images", tags=["images"])


@router.post("/", response_model=ImageResponse)
def create_image(image_data: ImageCreateRequest, db: Session = Depends(get_db)):
    try:
        # ------------------------01-------------------------------------- Добавить загрузку картинки в клоудинари
        image = Image(image=image_data.image, description=image_data.description)

        for tag_data in image_data.tags:
            tag = db.query(Tag).filter_by(name=tag_data).first()
            if not tag:
                tag = Tag(name=tag_data)
                db.add(tag)
            image.tags.append(tag)

        db.add(image)
        db.commit()
        db.refresh(image)
        return ImageResponse(
            image=image.image,
            description=image.description,
            tags=image_data.tags
        )
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))


@router.delete("/{image_id}")
def delete_image(image_id: int, db: Session = Depends(get_db)):
    try:
        image = db.query(Image).filter(Image.id == image_id).first()
        if not image:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Image not found")

        db.delete(image)
        db.commit()
        return {"message": "Image deleted successfully"}
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))


@router.put("/{image_id}/update-image", response_model=ImageResponse)
def update_image_image(image_id: int, image_data: ImageUpdateImageRequest, db: Session = Depends(get_db)):
    try:
        image = db.query(Image).filter(Image.id == image_id).first()
        if not image:
            raise HTTPException(status_code=404, detail="Image not found")

        image.image = image_data.image
        db.commit()
        db.refresh(image)

        return ImageResponse(
            image=image.image,
            description=image.description,
            tags=[tag.name for tag in image.tags],
            comments=[comment.content for comment in image.comments]
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.put("/{image_id}/update-tags", response_model=ImageResponse)
def update_image_tags(image_id: int, tag_data: ImageUpdateTagsRequest, db: Session = Depends(get_db)):
    try:
        image = db.query(Image).filter(Image.id == image_id).first()
        if not image:
            raise HTTPException(status_code=404, detail="Image not found")

        image.tags.clear()

        for tag_name in tag_data.tags:
            tag = db.query(Tag).filter(Tag.name == tag_name).first()
            if not tag:
                tag = Tag(name=tag_name)
                db.add(tag)
            image.tags.append(tag)

        db.commit()
        db.refresh(image)

        return ImageResponse(
            image=image.image,
            description=image.description,
            tags=[tag.name for tag in image.tags],
            comments=[comment.content for comment in image.comments]
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.put("/{image_id}/update-description", response_model=ImageResponse)
def update_image_description(image_id: int, description: ImageUpdateDescriptionRequest, db: Session = Depends(get_db)):
    try:
        image = db.query(Image).filter(Image.id == image_id).first()
        if not image:
            raise HTTPException(status_code=404, detail="Image not found")

        image.description = description.description
        db.commit()
        db.refresh(image)

        return ImageResponse(
            image=image.image,
            description=image.description,
            tags=[tag.name for tag in image.tags],
            comments=[comment.content for comment in image.comments]
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/{image_id}", response_model=ImageResponse)
def get_image(image_id: int, db: Session = Depends(get_db)):
    try:
        image = db.query(Image).filter(Image.id == image_id).first()
        if not image:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Image not found")

        return ImageResponse(
            image=image.image,
            description=image.description,
            tags=[tag.name for tag in image.tags],
            comments=[comment.content for comment in image.comments]
        )
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))


@router.get("/", response_model=List[ImageResponse])
def get_images_by_tags(tags: List[str] = Query(...), db: Session = Depends(get_db)):
    try:
        images = db.query(Image).join(Image.tags).filter(Tag.name.in_(tags)).all()

        image_responses = []
        for image in images:
            image_responses.append(ImageResponse(
                image=image.image,
                description=image.description,
                tags=[tag.name for tag in image.tags],
                comments=[comment.content for comment in image.comments]
            ))

        return image_responses
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))
