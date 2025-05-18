import random


class BinPackingSolver:
    def __init__(self, orders, max_weight, num_of_shippers):
        self.orders = orders
        self.max_weight = max_weight
        self.num_of_shippers = num_of_shippers

    def solve_by_BFD(self):
        # Sắp xếp đơn hàng giảm dần theo trọng lượng
        sorted_orders = sorted(self.orders, key=lambda x: -x["weight"])

        # Danh sách các bin (mỗi bin là một list các đơn hàng)
        bins = []

        for order in sorted_orders:
            best_bin = None
            min_remaining = float("inf")  # Khởi tạo remaining space nhỏ nhất

            # Tìm bin tốt nhất để đặt đơn hàng này
            for bin in bins:
                current_weight = sum(item["weight"] for item in bin)
                remaining = self.max_weight - current_weight

                # Nếu bin có đủ chỗ và remaining space là nhỏ nhất
                if remaining >= order["weight"] and remaining < min_remaining:
                    best_bin = bin
                    min_remaining = remaining

            # Nếu tìm được bin phù hợp, thêm đơn hàng vào bin đó
            if best_bin:
                best_bin.append(order)
            else:
                # Nếu không tìm được bin phù hợp, tạo bin mới
                bins.append([order])
        return bins

    def solve_by_BFD_with_shippers(self):
        # Sắp xếp đơn hàng giảm dần theo trọng lượng
        sorted_orders = sorted(self.orders, key=lambda x: -x["weight"])

        # Khởi tạo danh sách các bin (mỗi shipper có một bin)
        bins = [[] for _ in range(self.num_of_shippers)]
        unsorted_orders = []

        # Gán đơn hàng theo thuật toán Best Fit Decreasing (BFD)
        for order in sorted_orders:
            best_shipper = None
            min_orders = float("inf")  # Dùng để cân bằng số lượng đơn hàng giữa shipper

            # Tìm shipper có ít đơn hàng nhất mà vẫn có thể nhận đơn
            for i in range(self.num_of_shippers):
                current_weight = sum(item["weight"] for item in bins[i])
                remaining_weight = self.max_weight - current_weight

                if remaining_weight >= order["weight"] and len(bins[i]) < min_orders:
                    best_shipper = i
                    min_orders = len(bins[i])

            # Nếu tìm được shipper phù hợp, thêm đơn hàng vào bin đó
            if best_shipper is not None:
                bins[best_shipper].append(order)
            else:
                # Nếu không có shipper nào chứa được đơn hàng này, đưa vào danh sách chưa xử lý
                unsorted_orders.append(order)

        # **Giai đoạn 2: Xếp lại đơn hàng chưa gán được**
        remaining_orders = []
        for order in unsorted_orders:
            best_shipper = None
            min_remaining_weight = float("inf")

            # Thử tìm shipper còn khoảng trống lớn nhất
            for i in range(self.num_of_shippers):
                current_weight = sum(item["weight"] for item in bins[i])
                remaining_weight = self.max_weight - current_weight

                if (
                    remaining_weight >= order["weight"]
                    and remaining_weight < min_remaining_weight
                ):
                    best_shipper = i
                    min_remaining_weight = remaining_weight

            # Nếu tìm được shipper có chỗ, gán đơn hàng vào đó
            if best_shipper is not None:
                bins[best_shipper].append(order)
            else:
                # Nếu không có shipper nào chứa được, đẩy sang time_slot tiếp theo
                remaining_orders.append(order)

        return bins, remaining_orders

    def solve_by_random_fit_decreasing(self):
        # Sắp xếp đơn hàng giảm dần theo trọng lượng
        sorted_orders = sorted(self.orders, key=lambda x: -x["weight"])

        bins = []

        for order in sorted_orders:
            # Tìm các bin còn đủ chỗ
            valid_bins = []
            for bin in bins:
                current_weight = sum(item["weight"] for item in bin)
                remaining = self.max_weight - current_weight
                if remaining >= order["weight"]:
                    valid_bins.append(bin)

            # Nếu có bin phù hợp → chọn ngẫu nhiên 1 bin để thêm
            if valid_bins:
                chosen_bin = random.choice(valid_bins)
                chosen_bin.append(order)
            else:
                # Nếu không có bin phù hợp, tạo bin mới
                bins.append([order])

        return bins
