import json
import requests
from concurrent.futures import ThreadPoolExecutor, ProcessPoolExecutor
import multiprocessing

base_url = 'https://dummyjson.com/products'

def send_request_and_store_data(url, result_queue):
    response = requests.get(url)
    data = response.json()

    result_queue.put(data)

def process_worker(process_num, result_queue):
    urls = [f"{base_url}/{i}" for i in range(20 * process_num + 1, 20 * (process_num + 1) + 1)]

    with ThreadPoolExecutor(max_workers=5) as executor:
        for url in urls:
            executor.submit(send_request_and_store_data, url, result_queue)

if __name__ == "__main__":
    manager = multiprocessing.Manager()
    result_queue = manager.Queue()
    processes = []

    with ProcessPoolExecutor(max_workers=5) as executor:
        for i in range(5):
            processes.append(executor.submit(process_worker, i, result_queue))

    all_data = []
    for process in processes:
        process.result()

        while not result_queue.empty():
            all_data.append(result_queue.get())

    with open("data.json", "w") as json_file:
        json.dump(all_data, json_file, indent=2)