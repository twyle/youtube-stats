"""This module declares the app configuration.

The classes include:

BaseConfig:
    Has all the configurations shared by all the environments.

"""
import os
from datetime import timedelta

from dotenv import load_dotenv

load_dotenv()


class BaseConfig:
    """Base configuration."""

    DEBUG = True
    TESTING = False
    SECRET_KEY = os.environ.get("SECRET_KEY", "df0331cefc6c2b9a5d0208a726a5d1c0fd37324feba25506")
    POSTGRES_HOST = os.environ["POSTGRES_HOST"]
    POSTGRES_DB = os.environ["POSTGRES_DB"]
    POSTGRES_PORT = os.environ["POSTGRES_PORT"]
    POSTGRES_USER = os.environ["POSTGRES_USER"]
    POSTGRES_PASSWORD = os.environ["POSTGRES_PASSWORD"]
    db_conn_string = f"postgresql://{POSTGRES_USER}:{POSTGRES_PASSWORD}@{POSTGRES_HOST}:{POSTGRES_PORT}/{POSTGRES_DB}"
    SQLALCHEMY_DATABASE_URI = db_conn_string
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    JWT_SECRET_KEY=os.environ['JWT_SECRET_KEY']
    JWT_ACCESS_TOKEN_EXPIRES = timedelta(hours=int(os.getenv("JWT_ACCESS_TOKEN_EXPIRES", "24")))
    JWT_REFRESH_TOKEN_EXPIRES = timedelta(days=int(os.getenv("JWT_REFRESH_TOKEN_EXPIRES", "7")))
    APP_INDEX=os.environ['APP_INDEX']
    ES_HOST=os.environ['ES_HOST']
    ES_PORT=os.environ['ES_PORT']


class DevelopmentConfig(BaseConfig):
    """Development confuguration."""

    DEBUG = True
    TESTING = False
    SECRET_KEY = os.environ.get("SECRET_KEY", "df0331cefc6c2b9a5d0208a726a5d1c0fd37324feba25506")
    

class TestingConfig(BaseConfig):
    """Testing configuration."""

    TESTING = True
    SECRET_KEY = 'secret-key'
    SQLALCHEMY_DATABASE_URI = 'sqlite:///'

class ProductionConfig(BaseConfig):
    """Production configuration."""

    TESTING = False


Config = {
    "development": DevelopmentConfig,
    "test": TestingConfig,
    "production": ProductionConfig,
    "staging": ProductionConfig,
}
