from typing import List

from fastapi import UploadFile
from pydantic import BaseModel, constr
from pydantic.types import conlist


class ImageCreateRequest(BaseModel):
    description: str = None
    tags: conlist(constr(max_length=50), min_items=1, max_items=5) = []


class ImageUpdateRequest(BaseModel):
    description: str
    tags: conlist(constr(max_length=50), min_items=1, max_items=5) = []


class ImageUpdateImageRequest(BaseModel):
    image: UploadFile


class ImageUpdateTagsRequest(BaseModel):
    tags: conlist(constr(max_length=50), min_items=1, max_items=5) = []


class ImageUpdateDescriptionRequest(BaseModel):
    description: str


class ImageResponse(BaseModel):
    id: int
    image: str
    description: str
    tags: List[str] = []
    comments: List[str] = []


class ImageResponseCloudinaryModel(BaseModel):
    id: int
    image: str
    is_active: bool
    # created_at: datetime
    # update_at: datetime
    # user_id: int

    class Config():
        orm_mode = True
