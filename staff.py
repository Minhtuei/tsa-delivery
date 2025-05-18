from enum import Enum

from sqlalchemy import select
from sqlmodel import Field, Session, SQLModel


class UserStatus(str, Enum):
    AVAILABLE = "AVAILABLE"
    BUSY = "BUSY"


class UserRole(str, Enum):
    STUDENT = "STUDENT"
    STAFF = "STAFF"
    ADMIN = "ADMIN"


class StaffRepository(SQLModel, table=True):
    __tablename__ = "User"
    id: str = Field(primary_key=True, default=None)
    status: UserStatus
    role: UserRole

    @classmethod
    def get_total_available_staff(cls, session: Session) -> int:
        """Retrieve total number of available staff."""
        statement = select(cls).where(
            (cls.status == UserStatus.AVAILABLE) & (cls.role == UserRole.STAFF)
        )
        result = session.exec(statement).all()
        return len(result)
