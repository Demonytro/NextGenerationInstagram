import cloudinary.uploader
from typing import List

from fastapi import APIRouter, HTTPException, Depends, Query, UploadFile, File
from sqlalchemy.orm import Session
from starlette import status

from schemas import ImageResponse, ImageUpdateDescriptionRequest, ImageUpdateTagsRequest
from src.conf.config import settings
from src.database.db import get_db
from src.database.models import Image, Tag

router = APIRouter(prefix="/images", tags=["images"])


def config():
    return cloudinary.config(
        cloud_name=settings.cloudinary_name,
        api_key=settings.cloudinary_api_key,
        api_secret=settings.cloudinary_api_secret,
        secure=True
    )


@router.post("/", response_model=ImageResponse)
async def create_image(image: UploadFile = File(...), description: str = None, tags: List[str] = [],
                       db: Session = Depends(get_db)):
    try:
        config()
        uploaded_image = cloudinary.uploader.upload(image.file)

        image_url = uploaded_image['secure_url']

        image = Image(image=image_url, description=description)

        for tag_data in tags:
            tag = db.query(Tag).filter_by(name=tag_data).first()
            if not tag:
                tag = Tag(name=tag_data)
                db.add(tag)
            image.tags.append(tag)

        db.add(image)
        db.commit()
        db.refresh(image)

        return ImageResponse(
            id=image.id,
            image=image.image,
            description=image.description,
            tags=tags
        )
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))


@router.delete("/{image_id}")
async def delete_image(image_id: int, db: Session = Depends(get_db)):
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
async def update_image_image(image_id: int, image_data: UploadFile = File(...), db: Session = Depends(get_db)):
    try:
        config()

        image = db.query(Image).filter(Image.id == image_id).first()
        if not image:
            raise HTTPException(status_code=404, detail="Image not found")

        public_id = f"UsersPhoto/{image.id}"
        cloudinary.uploader.destroy(public_id)

        uploaded_image = cloudinary.uploader.upload(image_data.file, public_id=public_id)

        image_url = uploaded_image['secure_url']

        image.image = image_url

        db.commit()

        return ImageResponse(
            id=image.id,
            image=image.image,
            description=image.description,
            tags=[tag.name for tag in image.tags],
            comments=[comment.content for comment in image.comments]
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.put("/{image_id}/update-tags", response_model=ImageResponse)
async def update_image_tags(
        image_id: int,
        tags: List[str] = Query(..., description="List of tags to update for the image"),
        db: Session = Depends(get_db)
):
    try:
        image = db.query(Image).filter(Image.id == image_id).first()
        if not image:
            raise HTTPException(status_code=404, detail="Image not found")

        image.tags.clear()

        for tag_data in tags:
            tag = db.query(Tag).filter_by(name=tag_data).first()
            if not tag:
                tag = Tag(name=tag_data)
                db.add(tag)
            image.tags.append(tag)

        db.commit()
        db.refresh(image)

        return ImageResponse(
            id=image.id,
            image=image.image,
            description=image.description,
            tags=[tag.name for tag in image.tags],
            comments=[comment.content for comment in image.comments]
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.put("/{image_id}/update-description", response_model=ImageResponse)
async def update_image_description(image_id: int, description: ImageUpdateDescriptionRequest,
                                   db: Session = Depends(get_db)):
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
async def get_image(image_id: int, db: Session = Depends(get_db)):
    try:
        image = db.query(Image).filter(Image.id == image_id).first()
        if not image:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Image not found")

        return ImageResponse(
            id=image.id,
            image=image.image,
            description=image.description,
            tags=[tag.name for tag in image.tags],
            comments=[comment.content for comment in image.comments]
        )
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))


@router.get("/", response_model=List[ImageResponse])
async def get_images_by_tags(tags: List[str] = Query(...), db: Session = Depends(get_db)):
    try:
        images = db.query(Image).join(Image.tags).filter(Tag.name.in_(tags)).all()

        filtered_images = [image for image in images if set(tags).issubset({tag.name for tag in image.tags})]

        image_responses = []
        for image in filtered_images:
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
