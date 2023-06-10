from pydantic import BaseSettings

class Settings(BaseSettings):
    sqlalchemy_database_url: str
    secret_key: str
    algorithm: str
    cloudinary_name: str
    cloudinary_api_key: str
    cloudinary_api_secret: str

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"


settings = Settings()