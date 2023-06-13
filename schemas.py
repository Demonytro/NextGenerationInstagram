from datetime import datetime
from typing import List, Optional
from pydantic import BaseModel, Field


class ImageCreateRequest(BaseModel):
    image: str
    description: str = None
    tags: List[str] = []


class ImageUpdateRequest(BaseModel):
    description: str
    tags: List[str] = []


class ImageResponse(BaseModel):
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
