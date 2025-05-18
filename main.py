import csv
import json
import os

from delivery import OrderGroupingServiceTest

nums_of_orders = [5, 10, 30, 50, 70, 100, 200, 500, 1000]


def gen_data():
    for run_index in range(1, 11):  # Run 5 times
        for i in nums_of_orders:
            # Create new delivery with i orders
            delivery = OrderGroupingServiceTest(new_orders=True, nums_of_order=i)
            delivery.group_by_dormitory()
            data = delivery.group_by_time_slot()

            # Create output directory: data/time_{run_index}
            folder_path = f"data/time_{run_index}"
            os.makedirs(folder_path, exist_ok=True)

            # Save to corresponding JSON file
            file_path = os.path.join(
                folder_path, f"grouped_orders_by_timeslot_{i}.json"
            )
            with open(file_path, "w") as f:
                json.dump(data, f, indent=4)


def test_time():
    # Lưu thời gian chạy vào CSV

    csv_file = "results/test_runtime.csv"
    os.makedirs(os.path.dirname(csv_file), exist_ok=True)

    with open(csv_file, "w", newline="") as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(
            [
                "Lan chay",
                "So luong don hang",
                "Thoi gian (nn)",
                "Chi phi (nn)",
                "Thoi gian (tt)",
                "Chi phi (tt)",
            ]
        )

        for run_index in range(1, 11):  # Run 10 times
            for i in nums_of_orders:
                # Load input file đã sinh ra từ trước
                input_path = (
                    f"data/time_{run_index}/grouped_orders_by_timeslot_{i}.json"
                )
                with open(input_path, "r") as f:
                    data = json.load(f)

                # Gọi thuật toán test và đo thời gian chạy
                delivery = OrderGroupingServiceTest(
                    new_orders=True, nums_of_order=i, max_weight=20
                )
                (
                    random_time,
                    random_sort,
                    algorithm_time,
                    algorithm_sort,
                ) = delivery.test(data)

                writer.writerow(
                    [
                        run_index,
                        i,
                        round(random_time, 4),
                        random_sort,
                        round(algorithm_time, 4),
                        algorithm_sort,
                    ],
                )


def test_precise():
    csv_file = "results/test_precise.csv"
    os.makedirs(os.path.dirname(csv_file), exist_ok=True)

    with open(csv_file, "w", newline="") as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(
            [
                "Lan chay",
                "So luong don hang",
                "Thoi gian (held-karp)",
                "Chi phi (held-karp)",
                "Thoi gian (TSA)",
                "Chi phi (TSA)",
            ]
        )

        for run_index in range(1, 11):  # Run 10 times
            for i in range(1, 5):  # Số đơn từ 1 đến 11
                # Đọc dữ liệu đã lưu JSON
                file_path = (
                    f"data/precise_{run_index}/grouped_orders_by_timeslot_{i}.json"
                )
                with open(file_path, "r") as f:
                    grouped_data = json.load(f)

                # Tạo đối tượng xử lý (không tạo đơn hàng mới)
                delivery = OrderGroupingServiceTest(
                    new_orders=False, nums_of_order=i, max_weight=20000
                )

                # Gán dữ liệu đã load vào và test
                (
                    tsa_time,
                    tsa_cost,
                    held_karp_time,
                    held_karp_cost,
                ) = delivery.test_precise(grouped_data)

                # Ghi kết quả vào file CSV
                writer.writerow(
                    [
                        run_index,
                        i,
                        round(held_karp_time, 4),
                        held_karp_cost,
                        round(tsa_time, 4),
                        tsa_cost,
                        2,
                    ]
                )


# test_time()
test_precise()
