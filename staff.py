class Staff:
    def __init__(self, staff_id, status):
        self.staff_id = staff_id
        self.status = status

    @classmethod
    def from_db_row(cls, row):
        # Map dữ liệu từ DB row vào đối tượng Staff
        return cls(staff_id=row[0], status=row[1])

    @staticmethod
    def get_total_available_staff(db) -> int:
        conn = db.get_connection()
        cur = conn.cursor()
        query = """SELECT COUNT(*) FROM "Staff" WHERE "status" = 'AVAILABLE'"""
        cur.execute(query)
        total_available_staff = cur.fetchone()[0]
        db.close_connection(conn, cur)
        return total_available_staff
