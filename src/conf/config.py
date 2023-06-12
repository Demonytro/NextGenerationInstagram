from pydantic import BaseSettings


class Settings(BaseSettings):
    sqlalchemy_database_url='postgresql+psycopg2://iqcqncxp:rnqklDxfeX7Z1MbT3QxAZYLDUWBsM-0z@lucky.db.elephantsql.com/iqcqncxp'

    cloud_name = "cloud_name"
    cloud_api_key = "0000000000"
    cloud_api_secret = "secret"

    class Config:
        env_file = '.env'
        env_file_encoding = 'utf-8'


settings = Settings()
