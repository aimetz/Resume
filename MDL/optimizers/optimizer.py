"""
An optimizer adjusts the params of a network
based on the gradients computed
"""
from MDL.neural_net import NeuralNet


class Optimizer:
    def step(self, net: NeuralNet) -> None:
        raise NotImplementedError
