"""
A layer passes its inputs forward and propagates gradients backward
"""
from MDL.layers.layer import Layer
from MDL.tensor import Tensor

import numpy as np


class Linear(Layer):
    """
    computes output = inputs @ w + b
    """
    def __init__(self, num_inputs: int, num_neurons: int) -> None:
        # inputs are (batch_size, num_inputs)
        # outputs are (batch_size, num_neurons)
        super().__init__()
        self.params["w"] = np.random.randn(num_inputs, num_neurons)
        self.params["b"] = np.random.randn(num_neurons)

    def forward(self, inputs: Tensor) -> Tensor:
        """
        outputs = inputs @ w + b
        """
        self.inputs = inputs
        return inputs @ self.params["w"] + self.params["b"]

    def backward(self, grad: Tensor) -> Tensor:
        """
        if y = f(x) and x = a * b + c
        then dy/da = f'(x) * b
        and dy/db = f'(x) * a
        and dy/da = f'(x)

        if y = f(x) and x = a @ b + c
        then dy/da = f'(x) @ b.T
        and dy/db = a.T @ f'(x)
        and dy/da = f'(x)
        """
        self.grads["b"] = grad.sum(axis=0)
        self.grads["w"] = self.inputs.T @ grad
        return grad @ self.params["w"].T
