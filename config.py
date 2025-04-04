import os

from dotenv import load_dotenv

# Tải biến môi trường từ file .env
load_dotenv()


class Settings:
    DB_HOST = os.getenv("DB_HOST")
    DB_NAME = os.getenv("DB_NAME")
    DB_USER = os.getenv("DB_USER")
    DB_PASSWORD = os.getenv("DB_PASSWORD")
    DB_PORT = os.getenv("DB_PORT")
    SECRET_KEY = "your_secret_key"  # Change this to a strong secret key
    ACCESS_TOKEN_EXPIRE_MINUTES = 30  # minute
    ALGORITHM = "HS256"  # Encryption algorithm


settings = Settings()
