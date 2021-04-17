import numpy as np


class Layer:
    def __init__(self, n_inputs, n_neurons):
        self.size = (n_inputs, n_neurons)
        self.weights = np.random.randn(n_inputs, n_neurons)
        self.bias = np.zeros((1, n_neurons))

    def __repr__(self):
        return "Weights:\n{}\nBias:\n{}\n".format(self.weights, self.bias)

    def forward(self, inputs):
        self.output = np.dot(inputs, self.weights) + self.bias
        return self.output

    def lin_rect_act(self):
        self.output_act = np.maximum(0, self.output)
        return self.output_act

    def sigmoid_act(self):
        self.output_act = 1/(1+np.power(np.e, self.output))
        return self.output_act

    def mutate(self, intensity):
        new = Layer(self.size[0], self.size[1])
        new.weights = self.weights+.001*intensity*np.random.randn(self.size[0], self.size[1])
        new.bias = self.bias+.001*intensity*np.random.randn(1, self.size[1])
        return new

