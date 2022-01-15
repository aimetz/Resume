from MDL.activations.activation import Activation
from MDL.tensor import Tensor

import numpy as np


def sigmoid(x: Tensor) -> Tensor:
    return 1 / (1 + np.exp(-x))


def sigmoid_prime(x: Tensor) -> Tensor:
    s = sigmoid(x)
    return s * (1 - s)


class Sigmoid(Activation):
    def __init__(self):
        super().__init__(sigmoid, sigmoid_prime)
