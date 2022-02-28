import os
import time
from multiprocessing import Condition, Lock, Process, Queue, Semaphore


def producer(q: Queue, producer_cond: Condition, consumer_cond: Condition):
    while True:
        print("Producing")
        for i in range(100):
            q.put(i)

        with consumer_cond:
            consumer_cond.notify_all()
        with producer_cond:
            print("Producer waiting")
            producer_cond.wait()


def consumer(
    q: Queue, producer_cond: Condition, consumer_cond: Condition, notify_lock: Lock
):
    time.sleep(1)

    while True:
        with read_lock:
            if q.qsize() > 100:
                print(q.qsize())
                break

            if q.qsize() != 0:
                value = q.get()
                time.sleep(0.1)
            else:
                print(f"{os.getpid()} waiting to notify")

                with consumer_cond:
                    with producer_cond:
                        producer_cond.notify()
                    consumer_cond.wait()

        print(f"{os.getpid()} => consuming: {value} => Size: {q.qsize()}")


if __name__ == "__main__":
    q = Queue()
    producer_cond = Condition()
    consumer_cond = Condition()
    read_lock = Lock()

    producer = Process(target=producer, args=(q, producer_cond, consumer_cond))

    consumers = [
        Process(
            target=(consumer),
            args=(q, producer_cond, consumer_cond, read_lock),
        )
        for i in range(5)
    ]

    producer.start()

    for c in consumers:
        c.start()

    producer.join()
    for c in consumers:
        c.join()
