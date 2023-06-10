from fastapi import APIRouter, Security
from sqlalchemy.orm import Session
from fastapi.security import  HTTPBearer
import cloudinary
import cloudinary.uploader
from database.models import Image
from configure.config import settings


router = APIRouter(prefix='/cloudinary', tags=["cloudinary"])
security = HTTPBearer()


@router.patch('/{image_id}')
async def cloudinary_set(file: UploadFile = File(), image: Image, db: Session = Depends(get_db)):
    cloudinary.config(
        cloud_name=settings.cloudinary_name,
        api_key=settings.cloudinary_api_key,
        api_secret=settings.cloudinary_api_secret,
        secure=True
    )
    r = cloudinary.uploader.upload(file.file, public_id=f'UsersPhoto/{image.user_id}', overwrite=True)
    src_url = cloudinary.CloudinaryImage(f'UsersPhoto/{image.user_id}') \
        .build_url(width=250, height=250, crop='fill', version=r.get('version'))
    image.picture = src_url
    db.commit()

@router.patch("/{image_id}/cropped")
async def cloudinary_cropped(image: Image, height: int, width: int, db: Session = Depends(get_db)):
    cloudinary.config(
        cloud_name=settings.cloudinary_name,
        api_key=settings.cloudinary_api_key,
        api_secret=settings.cloudinary_api_secret,
        secure=True
    )
    new_url = cloudinary.CloudinaryImage("sample.jpg").image(transformation=[{'height': height, 'width': width, 'crop': "fill"}])
    image.picture = new_url
    db.commit()


@router.patch("/{image_id}/scaled")
async def cloudinary_scaled(image: Image, crop: str, blur: int, db: Session = Depends(get_db)):
    cloudinary.config(
        cloud_name=settings.cloudinary_name,
        api_key=settings.cloudinary_api_key,
        api_secret=settings.cloudinary_api_secret,
        secure=True
    )
    new_url = cloudinary.CloudinaryImage("sample.jpg").image(transformation=[{'crop': crop},{'effect': f"blur:{blur}"}])
    image.picture = new_url
    db.commit()

@router.patch("/{image_id}/zoom")
async def cloudinary_zoom(image: Image, zoom: float, db: Session = Depends(get_db)):
    cloudinary.config(
        cloud_name=settings.cloudinary_name,
        api_key=settings.cloudinary_api_key,
        api_secret=settings.cloudinary_api_secret,
        secure=True
    )
    new_url = cloudinary.CloudinaryImage("sample.jpg").image(transformation=[{'zoom': zoom}])
    image.picture = new_url
    db.commit()


#

@router.patch("/{image_id}/radius")
async def cloudinary_radius(image: Image, db: Session = Depends(get_db)):
    cloudinary.config(
        cloud_name=settings.cloudinary_name,
        api_key=settings.cloudinary_api_key,
        api_secret=settings.cloudinary_api_secret,
        secure=True
    )
    new_url = cloudinary.CloudinaryImage("sample.jpg").image(transformation=[{'radius': "max"}])
    image.picture = new_url
    db.commit()