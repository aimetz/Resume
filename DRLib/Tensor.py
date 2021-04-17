import numpy as np


# A Tensor is an N-dimensional Array
class Tensor:
    def __init__(self, shape=None, data=None):
        #self.tensor = np.ndarray(shape=shape, dtype=dtype)
        if data is None:
            self.tensor = np.zeros(shape)
        elif type(data) == np.ndarray:
            self.tensor = data
        else:
            print(type(data))
            raise ValueError

    def dot(self, other):
        return np.dot(self.tensor, other.tensor)

    def __mul__(self, other):
        return Tensor(data=np.dot(self.tensor, other.tensor))

    def __add__(self, other):
        return Tensor(data=(self.tensor+other.tensor))

    def __repr__(self):
        return str(self.tensor)


print(Tensor(shape=[3,2])+Tensor(shape=[3,2]))