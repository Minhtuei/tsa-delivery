from typing import List


class Order:
    def __init__(
        self,
        id,
        shippingFee,
        studentId,
        checkCode,
        weight,
        building,
        deliveryDate,
        dormitory,
        phone,
        product,
        room,
        brand,
    ):
        self.id = id
        self.shippingFee = shippingFee
        self.studentId = studentId
        self.checkCode = checkCode
        self.weight = weight
        self.building = building
        self.deliveryDate = deliveryDate
        self.dormitory = dormitory
        self.phone = phone
        self.product = product
        self.room = room
        self.brand = brand

    @classmethod
    def from_db_row(cls, row):
        # Map dữ liệu từ DB row vào đối tượng Order
        return cls(
            id=row[0],
            shippingFee=row[1],
            studentId=row[2],
            checkCode=row[3],
            weight=row[4],
            building=row[8],
            deliveryDate=row[9],
            dormitory=row[10],
            phone=row[11],
            product=row[12],
            room=row[13],
            brand=row[15],
        )

    @staticmethod
    def get_orders_by_delivery_date(
        db, delivery_date: str, dormitory: str
    ) -> List["Order"]:
        # Truy xuất đơn hàng từ DB
        conn = db.get_connection()
        cur = conn.cursor()
        query = """SELECT * FROM "Order" WHERE "deliveryDate" = %s AND "latestStatus" = 'ACCEPTED' AND "dormitory" = %s"""
        cur.execute(query, (delivery_date, dormitory))
        rows = cur.fetchall()

        orders = [Order.from_db_row(row) for row in rows]

        db.close_connection(conn, cur)

        return orders
