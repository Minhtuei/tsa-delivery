from enum import Enum

from sqlalchemy import select
from sqlmodel import Field, Session, SQLModel


class StaffStatus(str, Enum):
    AVAILABLE = "AVAILABLE"
    BUSY = "BUSY"
    OFFLINE = "OFFLINE"


class Staff(SQLModel, table=True):
    __tablename__ = "Staff"
    staffId: str = Field(primary_key=True, default=None)
    status: StaffStatus

    @classmethod
    def get_total_available_staff(cls, session: Session) -> int:
        """Retrieve total number of available staff."""
        statement = select(cls).where(cls.status == StaffStatus.AVAILABLE)
        result = session.exec(statement).all()
        return len(result)
