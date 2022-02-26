from dotenv import load_dotenv
import os
import datetime


# Load environment variables
load_dotenv()


class BaseConfig(object):
    JWT_ERROR_MESSAGE_KEY = os.getenv("JWT_ERROR_MESSAGE_KEY")
    JWT_SECRET_KEY = os.getenv("JWT_SECRET_KEY")
    SQLALCHEMY_DATABASE_URI = os.getenv("DATABASE_URL")
    SQLALCHEMY_TRACK_MODIFICATIONS = False


class DevelopmentConfig(BaseConfig):
    JWT_ACCESS_TOKEN_EXPIRES = datetime.timedelta(minutes=1)


class ProductionConfig(BaseConfig):
    JWT_ACCESS_TOKEN_EXPIRES = datetime.timedelta(hours=3)


if ProductionConfig.SQLALCHEMY_DATABASE_URI.startswith("postgres://"):
    ProductionConfig.SQLALCHEMY_DATABASE_URI = (
        ProductionConfig.SQLALCHEMY_DATABASE_URI.replace(
            "postgres://", "postgresql://", 1
        )
    )


config_dict = {"development": DevelopmentConfig, "production": ProductionConfig}
