from datetime import datetime
from pydantic import BaseModel, Field
from src.database.models import UserRole

class UserModel(BaseModel):
    username: str = Field(min_length=5, max_length=16)
    email: str
    password: str = Field(min_length=6, max_length=10)
    role: UserRole = UserRole.USER

class UserDb(BaseModel):
    id: int
    username: str
    email: str
    created_at: datetime
    role: UserRole = UserRole.USER
    avatar: str

    class Config:
        orm_mode = True


class UserResponse(BaseModel):
    user: UserDb
    detail: str = "User successfully created"


class TokenModel(BaseModel):
    access_token: str
    refresh_token: str
    token_type: str = "bearer"