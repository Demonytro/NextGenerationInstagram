from pydantic import BaseModel, EmailStr, PastDate, Field, FutureDate
from datetime import datetime, date
from typing import Optional

class ImageResponseCloudinaryModel(BaseModel):
    id: int
    picture: str
    is_active: bool
    created_at: datetime
    update_at: datetime
    user_id: int