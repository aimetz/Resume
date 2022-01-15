from typing import Sequence

from MDL.layers.layer import Layer
from MDL.tensor import Tensor

import numpy as np
from scipy import signal


class Convolutional(Layer):
    def __init__(self, input_shape: Sequence, kernel_size: int, depth: int) -> None:
        super().__init__()
        input_depth, input_height, input_width = input_shape
        self.input_shape = input_shape
        self.input_depth = input_depth
        self.kernel_shape = (depth, input_depth, kernel_size, kernel_size)
        self.params["k"] = np.random.randn(*self.kernel_shape)
        self.params["b"] = np.random.randn(depth, input_depth, input_height - kernel_size + 1,
                                           input_width - kernel_size + 1)

    def forward(self, inputs: Tensor) -> Tensor:
        """
        Push inputs forward
        """
        n, h_in, w_in, _ = inputs.shape
        _, h_out, w_out, _ = output_shape
        h_f, w_f, _, n_f = self._w.shape

        output_shape = self.calculate_output_dims(input_dims=a_prev.shape)
        output = np.zeros(output_shape)

        for i in range(h_out):
            for j in range(w_out):
                h_start, w_start = i, j
                h_end, w_end = h_start + h_f, w_start + w_f

                output[:, i, j, :] = np.sum(
                    a_prev[:, h_start:h_end, w_start:w_end, :, np.newaxis] *
                    self._w[np.newaxis, :, :, :],
                    axis=(1, 2, 3)
                )

    return output + self._b

    def backward(self, grad: Tensor) -> Tensor:
        """
        Backpropagate gradient through the layer
        """
        self.grads["k"] = np.zeros(self.kernel_shape)
        self.grads["b"] = grad
        input_grad = np.zeros(self.input_shape)
        print(grad)
        for i in range(self.image_depth):
            for j in range(self.input_depth):
                print(j)
                print(self.inputs[i][j], grad[i][j])
                self.grads["k"][i] = signal.correlate2d(self.inputs[i][j], grad[i][j], "valid")
                #input_grad[j] += signal.convolve2d(grad[i], self.params["k"][i, j], "full")
        return input_grad
