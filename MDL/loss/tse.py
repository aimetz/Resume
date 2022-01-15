from MDL.loss.loss import Loss
from MDL.tensor import Tensor


class TSE(Loss):
    """
    Total Squared Error
    """
    def loss(self, predicted: Tensor, actual: Tensor) -> float:
        return ((predicted - actual) ** 2).sum()

    def grad(self, predicted: Tensor, actual: Tensor) -> Tensor:
        return (predicted - actual) * 2


