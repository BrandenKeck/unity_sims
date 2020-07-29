import numpy as np

# Artificial Neural Network Class for Feature Approximation in Reinforcement Learning
class ann():

    def __init__(self, hidden_layer_sizes):

        # Structure Params
        self.initizalized = False
        self.layersizes = hidden_layer_sizes

        # Training values
        self.w = []
        self.b = []

        # Activation Function Settings
        self.use_sigmoid = True
        self.use_relu = False

    def train_network(self, current_state):

        # Vectorize the state matrix
        state_vector = np.array(current_state).flatten().tolist()

        # Initialize the Network on First Pass
        if not self.initizalized:
            self.layersizes.insert(0, len(state_vector))
            for layersize in self.layersizes:
                self.w.append(np.ones(layersize))
                self.b.append(1)
            self.initizalized = True

        '''
        HERE
        '''





def sigmoid(x):
    return 1/(1+np.exp(-x))

def ReLU(x):
    return np.max(0, x)