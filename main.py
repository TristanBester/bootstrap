from dataclasses import dataclass

import numpy as np


@dataclass
class BootstrapSample:
    bootstrap_X: np.ndarray
    bootstrap_y: np.ndarray
    oob_X: np.ndarray
    oob_y: np.ndarray
    predictions: np.ndarray = None
    probabilites: np.ndarray = None


@dataclass
class MetricSet:
    metrics: list[callable]
    inputs: list[str]
    kwargs: list[dict] = None


def acc(y_true: np.ndarray, y_pred: np.ndarray) -> float:
    return (y_true == y_pred).astype(int).mean()


def log_loss(y_true: np.ndarray, y_pred_proba: np.ndarray) -> float:
    error_one = y_true * np.log1p(y_pred_proba)
    error_two = (1 - y_true) * np.log1p(1 - y_pred_proba)
    error = -(error_one + error_two)
    return error.mean()


def produce() -> BootstrapSample:
    sample = BootstrapSample(
        bootstrap_X=np.array([1, 1, 0, 0]),
        bootstrap_y=np.array([0, 0, 1, 1]),
        oob_X=np.array([1, 0]),
        oob_y=np.array([0, 1]),
    )
    return sample


def consume(sample: BootstrapSample) -> None:
    sample.predictions = np.array([0, 1])
    sample.probabilites = np.array([0.3, 0.9])


def process(result: BootstrapSample, metric_set: MetricSet) -> dict:
    result_set = {}

    for inpt, metric in zip(metric_set.inputs, metric_set.metrics):
        if inpt == "pred":
            metric_value = metric(result.oob_y, result.predictions)
        else:
            metric_value = metric(result.oob_y, result.probabilites)
        result_set[metric.__name__] = metric_value
    return result_set


if __name__ == "__main__":
    # samples = [produce() for i in range(5)]
    # results = [consume(i) for i in samples]
    sample = produce()
    consume(sample)

    metric_set = MetricSet(metrics=[acc, log_loss], inputs=["pred", "proba"])

    print(process(sample, metric_set))
