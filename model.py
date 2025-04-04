from typing import List, Literal, Optional

from pydantic import BaseModel, Field


class OrderType(BaseModel):
    id: str
    shippingFee: float | None
    studentId: str
    checkCode: str
    weight: float
    building: str
    deliveryDate: str
    dormitory: str
    phone: str | None
    product: str
    room: str
    brand: str


class GroupOrdersRequest(BaseModel):
    maxWeight: Optional[float] = Field(default=None, gt=0)
    dormitory: Literal["A", "B"]
    timeslot: str  # Unix timestamp
    mode: Optional[Literal["free", "balanced"]] = Field(default=None)  # Sorting mode


class GroupOrdersResponse(BaseModel):
    deliveries: List[List[OrderType]]
    delayed: List[OrderType]
