from dataclasses import dataclass

import numpy as np


@dataclass
class BootstrapSample:
    bootstrap_X: np.ndarray
    bootstrap_y: np.ndarray
    oob_X: np.ndarray
    oob_y: np.ndarray
    oob_preditions: np.ndarray = None
    oob_probabilities: np.ndarray = None
