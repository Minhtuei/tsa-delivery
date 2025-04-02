from typing import List

class Order:

    def __init__(self, order_id, shipping_fee, student_id, check_code, weight, building, delivery_date, dormitory, phone, product, room, brand):
        self.order_id = order_id
        self.shipping_fee = shipping_fee
        self.student_id = student_id
        self.check_code = check_code
        self.weight = weight
        self.building = building
        self.delivery_date = delivery_date
        self.dormitory = dormitory
        self.phone = phone
        self.product = product
        self.room = room
        self.brand = brand

    @classmethod
    def from_db_row(cls, row):
        # Map dữ liệu từ DB row vào đối tượng Order
        return cls(
            order_id=row[0],
            shipping_fee=row[1],
            student_id=row[2],
            check_code=row[3],
            weight=row[4],
            building=row[8],
            delivery_date=row[9],
            dormitory=row[10],
            phone=row[11],
            product=row[12],
            room=row[13],
            brand=row[15]
        )


    @staticmethod
    def get_orders_by_delivery_date(db, delivery_date: str,dormitory) -> List['Order']:
        # Truy xuất đơn hàng từ DB
        conn = db.get_connection()
        cur = conn.cursor()
        query = """SELECT * FROM "Order" WHERE "deliveryDate" = %s AND "latestStatus" = 'ACCEPTED' AND "dormitory" = %s"""
        cur.execute(query, (delivery_date,dormitory))
        rows = cur.fetchall()
        
        orders = [Order.from_db_row(row) for row in rows]
        
        db.close_connection(conn, cur)
        
        return orders
