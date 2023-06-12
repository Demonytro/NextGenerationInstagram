from typing import List

from pydantic import BaseModel


class ImageCreateRequest(BaseModel):
    image: str
    description: str = None
    tags: List[str] = []


class ImageUpdateRequest(BaseModel):
    description: str
    tags: List[str] = []


class ImageUpdateImageRequest(BaseModel):
    image: str


class ImageUpdateTagsRequest(BaseModel):
    tags: List[str] = []


class ImageUpdateDescriptionRequest(BaseModel):
    description: str


class ImageResponse(BaseModel):
    image: str
    description: str
    tags: List[str] = []
    comments: List[str] = []


