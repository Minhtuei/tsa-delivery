import json
import time

from BinPacking import BinPackingSolver
from TSP import TSPSolver
from util import generate_orders


class OrderGroupingServiceTest:
    def __init__(self, new_orders=False, max_weight=10.0, nums_of_order=10.0):
        self.orders = []
        self.grouped_order_by_dormitory = {}
        self.grouped_order_by_timeslot = {}
        self.grouped_orders_by_weight = {}
        self.sorted_orders_by_TSP = {}
        self.time_slots = [
            {"start": f"{i}:00", "end": f"{i + 1}:45"} for i in range(7, 21)
        ]
        self.max_weight = max_weight
        self.map_box_distance = {}
        with open("mapbox_distance.json") as f:
            self.map_box_distance = json.load(f)
        # self.load_orders(new_orders, nums_of_order)
        # self.group_by_dormitory()
        # self.group_by_time_slot()
        # self.group_by_weight()
        # self.sort_orders_by_TSP()

    def load_orders(self, new_orders=False, nums_of_order=10):
        if new_orders:
            self.orders = generate_orders(nums_of_order)
        else:
            with open("orders.json") as f:
                self.orders = json.load(f)

        print("Orders loaded successfully!")

    def get_start_location(self, dormitory):
        return (
            {"building": "A7", "room": "000", "weight": 0.0, "order_id": 0}
            if dormitory == "A"
            else {"building": "BD4", "room": "000", "weight": 0.0, "order_id": 0}
        )

    def group_by_dormitory(self):
        # start_time = time.time()
        for order in self.orders:
            if order["building"][0] not in self.grouped_order_by_dormitory:
                self.grouped_order_by_dormitory[order["building"][0]] = []
            self.grouped_order_by_dormitory[order["building"][0]].append(order)
        # print(f"Time elapsed for grouping by dormitory: {time.time() - start_time}")
        # print("Orders grouped by dormitory successfully!")

    def group_by_time_slot(self):
        # start_time = time.time()
        for dormitory, orders in self.grouped_order_by_dormitory.items():
            for order in orders:
                order_hour_str = order["hour"].split(":")[0]
                slot_name = None
                for time_slot in self.time_slots:
                    start = time_slot["start"].split(":")[0]
                    end = time_slot["end"].split(":")[0]
                    if start <= order_hour_str <= end:
                        slot_name = f'{time_slot["start"]} - {time_slot["end"]}'
                        break
                if slot_name:
                    self.grouped_order_by_timeslot.setdefault(dormitory, {}).setdefault(
                        order["date"], {}
                    ).setdefault(slot_name, []).append(order)
                else:
                    print(f'No slot found for order {order["order_id"]}')
        # print("Orders grouped by time slot successfully!")
        # print(f"Time elapsed for grouping by time slot: {time.time() - start_time}")
        # with open("grouped_orders_by_timeslot.json", "w") as f:
        #     json.dump(self.grouped_order_by_timeslot, f, indent=4)
        return self.grouped_order_by_timeslot

    def group_by_weight(self):
        start_time = time.time()
        for dormitory, dates in self.grouped_order_by_timeslot.items():
            for date_slots, time_slots in dates.items():
                for time_slots, orders in time_slots.items():
                    # solver = BinPackingSolver(orders, self.max_weight)
                    # trips = solver.solve_by_BFD()
                    trips = BinPackingSolver(orders, self.max_weight, 2).solve_by_BFD()
                    self.grouped_orders_by_weight.setdefault(dormitory, {}).setdefault(
                        date_slots, {}
                    ).setdefault(time_slots, []).extend(trips)
        # print("Orders grouped by weight successfully!")
        # print(f"Time elapsed for Bin Packing: {time.time() - start_time}")
        # with open("grouped_orders_by_weight.json", "w") as f:
        #     json.dump(self.grouped_orders_by_weight, f, indent=4)
        return time.time() - start_time, len(trips)

    def sort_orders_by_TSP(self):
        start_time = time.time()
        total_cost = 0
        for dormitory, dates in self.grouped_orders_by_weight.items():
            for date, time_slots_dict in dates.items():
                for time_slots, trips in time_slots_dict.items():
                    for trip in trips:
                        solver = TSPSolver(
                            trip,
                            self.get_start_location(dormitory),
                            self.map_box_distance,
                        )
                        sorted_trip, cost = solver.get_sorted_orders_by_TSP()
                        total_cost += cost
                        self.sorted_orders_by_TSP.setdefault(dormitory, {}).setdefault(
                            date, {}
                        ).setdefault(time_slots, []).append(sorted_trip)

        end_time = time.time()
        return end_time - start_time, total_cost
        # print("Orders sorted by TSP successfully!")
        # print(f"Time elapsed for TSP: {time.time() - start_time}")
        # with open("sorted_orders_by_TSP.json", "w") as f:
        #     json.dump(self.sorted_orders_by_TSP, f, indent=4)

    def group_by_weight_random(self):
        start_time = time.time()
        for dormitory, dates in self.grouped_order_by_timeslot.items():
            for date_slots, time_slots in dates.items():
                for time_slots, orders in time_slots.items():
                    # solver = BinPackingSolver(orders, self.max_weight)
                    # trips = solver.solve_by_BFD()
                    trips = BinPackingSolver(
                        orders, self.max_weight, 2
                    ).solve_by_random_fit_decreasing()
        # print("Orders grouped by weight successfully!")
        # print(f"Time elapsed for Bin Packing: {time.time() - start_time}")
        # with open("grouped_orders_by_weight.json", "w") as f:
        #     json.dump(self.grouped_orders_by_weight, f, indent=4)
        return time.time() - start_time, len(trips)

    def sort_orders_by_TSP_random(self):
        start_time = time.time()
        total_cost = 0
        for dormitory, dates in self.grouped_orders_by_weight.items():
            for date, time_slots_dict in dates.items():
                for time_slots, trips in time_slots_dict.items():
                    for trip in trips:
                        solver = TSPSolver(
                            trip,
                            self.get_start_location(dormitory),
                            self.map_box_distance,
                        )
                        _, cost = solver.get_random_order_and_cost()
                        total_cost += cost

        end_time = time.time()
        return end_time - start_time, total_cost

    def sort_orders_by_TSP_hk(self):
        start_time = time.time()
        total_cost = 0
        for dormitory, dates in self.grouped_orders_by_weight.items():
            for date, time_slots_dict in dates.items():
                for time_slots, trips in time_slots_dict.items():
                    for trip in trips:
                        solver = TSPSolver(
                            trip,
                            self.get_start_location(dormitory),
                            self.map_box_distance,
                        )
                        _, cost = solver.get_sorted_orders_by_TSP_hk()
                        total_cost += cost

        end_time = time.time()
        return end_time - start_time, total_cost

    def solve_tsp_for_trip(self, args):
        dormitory, date, time_slots, trip = args
        solver = TSPSolver(
            trip, self.get_start_location(dormitory), self.map_box_distance
        )
        sorted_trip, _ = solver.get_sorted_orders_by_TSP()
        return dormitory, date, time_slots, sorted_trip

    def test(self, data):
        self.grouped_order_by_timeslot = data
        bfd_group_time, algorithm_deli = self.group_by_weight()
        # random_group_time, random_deli = self.group_by_weight_random()
        tsp_sort_time, tsp_sort_cost = self.sort_orders_by_TSP()
        random_sort_time, random_sort_cost = self.sort_orders_by_TSP_random()
        return (
            bfd_group_time + random_sort_time,
            # random_deli,
            random_sort_cost,
            bfd_group_time + tsp_sort_time,
            # algorithm_deli,
            tsp_sort_cost,
        )

    def test_precise(self, data):
        self.grouped_order_by_timeslot = data
        bfd_group_time, algorithm_deli = self.group_by_weight()
        # random_group_time, random_deli = self.group_by_weight_random()
        tsp_sort_time, tsp_sort_cost = self.sort_orders_by_TSP()
        herd_karp_sort_time, herd_karp_sort_cost = self.sort_orders_by_TSP_hk()
        return (
            bfd_group_time + herd_karp_sort_time,
            # herd_karp_deli,
            herd_karp_sort_cost,
            bfd_group_time + tsp_sort_time,
            # algorithm_deli,
            tsp_sort_cost,
        )


