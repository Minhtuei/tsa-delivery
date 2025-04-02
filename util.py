import json
import random
from datetime import datetime

num_of_orders = 100
date_to_group = 14

buildings = [
   "A1", "A2", "A3", "A4", "A5", "A6", "A7", "A8",
   "A9", "A10", "A11", "A12", "A13", "A14", "A15", "A16",
   "A17", "A18", "A19", "A20", "AG3", "AG4", "AH1", "AH2",
   "BA1", "BA2", "BA3", "BA4", "BA5","BB1", "BB2", "BB3", 
   "BB5", "BC1", "BC2", "BC3", "BC4", "BC5", "BC6", "BD1",
    "BD2", "BD3", "BD4", "BD5", "BD6", "BE1", "BE2", "BE3", "BE4"
]
rooms = [
    "101", "102", "103", "104", "201", "202","203","204",
    "301", "302", "303", "304", "401", "402", "403", "404",
]

# Tạo trọng số cao hơn cho khoảng 0.1 - 2.0
low_weights = [round(random.uniform(0.1, 2.0), 2) for _ in range(5 * num_of_orders)] 
high_weights = [round(random.uniform(2.1, 5.0), 2) for _ in range(num_of_orders)]

# Kết hợp và chọn ngẫu nhiên
weights = random.choices(low_weights + high_weights, k=num_of_orders)

order_ids = [i for i in range(1, num_of_orders+1)]
hours = [f'{random.randint(7, 21)}:00' for i in range(num_of_orders)]
dates = [f'{random.randint(1, date_to_group)}/3/2025' for i in range(num_of_orders)]




def generate_orders() :
    orders = []
    for i in range(num_of_orders):
        order = {
            "order_id": order_ids[i],
            "building": random.choice(buildings),
            "room": random.choice(rooms),
            "weight": weights[i],
            "hour": hours[i],
            "date": dates[i]
        }
        orders.append(order)
    with open('orders.json', 'w') as f:
        json.dump(orders, f, indent=4)
    print('Orders generated successfully!')
    return orders

def get_coordinate_of_building(building: str, room: str) -> tuple:
    z = int(room[0])
    with open('coordinate.json') as f:
        coordinates = json.load(f)
    building_data = next((b for b in coordinates if b["building"] == building), None)
    if building_data:
        x, y  = building_data["value"][1], building_data["value"][0]
        return x, y, z
    else:
        return (0, 0, 0)
    
def get_mapbox_distance(from_buiding:str, to_building:str) -> float:
    with open('mapbox_distance.json') as f:
        distances = json.load(f)
    distance = next((d for d in distances if d["from"] == from_buiding and d["to"] == to_building), None)
    if distance:
        return distance["distance"]
    else:
        return 0.0