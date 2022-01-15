from MDL.optimizers.optimizer import Optimizer
from MDL.neural_net import NeuralNet


class SGD(Optimizer):
    def __init__(self, lr: float = .001) -> None:
        self.lr = lr

    def step(self, net: NeuralNet) -> None:
        for param, grad in net.params_and_grads():
            param -= self.lr * grad
