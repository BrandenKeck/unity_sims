import numpy as np

# Artificial Neural Network Class for Feature Approximation in Reinforcement Learning
class neural_network():

    def __init__(self, layer_sizes):

        # Structure Params
        self.layersizes = np.array([int(i) for i in layer_sizes])

        # Training values
        self.w = []
        self.b = []
        for i in np.arange(1, len(self.layersizes)):
            self.w.append(np.ones([self.layersizes[i], self.layersizes[i-1]]).tolist())
            self.b.append(np.ones(self.layersizes[i]))

        # Network Parameters
        self.learning_rates = 0.1 * np.ones(len(layer_sizes))
        self.leaky_relu_rates = 0.01 * np.ones(len(layer_sizes))

        # Activation Function Settings
        self.use_leaky_relu = [True] * len(layer_sizes)
        self.use_relu = [False] * len(layer_sizes)
        self.use_tanh = [False] * len(layer_sizes)
        self.use_sigmoid = [False] * len(layer_sizes)

    def train_network(self, current_state):

        # Vectorize the state matrix
        state_vector = np.array(current_state).flatten().tolist()




        '''
        HERE
        '''





def sigmoid(x):
    return 1/(1+np.exp(-x))

def ReLU(x):
    return np.max(0, x)