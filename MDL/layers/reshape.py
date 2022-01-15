from MDL.tensor import Tensor
from MDL.layers.layer import Layer


class Reshape(Layer):
    def __init__(self, input_shape, output_shape) -> None:
        super().__init__()
        self.input_shape = input_shape
        self.output_shape = output_shape

    def forward(self, inputs: Tensor) -> Tensor:
        """
        Push inputs forward
        """
        return inputs.reshape(self.output_shape)

    def backward(self, grad: Tensor) -> Tensor:
        """
        Backpropagate gradient through the layer
        """
        return grad.reshape(self.input_shape)
