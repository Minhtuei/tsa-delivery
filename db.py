from sqlmodel import Session, SQLModel, create_engine

from config import settings


class DB:
    _instance = None
    _engine = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance._init_engine()
        return cls._instance

    def _init_engine(self):
        """Initialize the database engine only once."""
        if not self._engine:
            self._engine = create_engine(
                str(settings.SQLALCHEMY_DATABASE_URI),
                # echo=True,  # Logs SQL queries for debugging
            )

    def get_session(self) -> Session:
        """Creates a new session; caller must close it after use."""
        return Session(self._engine)

    def init_db(self):
        """Creates tables if they don't exist."""
        SQLModel.metadata.create_all(self._engine)


# Usage example:
db = DB()
db.init_db()  # Ensure tables exist
