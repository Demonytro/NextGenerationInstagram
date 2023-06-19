import cloudinary
from pydantic import BaseSettings


class Settings(BaseSettings):
    sqlalchemy_database_url: str
    #= "postgresql+psycopg2://postgres:567234@localhost:5432/postgres"
    cloudinary_name = "cloud_name"
    cloudinary_api_key = "0000000000"
    cloudinary_api_secret = "secret"

    jwt_secret_key: str = "secret"
    jwt_algorithm: str = "HS256"

    class Config:
        env_file = '.env'
        env_file_encoding = 'utf-8'


def config_cloudinary():
    return cloudinary.config(
        cloud_name=settings.cloudinary_name,
        api_key=settings.cloudinary_api_key,
        api_secret=settings.cloudinary_api_secret,
        secure=True
    )


settings = Settings()
