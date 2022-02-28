import os
import time
from multiprocessing import Condition, Lock, Process, Queue, Semaphore
from multiprocessing.queues import Empty

# def produce(q, lock, cond):
#     while True:
#         q.put(1)
#         with cond:
#             cond.wait()


# def consume(q, lock, cond):
#     while True:
#         print(q.get_nowait())


#         with cond:
#             cond.notify()


# if __name__ == "__main__":
#     q = Queue()
#     lock = Lock()
#     cond = Condition()

#     p1 = Process(target=produce, args=(q, lock, cond))
#     p2 = Process(target=consume, args=(q, lock, cond))

#     p1.start()
#     p2.start()

#     p1.join()
#     p2.join()


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

    # while True:
    # try:
    #     value = q.get_nowait()
    # except Empty:
    #     with consumer_cond:
    #         if notify_lock.acquire():
    #             with producer_cond:
    #                 producer_cond.notify()
    #             consumer_cond.wait()
    #             notify_lock.release()
    #         else:
    #             consumer_cond.wait()
    #     continue

    # print(f"{os.getpid()} => consuming: {value} => Size: {q.qsize()}")
    # time.sleep(0.5)

    # with consumer_cond:
    #     consumer_cond.wait()

    while True:
        with read_lock:
            if q.qsize() > 100:
                print(q.qsize())
                break

            if q.qsize() != 0:
                value = q.get()
            else:
                print(f"{os.getpid()} waiting to notify")

                with consumer_cond:
                    with producer_cond:
                        producer_cond.notify()
                    consumer_cond.wait()

                # with producer_cond:
                #     producer_cond.notify()

                # with consumer_cond:
                #     print("Consumer Waiting")
                #     consumer_cond.wait()
                #     print(q.qsize())
                # print("Releasing read lock")

        print(f"{os.getpid()} => consuming: {value} => Size: {q.qsize()}")
        # time.sleep(0.1)


# # def produce(q: Queue, produce_mode: Condition, consume_mode: Condition):
# #     while True:
# #         with produce_mode:
# #             print()
# #             for i in range(1000):
# #                 q.put(i)
# #                 print(f"Adding {i}")
# #                 # time.sleep()
# #             print()
# #             with consume_mode:
# #                 print("Waking consumers")
# #                 time.sleep(3)
# #                 consume_mode.notify_all()
# #             produce_mode.wait()


# # def consume(q, producer_cond, consumer_cond, notify_lock: Lock, read_lock: Lock):
# #     with consumer_cond:
# #         print("Waiting...")
# #         consumer_cond.wait()

# #     print("Awake")

# #     while True:

# #         with read_lock:
# #             if not q.empty():
# #                 print(f"Consuming: {q.get()}")
# #             else:
# #                 # if notify_lock.acquire():
# #                 # This process is blocking while holding the read lock
# #                 # This prevents any other processes from entering the critical
# #                 # region until more things have been put into the queue
# #                 print("Notifying and waiting")
# #                 time.sleep(3)
# #                 with producer_cond:
# #                     producer_cond.notify()
# #                 with consumer_cond:
# #                     consumer_cond.wait()

# #         # try:
# #         #     print(q.qsize())
# #         #     v = q.get(block=False)
# #         #     print(f"Consuming: {v}")
# #         #     time.sleep(1)
# #         # except Empty:
# #         #     # if lock.acquire(block=False):
# #         #     #     print("Notifying consumer")
# #         #     #     with producer_cond:
# #         #     #         producer_cond.notify()
# #         #     # else:
# #         #     #     print("Lock already taken")
# #         #     print("Empty")
# #         #     break


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
