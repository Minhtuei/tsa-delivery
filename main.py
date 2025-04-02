import time
from delivery import CreateDeliveries, CreateDeliveriesTest


if __name__ == '__main__':
    start_time = time.time()
    CreateDeliveriesTest(new_orders=False)
    print(f'Total time elapsed: {time.time() - start_time}')

