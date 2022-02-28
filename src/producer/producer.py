from multiprocessing import Condition, Queue

import numpy as np

from ..sample import BootstrapSample


def make_bootstrap_sample(X: np.ndarray, y: np.ndarray) -> BootstrapSample:
    boostrap_idx = np.random.choice(range(X.shape[0]), size=X.shape[0], replace=True)
    oob_idx = [i for i in range(X.shape[0]) if i not in boostrap_idx]
    return BootstrapSample(
        bootstrap_X=X[boostrap_idx],
        bootstrap_y=y[boostrap_idx],
        oob_X=X[oob_idx],
        oob_y=y[oob_idx],
    )


def producer(
    task_queue: Queue, producer_notifier: Condition, consumer_notifier: Condition
) -> None:
    while True:
        print("Producing")
        for i in range(100):
            task_queue.put(i)

        with consumer_notifier:
            consumer_notifier.notify_all()
        with producer_notifier:
            print("Producer waiting")
            producer_notifier.wait()
