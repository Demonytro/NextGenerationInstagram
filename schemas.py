from typing import List

from fastapi import UploadFile
from pydantic import BaseModel, constr
from pydantic.types import conlist


class ImageCreateRequest(BaseModel):
    image: str
    description: str = None
    tags: conlist(constr(max_length=50), min_items=1, max_items=5) = []



class ImageUpdateRequest(BaseModel):
    description: str
# <<<<<<< Polina
    tags: List[str] = []


class ImageResponse(BaseModel):
    image: str
    description: str
    tags: List[str] = []
    comments: List[str] = []
# =======
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
# >>>>>>> dev
