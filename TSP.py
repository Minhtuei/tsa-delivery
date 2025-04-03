import heapq

from ortools.constraint_solver import pywrapcp, routing_enums_pb2


class TSPSolver:
    def __init__(self, orders, start_location, map_box_distance):
        self.start_location = start_location
        self.orders = [start_location] + orders
        self.memo = {}
        self.map_box_distance = map_box_distance
        self.distance_matrix = self.create_distance_matrix()

    def get_distance(self, order1, order2, alpha=1.0, beta=100.0):
        """Tính khoảng cách giữa 2 điểm"""
        from_building = order1["building"]
        to_building = order2["building"]
        if from_building != to_building:
            distance = distance = next(
                (
                    d
                    for d in self.map_box_distance
                    if d["from"] == from_building and d["to"] == to_building
                ),
                None,
            )
            horizontal_distance = distance["distance"] if distance else 0.0
            vertical_distance = (
                abs(int(order1["room"][0]) + int(order2["room"][0])) * alpha
            )
        else:
            horizontal_distance = 0.0
            vertical_distance = (
                abs(int(order1["room"][0]) - int(order2["room"][0])) * alpha
            )
        # Ortools yêu cầu khoảng cách là số nguyên
        return int((horizontal_distance + vertical_distance) * beta)

    def create_distance_matrix(self):
        n = len(self.orders)
        distance_matrix = [[0.0] * n for _ in range(n)]

        # Tính khoảng cách giữa các điểm cần đi qua
        for i in range(n):
            for j in range(n):
                if i != j:
                    distance_matrix[i][j] = self.get_distance(
                        self.orders[i], self.orders[j]
                    )
        return distance_matrix

    def tsp_dp(self, mask, last):
        """Dynamic Programming (Held-Karp algorithm)"""
        if mask == (1 << (len(self.orders))) - 1:  # Đã sửa lỗi toán tử bit
            return self.distance_matrix[last][0]  # Quay về điểm xuất phát

        if (mask, last) in self.memo:
            return self.memo[(mask, last)]

        ans = float("inf")
        for i in range(1, len(self.orders)):
            if (mask & (1 << i)) == 0:  # Kiểm tra nếu chưa đi qua điểm i
                new_mask = mask | (1 << i)  # Đánh dấu điểm i đã đi qua
                ans = min(ans, self.distance_matrix[last][i] + self.tsp_dp(new_mask, i))

        self.memo[(mask, last)] = ans
        return ans

    def tsp_branch_and_bound_dp(self):
        n = len(self.orders)
        pq = []
        heapq.heappush(pq, (0, [0], 1 << 0))  # (cost, path, mask)

        best_cost = float("inf")
        best_path = []

        while pq:
            cost, path, mask = heapq.heappop(pq)
            if len(path) == n:
                total_cost = cost + self.distance_matrix[path[-1]][0]
                if total_cost < best_cost:
                    best_cost = total_cost
                    best_path = path
                continue
            for i in range(1, n):
                if not (mask & (1 << i)):
                    new_mask = mask | (1 << i)
                    new_cost = cost + self.distance_matrix[path[-1]][i]

                    estimated_cost = new_cost + self.tsp_dp(new_mask, i)
                    if estimated_cost < best_cost:
                        heapq.heappush(pq, (new_cost, path + [i], new_mask))

        return best_cost, best_path

    # def get_sorted_orders_by_TSP(self):
    #     """Trả về danh sách đơn hàng theo thứ tự tối ưu"""
    #     best_cost, best_path = self.tsp_branch_and_bound_dp()
    #     print(best_cost)
    #     return [ self.orders[i] for i in best_path[1:]], best_cost

    def tsp_ortool(self):
        data = {"distance_matrix": self.distance_matrix, "num_shippers": 1, "depot": 0}
        manager = pywrapcp.RoutingIndexManager(
            len(data["distance_matrix"]), data["num_shippers"], data["depot"]
        )
        routing = pywrapcp.RoutingModel(manager)

        def distance_callback(from_index, to_index):
            from_node = manager.IndexToNode(from_index)
            to_node = manager.IndexToNode(to_index)
            return data["distance_matrix"][from_node][to_node]

        transit_callback_index = routing.RegisterTransitCallback(distance_callback)
        routing.SetArcCostEvaluatorOfAllVehicles(transit_callback_index)
        search_parameters = pywrapcp.DefaultRoutingSearchParameters()
        search_parameters.first_solution_strategy = (
            routing_enums_pb2.FirstSolutionStrategy.PATH_CHEAPEST_ARC
        )
        solution = routing.SolveWithParameters(search_parameters)
        index = routing.Start(0)
        path = []
        while not routing.IsEnd(index):
            path.append(manager.IndexToNode(index))
            index = solution.Value(routing.NextVar(index))
        total_cost = solution.ObjectiveValue()
        print(total_cost)
        return [self.orders[i] for i in path[1:]], total_cost

    def get_sorted_orders_by_TSP(self):
        """Trả về danh sách đơn hàng theo thứ tự tối ưu"""
        return self.tsp_ortool()
