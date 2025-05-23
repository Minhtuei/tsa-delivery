# order.py
from enum import Enum
from typing import List, Optional

from sqlmodel import Field, Session, SQLModel, select

from model import OrderSchema


# Define Enum for OrderStatus
class OrderStatus(str, Enum):
    PENDING = "PENDING"
    ACCEPTED = "ACCEPTED"
    REJECTED = "REJECTED"
    DELIVERED = "DELIVERED"
    CANCELED = "CANCELED"
    IN_TRANSPORT = "IN_TRANSPORT"
    RECEIVED_EXTERNAL = "RECEIVED_EXTERNAL"


# Define Order model
class OrderRepository(SQLModel, table=True):
    __tablename__ = "Order"

    id: str = Field(primary_key=True, index=True)
    studentId: Optional[str] = None
    shippingFee: Optional[float] = None
    deliveryDate: Optional[str] = None
    isPaid: bool = Field(default=False)
    room: Optional[str] = None
    dormitory: Optional[str] = None
    building: Optional[str] = None
    checkCode: str
    product: Optional[str] = None
    weight: Optional[float] = None
    shipperId: Optional[str] = None
    phone: Optional[str] = None
    latestStatus: Optional[OrderStatus] = None
    brand: Optional[str] = None
    remainingAmount: Optional[float] = None
    finishedImage: Optional[str] = None

    @classmethod
    def get_orders_by_delivery_date(
        cls, session: Session, timeslot: str, dormitory: str
    ) -> List[OrderSchema]:
        """Retrieve orders by timeslot & dormitory, filtering only 'RECEIVED_EXTERNAL' orders."""
        print(timeslot)
        statement = select(cls).where(
            cls.deliveryDate == timeslot,
            cls.dormitory == dormitory,
            cls.latestStatus == OrderStatus.RECEIVED_EXTERNAL,
            cls.shipperId.is_(None),
        )
        return session.exec(statement).all()
