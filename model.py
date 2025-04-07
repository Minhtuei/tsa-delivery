from typing import List, Literal, Optional

from pydantic import BaseModel, Field


class OrderSchema(BaseModel):
    """Schema to serialize Order for API response"""

    id: str
    studentId: Optional[str]
    shippingFee: Optional[float]
    deliveryDate: Optional[str]
    isPaid: bool
    room: Optional[str]
    dormitory: Optional[str]
    building: Optional[str]
    checkCode: str
    product: Optional[str]
    weight: Optional[float]
    shipperId: Optional[str]
    phone: Optional[str]
    latestStatus: Optional[str]
    brand: Optional[str]
    remainingAmount: Optional[float]
    finishedImage: Optional[str]

    class Config:
        from_attributes = True  # Enables ORM serialization


class SortOrderSchema(BaseModel):
    """Schema to serialize sort Order information for API response"""

    id: str
    room: str
    building: str
    dormitory: str


class GroupOrdersRequest(BaseModel):
    maxWeight: Optional[float] = Field(default=None, gt=0)
    dormitory: Literal["A", "B"]
    timeslot: str  # Unix timestamp
    mode: Optional[Literal["free", "balanced"]] = Field(default=None)  # Sorting mode


class GroupOrdersResponse(BaseModel):
    deliveries: List[List[OrderSchema]]
    delayed: List[OrderSchema]


class SortOrderRequest(BaseModel):
    orders: List[SortOrderSchema]


class SortOrderResponse(BaseModel):
    orders: List[SortOrderSchema]
