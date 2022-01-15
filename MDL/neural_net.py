"""
A Neural Network is a collection of layers
"""
from typing import Sequence, Iterator, Tuple

from MDL.tensor import Tensor
from MDL.layers.layer import Layer
from MDL.layers.linear import Linear

import pandas as pd
import json


class NeuralNet:
    def __init__(self, Layers: Sequence[Layer]) -> None:
        self.layers = Layers

    def forward(self, inputs: Tensor) -> Tensor:
        for Layer in self.layers:
            print(inputs.shape)
            inputs = Layer.forward(inputs)
        return inputs

    def backward(self, grad: Tensor) -> Tensor:
        for Layer in reversed(self.layers):
            grad = Layer.backward(grad)
        return grad

    def params_and_grads(self) -> Iterator[Tuple[Tensor, Tensor]]:
        for Layer in self.layers:
            for name, param in Layer.params.items():
                grad = Layer.grads[name]
                yield param, grad

    def to_series(self, code):
        series = pd.Series(dtype=object)
        series.loc["code"] = code
        for i, Layer in enumerate(self.layers):
            if type(Layer) == Linear:
                series.loc["Weights" + str(i)] = json.dumps(Layer.params["w"].tolist())
                series.loc["Bias" + str(i)] = json.dumps(Layer.params["b"].tolist())
        return series

    def save(self, text_file, code=None):
        s = self.to_series(code)
        try:
            df = pd.read_csv(text_file, index_col=0)
        except pd.errors.EmptyDataError:
            df = pd.DataFrame(columns=s.index)
        except FileNotFoundError:
            a = open(text_file, "w")
            a.close()
            df = pd.DataFrame(columns=s.index)
        df.loc[len(df)] = s.transpose()
        df.to_csv(text_file)