class OrderGroupingService:
    def __init__(
        self,
        orders,
        dormitory,
        max_weight=20.0,
        num_of_shippers=1,
        mode="balanced",
        skip_group=False,
    ):
        self.orders = orders
        self.dormitory = dormitory
        self.max_weight = max_weight
        self.num_of_shippers = num_of_shippers
        self.mode = mode

        self.grouped_orders_by_weight = orders if skip_group else {}
        self.delay_orders = {}
        self.sorted_orders_by_TSP = []
        self.map_box_distance = {}
        with open("mapbox_distance.json") as f:
            self.map_box_distance = json.load(f)

        if not skip_group:
            self.group_by_weight()

        self.sort_orders_by_TSP()

    def get_start_location(self, dormitory):
        return (
            {
                "building": "A7",
                "room": "000",
                "weight": 0.0,
            }
            if dormitory == "A"
            else {
                "building": "BD4",
                "room": "000",
                "weight": 0.0,
            }
        )

    def group_by_weight(self):
        start_time = time.time()
        # Print orders as dictionaries
        if self.mode == "balanced":
            trips, delay_orders = BinPackingSolver(
                self.orders, self.max_weight, self.num_of_shippers
            ).solve_by_BFD_with_shippers()
            self.delay_orders = delay_orders

        else:
            trips = BinPackingSolver(
                self.orders, self.max_weight, self.num_of_shippers
            ).solve_by_BFD()

        filtered_trips = [trip for trip in trips if trip]
        self.grouped_orders_by_weight = filtered_trips
        print("Orders grouped by weight successfully!")
        print(f"Time elapsed for Bin Packing: {time.time() - start_time}")

    def sort_orders_by_TSP(self):
        start_time = time.time()
        for trip in self.grouped_orders_by_weight:
            solver = TSPSolver(
                trip, self.get_start_location(self.dormitory), self.map_box_distance
            )
            sorted_trip, _ = solver.get_sorted_orders_by_TSP()
            print(sorted_trip)
            self.sorted_orders_by_TSP.append(sorted_trip)

        print("Orders sorted by TSP successfully!")
        print(f"Time elapsed for TSP: {time.time() - start_time}")

    def get_delivery(self):
        return self.sorted_orders_by_TSP, self.delay_orders
