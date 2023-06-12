from typing import List
from pydantic import BaseModel


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