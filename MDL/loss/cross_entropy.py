from MDL.loss.loss import Loss
from MDL.tensor import Tensor

import numpy as np


class CrossEntropy(Loss):
    def loss(self, predicted: Tensor, actual: Tensor) -> float:
        return -(actual * np.log(predicted) + (1-actual) * np.log(1-predicted)).mean()

    def grad(self, predicted: Tensor, actual: Tensor) -> Tensor:
        return ((1 - actual) / (1 - predicted) - actual / predicted) / actual.size