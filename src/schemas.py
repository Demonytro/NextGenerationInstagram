from datetime import datetime, date
from pydantic import BaseModel, Field, constr, EmailStr
from src.database.models import UserRole, User
from typing import List, Optional
from fastapi import UploadFile
from pydantic.types import conlist


class ImageCreateRequest(BaseModel):
    image: str
    description: str = None
    tags: conlist(constr(max_length=50), min_items=1, max_items=5) = []


class ImageUpdateRequest(BaseModel):
    description: str
    tags: conlist(constr(max_length=50), min_items=1, max_items=5) = []


class ImageResponse(BaseModel):
    id: int
    image: str
    description: str
    tags: conlist(constr(max_length=50), min_items=1, max_items=5) = []
    comments: List[str] = []

    # возможно стоит тут добавить поле rating если да то и в search_filtering тоже
    class Config:
        orm_mode = True


class ImageUpdateImageRequest(BaseModel):
    image: UploadFile


class ImageUpdateTagsRequest(BaseModel):
    tags: conlist(constr(max_length=50), min_items=1, max_items=5) = []


class ImageUpdateDescriptionRequest(BaseModel):
    description: str


class CommentBase(BaseModel):
    text: str = Field(max_length=500)


class CommentModel(CommentBase):
    id: int
    created_at: datetime
    updated_at: Optional[datetime]
    user_id: int
    image_id: int
    update_status: bool = False

    class Config:
        orm_mode = True


class CommentUpdate(CommentModel):
    update_status: bool = True
    updated_at = datetime

    class Config:
        orm_mode = True


class ImageResponseCloudinaryModel(BaseModel):
    id: int
    image: str
    is_active: bool

    # created_at: datetime
    # update_at: datetime
    # user_id: int

    class Config():
        orm_mode = True


class UserModel(BaseModel):
    username: str = Field(min_length=5, max_length=16)
    email: EmailStr
    password: str = Field(min_length=6, max_length=10)
    role: UserRole = UserRole.USER


class UserResponse(BaseModel):
    id: int
    username: str
    email: EmailStr
    avatar: str
    role: UserRole
    detail: str = "User successfully created"

    class Config:
        orm_mode = True



class UserDb(BaseModel):
    id: int
    username: str
    email: str
    created_at: datetime
    role: UserRole = UserRole.USER
    avatar: str

    class Config:
        orm_mode = True


class TokenModel(BaseModel):
    access_token: str
    refresh_token: str
    token_type: str = "bearer"


class BlacklistTokenCreate(BaseModel):
    token: str


class UserProfileCreate(BaseModel):
    first_name: str
    last_name: str
    email: EmailStr
    phone: str
    date_of_birth: date


class UserProfileResponse(BaseModel):
    id: int
    user_id: int
    first_name: str
    last_name: str
    email: EmailStr
    phone: str
    date_of_birth: date

    class Config:
        orm_mode = True


class RatingRequestModel(BaseModel):
    numbers_rating: int
    text_rating: str
    user_id: int
    image_id: int


class RatingResponseModel(BaseModel):
    id: int
    numbers_rating: int
    text_rating: str
    user_id: int
    image_id: int
    created_at: datetime
    updated_at: Optional[datetime]

    class Config:
        orm_mode = True