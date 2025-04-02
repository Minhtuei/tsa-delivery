import psycopg2
import os
from dotenv import load_dotenv

# Tải biến môi trường từ file .env
load_dotenv()

class DB:
    _instance = None  # Biến lớp để lưu đối tượng singleton

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)  # Tạo instance mới nếu chưa có
        return cls._instance

    def __init__(self):
        if not hasattr(self, 'db_config'):
            # Chỉ thiết lập khi instance chưa được tạo (đảm bảo chỉ chạy 1 lần)
            self.db_config = {
                "host": os.getenv("DB_HOST"),
                "dbname": os.getenv("DB_NAME"),
                "user": os.getenv("DB_USER"),
                "password": os.getenv("DB_PASSWORD"),
                "port": os.getenv("DB_PORT")
            }

    def get_connection(self):
        # Kết nối cơ sở dữ liệu
        return psycopg2.connect(**self.db_config)

    def close_connection(self, conn, cur):
        # Đóng kết nối và cursor
        cur.close()
        conn.close()
