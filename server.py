import time

from fastapi import Depends, FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from sqlmodel import Session

from db import db
from delivery import CreateDeliveries
from model import (
    GroupOrdersRequest,
    GroupOrdersResponse,
    SortOrderRequest,
    SortOrderResponse,
)
from order import Order
from staff import Staff


class App:
    def __init__(self):
        self.app = FastAPI()
        self.setup_routes()

    def setup_routes(self):
        @self.app.get("/")
        def root():
            return {"message": "Welcome to TSA-DELIVERY API!"}

        @self.app.get("/health-check")
        def health_check():
            uptime = time.time() - START_TIME  # Calculate uptime in seconds
            return {
                "status": "ok",
                "uptime_seconds": round(uptime, 2),  # Round for readability
            }

        @self.app.post("/group-orders")
        def group_orders(
            request: GroupOrdersRequest, session: Session = Depends(db.get_session)
        ) -> GroupOrdersResponse:
            try:
                # Fetch orders from DB
                orders = Order.get_orders_by_delivery_date(
                    session, request.timeslot, request.dormitory
                )
                if not orders:
                    return JSONResponse(
                        status_code=400,
                        content={
                            "code": "NO_ORDERS",
                            "message": "Không có đơn hàng nào trong timeslot này!",
                        },
                    )
                # Convert orders to a list of dictionaries
                orders_dict = [order.__dict__ for order in orders]

                # Handle optional data
                default_max_weight = request.maxWeight or 20.0
                default_mode = request.mode or "balanced"

                create_deliveries_config = {
                    "orders": orders_dict,
                    "dormitory": request.dormitory,
                    "max_weight": default_max_weight,
                    "mode": default_mode,
                }

                if default_mode == "balanced":
                    # Get num of available shipper
                    create_deliveries_config[
                        "num_of_shippers"
                    ] = Staff.get_total_available_staff(session)

                deliveries, delay_orders = CreateDeliveries(
                    **create_deliveries_config
                ).get_delivery()

                return GroupOrdersResponse(
                    deliveries=deliveries, delayed=delay_orders or []
                )
            except Exception as e:
                print(str(e))

                return JSONResponse(
                    status_code=500,
                    content={
                        "code": "INTERNAL_SERVER_ERROR",
                        "message": "Hệ thống đang gặp sự cố. Vui lòng thử lại sau!",
                    },
                )

        @self.app.post("/route-orders")
        def route_orders(request: SortOrderRequest) -> SortOrderResponse:
            orders = [order.model_dump() for order in request.orders]
            dormitories = set(order.dormitory for order in request.orders)
            if len(dormitories) > 1:
                return JSONResponse(
                    status_code=400,
                    content={
                        "code": "NOT_SAME_DORMITORY",
                        "message": "Các đơn hàng của bạn phải cùng thuộc một KTX",
                    },
                )

            deliveries, _ = CreateDeliveries(
                orders=[orders],
                dormitory=dormitories.pop(),
                skip_group=True,
                mode="free",
                num_of_shippers=1,
                max_weight=1000.0,
            ).get_delivery()
            return SortOrderResponse(orders=deliveries[0])


START_TIME = time.time()
# Khởi tạo app FastAPI
app_instance = App()
app = app_instance.app

allow_all = ["*"]
app.add_middleware(
    CORSMiddleware,
    allow_origins=allow_all,
    allow_credentials=True,
    allow_methods=allow_all,
    allow_headers=allow_all,
)
