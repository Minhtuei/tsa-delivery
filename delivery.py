import json
from datetime import datetime
from util import generate_orders
from copy import deepcopy
import heapq
from TSP import TSPSolver
from BinPacking import BinPackingSolver
import time


class CreateDeliveriesTest:
    def __init__(self, new_orders=False, max_weight=10.0):
        self.orders = []
        self.grouped_order_by_dormitory = {}
        self.grouped_order_by_timeslot = {}
        self.grouped_orders_by_weight = {}
        self.sorted_orders_by_TSP = {}
        self.time_slots =  [{
                "start": f'{i}:00',
                "end": f'{i+1}:45'
            } for i in range(7,21)]
        self.max_weight = max_weight
        self.map_box_distance = {}
        self.load_orders(new_orders)
        self.group_by_dormitory()
        self.group_by_time_slot()
        self.group_by_weight()
        self.sort_orders_by_TSP()

    def load_orders(self, new_orders=False):
        with open('mapbox_distance.json') as f:
            self.map_box_distance = json.load(f)
        if new_orders:
            self.orders = generate_orders()
        else:
            # with open('orders.json') as f:
            #     self.orders = json.load(f)
            self.orders =[ {
                        "order_id": 749,
                        "building": "A10",
                        "room": "401",
                        "weight": 2.4,
                        "hour": "16:00",
                        "date": "5/3/2025"
                    },
                    {
                        "order_id": 771,
                        "building": "A6",
                        "room": "402",
                        "weight": 0.72,
                        "hour": "16:00",
                        "date": "5/3/2025"
                    },
                    {
                        "order_id": 950,
                        "building": "A6",
                        "room": "301",
                        "weight": 0.56,
                        "hour": "16:00",
                        "date": "5/3/2025"
                    },
                    {
                        "order_id": 237,
                        "building": "A5",
                        "room": "401",
                        "weight": 1.61,
                        "hour": "16:00",
                        "date": "5/3/2025"
                    },
                    {
                        "order_id": 587,
                        "building": "A13",
                        "room": "302",
                        "weight": 2.69,
                        "hour": "16:00",
                        "date": "5/3/2025"
                    },{
                        "order_id": 587,
                        "building": "AH1",
                        "room": "302",
                        "weight": 0.69,
                        "hour": "16:00",
                        "date": "5/3/2025"
                    },{
                        "order_id": 587,
                        "building": "AG3",
                        "room": "302",
                        "weight": 0.09,
                        "hour": "16:00",
                        "date": "5/3/2025"
                    },{
                        "order_id": 587,
                        "building": "A4",
                        "room": "302",
                        "weight": 0.09,
                        "hour": "16:00",
                        "date": "5/3/2025"
                    },{
                        "order_id": 587,
                        "building": "A20",
                        "room": "302",
                        "weight": 0.09,
                        "hour": "16:00",
                        "date": "5/3/2025"
                    },{
                        "order_id": 587,
                        "building": "A12",
                        "room": "402",
                        "weight": 0.09,
                        "hour": "16:00",
                        "date": "5/3/2025"
                    }]
        print('Orders loaded successfully!')

    def get_start_location(self, dormitory):
        return {
            'building': 'A7',
            'room': '000',
            'weight': 0.0,
            'order_id': 0
        } if dormitory == 'A' else {
            'building': 'BD4',
            'room': '000',
            'weight': 0.0,
            'order_id': 0
        }

    def group_by_dormitory(self):
        start_time = time.time()
        for order in self.orders:
            if order['building'][0] not in self.grouped_order_by_dormitory:
                self.grouped_order_by_dormitory[order['building'][0]] = []
            self.grouped_order_by_dormitory[order['building'][0]].append(order)
        print(f'Time elapsed for grouping by dormitory: {time.time() - start_time}')
        print('Orders grouped by dormitory successfully!')
    
    def group_by_time_slot(self):
        start_time = time.time()
        for dormitory, orders in self.grouped_order_by_dormitory.items():
            for order in orders:
                order_hour_str = order['hour'].split(':')[0]
                slot_name = None
                for time_slot in self.time_slots:
                    start = time_slot['start'].split(':')[0]
                    end = time_slot['end'].split(':')[0]
                    if start <= order_hour_str <= end:
                        slot_name = f'{time_slot["start"]} - {time_slot["end"]}'
                        break
                if slot_name:
                    self.grouped_order_by_timeslot.setdefault(dormitory, {}).setdefault(order['date'], {}).setdefault(slot_name, []).append(order)
                else:
                    print(f'No slot found for order {order["order_id"]}')
        print('Orders grouped by time slot successfully!')
        print(f'Time elapsed for grouping by time slot: {time.time() - start_time}')
        with open('grouped_orders_by_timeslot.json', 'w') as f:
            json.dump(self.grouped_order_by_timeslot, f, indent=4)

    

    def group_by_weight(self):
        start_time = time.time()
        for dormitory, dates in self.grouped_order_by_timeslot.items():
            for date_slots, time_slots in dates.items():
                for time_slots, orders in time_slots.items():
                    # solver = BinPackingSolver(orders, self.max_weight)
                    # trips = solver.solve_by_BFD()
                    trips,_ = BinPackingSolver(orders, self.max_weight,2).solve_by_BFD_with_shippers()
                    self.grouped_orders_by_weight.setdefault(dormitory, {}).setdefault(date_slots, {}).setdefault(time_slots, []).extend(trips)
        print('Orders grouped by weight successfully!')
        print(f'Time elapsed for Bin Packing: {time.time() - start_time}')
        with open('grouped_orders_by_weight.json', 'w') as f:
            json.dump(self.grouped_orders_by_weight, f, indent=4)


    def sort_orders_by_TSP(self):
        start_time = time.time()
        for dormitory, dates in self.grouped_orders_by_weight.items():
            for date, time_slots_dict in dates.items():
                for time_slots, trips in time_slots_dict.items():
                    for trip in trips:
                        solver = TSPSolver(trip, self.get_start_location(dormitory), self.map_box_distance)
                        sorted_trip, _ = solver.get_sorted_orders_by_TSP()
                        self.sorted_orders_by_TSP.setdefault(dormitory, {}).setdefault(date, {}).setdefault(time_slots, []).append(sorted_trip)

        print('Orders sorted by TSP successfully!')
        print(f'Time elapsed for TSP: {time.time() - start_time}')
        with open('sorted_orders_by_TSP.json', 'w') as f:
            json.dump(self.sorted_orders_by_TSP, f, indent=4)

    def solve_tsp_for_trip(self, args):
        dormitory, date, time_slots, trip = args
        solver = TSPSolver(trip, self.get_start_location(dormitory), self.map_box_distance)
        sorted_trip, _ = solver.get_sorted_orders_by_TSP()
        return dormitory, date, time_slots, sorted_trip


