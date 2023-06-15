import cloudinary
from pydantic import BaseSettings


class Settings(BaseSettings):
    sqlalchemy_database_url: str
    cloudinary_name = "cloud_name"
    cloudinary_api_key = "0000000000"
    cloudinary_api_secret = "secret"

    class Config:
        env_file = '.env'
        env_file_encoding = 'utf-8'


settings = Settings()


def config_cloudinary():
    return cloudinary.config(
        cloud_name=settings.cloudinary_name,
        api_key=settings.cloudinary_api_key,
        api_secret=settings.cloudinary_api_secret,
        secure=True
    )
