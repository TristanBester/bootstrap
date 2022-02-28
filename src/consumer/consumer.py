import os
import time
from multiprocessing import Condition, Lock, Process, Queue, Semaphore


def consumer(
    q: Queue, producer_cond: Condition, consumer_cond: Condition, notify_lock: Lock
):
    time.sleep(1)

    while True:
        with notify_lock:
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
