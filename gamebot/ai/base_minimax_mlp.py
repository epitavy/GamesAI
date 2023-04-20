from abc import ABC
import numpy as np
from .base_minimax import BaseMinimax
from .mlp import MLP


class BaseMinimaxMLP(BaseMinimax, ABC):
    """This class implements the scoring mecanism of minimax with a MLP.

    It does nothing more, except making the MLP parameters (weights and bias) be able to be
    transfered throught the parameters property.
    """

    def __init__(self, shape, filename=None):
        """Initialize the class with an MLP of the given shape.

        The MLP can be loaded from a file instead of being randomly initialized.
        """
        super().__init__()
        self.mlp = MLP(shape)
        if filename:
            params = np.load(filename)
            self.parameters = params

    def state_score(self, state):
        input_state = np.array(list(state))
        return self.mlp.forward_propagation(input_state)

    @property
    def parameters(self):
        """Return the MLP parameters in a numpy 1D array."""
        params = []
        for layer in self.mlp.layers:
            params.extend(layer[0].ravel())
            params.extend(layer[1].ravel())

        return np.array(params)

    @parameters.setter
    def parameters(self, parameters):
        """Set the MLP parameters from the given 1D array."""
        pcount = 0
        for i in range(len(self.mlp.shape) - 1):
            shape = (self.mlp.shape[i + 1], self.mlp.shape[i])
            weights = np.reshape(parameters[pcount:pcount + shape[0] * shape[1]], shape)
            pcount += shape[0] * shape[1]
            biases = np.reshape(parameters[pcount:pcount + shape[0]], shape[0])
            pcount += shape[0]
            self.mlp.layers[i] = (weights, biases)