class CreateDeliveries:
    def __init__(self, orders,dormitory, max_weight=20.0, num_of_shippers=1):
        self.orders = orders
        self.dormitory = dormitory
        self.max_weight = max_weight
        self.num_of_shippers = num_of_shippers

        self.grouped_orders_by_weight = {}
        self.sorted_orders_by_TSP = []
        self.map_box_distance = {}

        self.group_by_weight()
        self.sort_orders_by_TSP()

    
    def get_start_location(self, dormitory):
        return {
            'building': 'A7',
            'room': '000',
            'weight': 0.0,
            'order_id': 0
        } if dormitory == 'A' else {
            'building': 'BD4',
            'room': '000',
            'weight': 0.0,
            'order_id': 0
        }

    
    

    def group_by_weight(self):
        start_time = time.time()
        # Print orders as dictionaries
        trips,_ = BinPackingSolver(self.orders, self.max_weight,self.num_of_shippers).solve_by_BFD_with_shippers()
        filtered_trips = [trip for trip in trips if trip]
        self.grouped_orders_by_weight = filtered_trips
        print('Orders grouped by weight successfully!')
        print(f'Time elapsed for Bin Packing: {time.time() - start_time}')
        


    def sort_orders_by_TSP(self):
        start_time = time.time()
        for trip in self.grouped_orders_by_weight:
            solver = TSPSolver(trip, self.get_start_location(self.dormitory), self.map_box_distance)
            sorted_trip, _ = solver.get_sorted_orders_by_TSP()
            print(sorted_trip)
            self.sorted_orders_by_TSP.append(sorted_trip)

        print('Orders sorted by TSP successfully!')
        print(f'Time elapsed for TSP: {time.time() - start_time}')

    def get_delivery(self):
        return self.sorted_orders_by_TSP
        
