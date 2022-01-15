from MDL.activations.activation import Activation
from MDL.tensor import Tensor

import numpy as np


def softmax(x: Tensor) -> Tensor:
    """ applies softmax to an input x"""
    e_x = np.exp(x - np.max(x))
    return e_x / e_x.sum()


def softmax_prime(x: Tensor) -> Tensor:
    raise NotImplementedError


class Softmax(Activation):
    def __init__(self):
        super().__init__(softmax, softmax_prime)
