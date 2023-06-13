# <<<<<<< Natali
# from pydantic import BaseModel, EmailStr, PastDate, Field, FutureDate
# from datetime import datetime, date
# from typing import Optional

# class ImageResponseCloudinaryModel(BaseModel):
#     id: int
#     image: str
#     is_active: bool
#     # created_at: datetime
#     # update_at: datetime
#     user_id: int

#     class Config():
#         orm_mode = True
# =======
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
# >>>>>>> dev
