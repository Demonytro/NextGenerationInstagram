import configparser
import pathlib

from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine
from configure.config import settings

SQLALCHEMY_DATABASE_URL = settings.sqlalchemy_database_url

engine = create_engine(SQLALCHEMY_DATABASE_URL, echo = True)
DBSession = sessionmaker(autocommit= False, autoflush=False, bind=engine)

Base = declarative_base()

def get_db():
    session = DBSession()
    try:
        yield session
    finally:
        session.close()
