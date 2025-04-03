from fastapi import FastAPI, HTTPException,Query
from fastapi.responses import JSONResponse

from typing import List
from datetime import datetime
from db import DB
from order import Order
from enum import Enum
from delivery import CreateDeliveries
from staff import Staff
# Enum to restrict dormitory to "A" or "B"
class Dormitory(str, Enum):
    A = "A"
    B = "B"

class App:
    def __init__(self):
        self.app = FastAPI()
        self.db = DB()  # Sử dụng singleton DB
        self.setup_routes()

    def setup_routes(self):
        @self.app.get("/group-orders")
        def group_orders(timeslot: str = Query(..., description="The delivery timeslot"), dormitory: Dormitory  = Query(..., description="The dormitory name")):
            try:
                # Xử lý API gom nhóm đơn hàng theo timeslot
                orders = Order.get_orders_by_delivery_date(self.db, timeslot, dormitory)
                if not orders:
                    return JSONResponse(
                        status_code=404,
                        content={
                            "code": "NO_ORDERS",
                            "message": "Không có đơn hàng nào trong timeslot này!"
                        }
                    )
                # Convert orders to a list of dictionaries
                orders_dict = [order.__dict__ for order in orders]

                #Get num of available shipper
                num_of_shippers = Staff.get_total_available_staff(self.db)

                deliveries,delay_orders = CreateDeliveries(orders=orders_dict, dormitory = dormitory,num_of_shippers=num_of_shippers).get_delivery()
                return {"deliveries": deliveries, "delayed":delay_orders}
            except Exception as e:
                print(str(e))

                return JSONResponse(
                        status_code=500,
                        content={
                            "code": "INTERNAL_SERVER_ERROR",
                            "message": "Hệ thống đang gặp sự cố. Vui lòng thử lại sau!"
                        }
                    )

# Khởi tạo app FastAPI
app_instance = App()
app = app_instance.app
