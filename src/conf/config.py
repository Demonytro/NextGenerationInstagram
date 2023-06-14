from pydantic import BaseSettings


class Settings(BaseSettings):
    sqlalchemy_database_url='postgresql+psycopg2://iqcqncxp:rnqklDxfeX7Z1MbT3QxAZYLDUWBsM-0z@lucky.db.elephantsql.com/iqcqncxp'

    cloud_name = 'dauzk4wq6'
    cloud_api_key = '537747638174553'
    cloud_api_secret = '27cPwALh3jLbhpU9AeEvwMPyBbE'


    class Config:
        env_file = '.env'
        env_file_encoding = 'utf-8'


settings = Settings()
