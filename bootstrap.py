from dataclasses import dataclass
from enum import Enum, auto

import numpy as np


class MetricInput(Enum):
    PREDICTIONS = auto()
    PROBABILITIES = auto()


@dataclass
class BootstrapSample:
    bootstrap_X: np.ndarray
    bootstrap_y: np.ndarray
    oob_X: np.ndarray
    oob_y: np.ndarray
    oob_preditions: np.ndarray = None
    oob_probabilities: np.ndarray = None


@dataclass
class MetricSet:
    metrics: list[callable]
    inputs: list[MetricInput]
    kwargs: list[dict] = None


def make_bootstrap_sample(X: np.ndarray, y: np.ndarray) -> BootstrapSample:
    boostrap_idx = np.random.choice(range(X.shape[0]), size=X.shape[0], replace=True)
    oob_idx = [i for i in range(X.shape[0]) if i not in boostrap_idx]
    return BootstrapSample(
        bootstrap_X=X[boostrap_idx],
        bootstrap_y=y[boostrap_idx],
        oob_X=X[oob_idx],
        oob_y=y[oob_idx],
    )


if __name__ == "__main__":
    X = np.arange(10)
    y = np.random.randint(0, 2, X.shape)

    sample = make_bootstrap_sample(X, y)

    print(sample.bootstrap_X)
    print(sample.bootstrap_y)
    print(sample.oob_X)
    print(sample.oob_y)
