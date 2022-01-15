"""
A layer passes its inputs forward and propagates gradients backward
"""
from typing import Dict
from MDL.tensor import Tensor


class Layer:
    def __init__(self) -> None:
        self.params: Dict[str, Tensor] = {}
        self.grads: Dict[str, Tensor] = {}
        self.inputs: Tensor or None = None

    def forward(self, inputs: Tensor) -> Tensor:
        """
        Push inputs forward
        """
        raise NotImplementedError

    def backward(self, grad: Tensor) -> Tensor:
        """
        Backpropagate gradient through the layer
        """
        raise NotImplementedError
