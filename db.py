import psycopg2

from config import settings


class DB:
    _instance = None  # Biến lớp để lưu đối tượng singleton

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)  # Tạo instance mới nếu chưa có
        return cls._instance

    def __init__(self):
        if not hasattr(self, "db_config"):
            # Chỉ thiết lập khi instance chưa được tạo (đảm bảo chỉ chạy 1 lần)
            self.db_config = {
                "host": settings.DB_HOST,
                "dbname": settings.DB_NAME,
                "user": settings.DB_USER,
                "password": settings.DB_PASSWORD,
                "port": settings.DB_PORT,
            }

    def get_connection(self):
        # Kết nối cơ sở dữ liệu
        return psycopg2.connect(**self.db_config)

    def close_connection(self, conn, cur):
        # Đóng kết nối và cursor
        cur.close()
        conn.close()
