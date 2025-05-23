import os

from dotenv import load_dotenv
from pydantic import PostgresDsn
from pydantic_core import MultiHostUrl

# Tải biến môi trường từ file .env
load_dotenv()


class Settings:
    DB_HOST = os.getenv("DB_HOST")
    DB_NAME = os.getenv("DB_NAME")
    DB_USER = os.getenv("DB_USER")
    DB_PASSWORD = os.getenv("DB_PASSWORD")
    DB_PORT = os.getenv("DB_PORT")
    DB_SCHEMA = os.getenv("DB_SCHEMA")
    SECRET_KEY = "your_secret_key"  # Change this to a strong secret key
    ACCESS_TOKEN_EXPIRE_MINUTES = 30  # minute
    ALGORITHM = "HS256"  # Encryption algorithm

    @property
    def SQLALCHEMY_DATABASE_URI(self) -> PostgresDsn:
        return MultiHostUrl.build(
            scheme=self.DB_SCHEMA,
            username=self.DB_USER,
            password=self.DB_PASSWORD,
            host=self.DB_HOST,
            port=int(self.DB_PORT),
            path=self.DB_NAME,
        )


settings = Settings()
