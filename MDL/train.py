from MDL.tensor import Tensor
from MDL.neural_net import NeuralNet
from MDL.loss.loss import Loss
from MDL.loss.tse import TSE
from MDL.optimizers.optimizer import Optimizer
from MDL.optimizers.gradient_descent import SGD
from MDL.iterators.data import DataIterator
from MDL.iterators.batch_iterator import BatchIterator


def train(net: NeuralNet,
          inputs: Tensor,
          targets: Tensor,
          num_epochs: int = 5000,
          iterator: DataIterator = BatchIterator(),
          loss: Loss = TSE(),
          optimizer: Optimizer = SGD()) -> None:
    for epoch in range(num_epochs):
        epoch_loss = 0.0
        for batch in iterator(inputs, targets):
            predicted = net.forward(batch.inputs)
            epoch_loss += loss.loss(predicted, batch.targets)
            grad = loss.grad(predicted, batch.targets)
            net.backward(grad)
            optimizer.step(net)
        print(epoch, epoch_loss)
