import json
import queue
import multiprocessing

import requests
import threading

base_url = 'https://dummyjson.com/products'


def send_request_and_store_data(url, result_queue):
    response = requests.get(url)
    data = response.json()

    result_queue.put(data)


def worker(process_num, result_queue):
    threads = []

    for i in range(process_num * 20, (process_num + 1) * 20):
        url = f"{base_url}/{i}"
        thread = threading.Thread(target=send_request_and_store_data, args=(url, result_queue))
        thread.start()
        threads.append(thread)

    for thread in threads:
        thread.join()


if __name__ == "__main__":
    manager = multiprocessing.Manager()
    result_queue = manager.Queue()
    file_lock = threading.Lock()

    processes = []

    for i in range(5):
        process = multiprocessing.Process(target=worker, args=(i, result_queue))
        process.start()
        processes.append(process)

    for process in processes:
        process.join()

    all_data = []
    while not result_queue.empty():
        all_data.append(result_queue.get())

    with file_lock:
        with open("data.json", "w") as json_file:
            json.dump(all_data, json_file, indent=2)