import os
import shutil
import threading
from queue import Queue
from tqdm import tqdm

SOURCE_DIR = "/path/to/A"
DEST_DIR = "/path/to/B"

NUM_WORKERS = min(64, (os.cpu_count() or 4) * 4)
QUEUE_SIZE = 10000


def fast_copy(src_path):
    rel_path = os.path.relpath(src_path, SOURCE_DIR)
    dst_path = os.path.join(DEST_DIR, rel_path)

    os.makedirs(os.path.dirname(dst_path), exist_ok=True)

    try:
        # copyfile dùng sendfile nếu OS hỗ trợ (nhanh hơn copyfileobj)
        shutil.copyfile(src_path, dst_path)
    except Exception:
        # fallback
        with open(src_path, 'rb') as fsrc, open(dst_path, 'wb') as fdst:
            shutil.copyfileobj(fsrc, fdst, length=1024 * 1024 * 8)


def worker(queue, pbar):
    while True:
        src = queue.get()
        if src is None:
            break
        fast_copy(src)
        pbar.update(1)
        queue.task_done()


def file_producer(queue):
    for root, _, files in os.walk(SOURCE_DIR):
        for f in files:
            if f.endswith(".wav"):
                queue.put(os.path.join(root, f))
    # gửi tín hiệu stop
    for _ in range(NUM_WORKERS):
        queue.put(None)


def count_files():
    count = 0
    for _, _, files in os.walk(SOURCE_DIR):
        for f in files:
            if f.endswith(".wav"):
                count += 1
    return count


def main():
    total_files = count_files()

    queue = Queue(maxsize=QUEUE_SIZE)

    with tqdm(total=total_files) as pbar:
        threads = []

        for _ in range(NUM_WORKERS):
            t = threading.Thread(target=worker, args=(queue, pbar))
            t.start()
            threads.append(t)

        file_producer(queue)

        queue.join()

        for t in threads:
            t.join()


if __name__ == "__main__":
    main()
