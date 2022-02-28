from multiprocessing import Condition, Lock, Process, Queue, Semaphore

from src.consumer import consumer
from src.producer import producer

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
