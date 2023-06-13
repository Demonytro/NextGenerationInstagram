from pydantic import BaseSettings


class Settings(BaseSettings):
    sqlalchemy_database_url: str

    cloud_name = "cloud_name"
    cloud_api_key = "0000000000"
    cloud_api_secret = "secret"


    class Config:
        env_file = '.env'
        env_file_encoding = 'utf-8'


settings = Settings()
