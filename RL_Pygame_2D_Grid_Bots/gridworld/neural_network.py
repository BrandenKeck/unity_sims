import numpy as np

# Neural Network Class for Feature Approximation in Reinforcement Learning
class neural_network():

    def __init__(self, layer_sizes):

        # Track layersizes as a numpy array
        self.layersizes = np.array([int(i) for i in layer_sizes])
        self.training_batch_size = 1

        # Initialize Node Arrays
        self.a = []
        self.z = []
        self.y_hat = None
        self.y_prob = None

        # Initialize Weight Arrays
        self.w = []
        self.b = []
        for i in np.arange(1, len(self.layersizes)):
            self.w.append(0.01 * np.random.randn(self.layersizes[i], self.layersizes[i-1]))
            self.b.append(np.zeros(self.layersizes[i]))

        # Misc. Network Settings
        self.learning_rates = 0.01 * np.ones(len(self.w))
        self.leaky_relu_rates = 0.01 * np.ones(len(self.w))
        self.huber_cost_delta = 5

        # Initialize Cost Function Settings
        # DEFAULT: Huber Cost Function
        self.use_huber_cost = True
        self.use_hellinger_cost = False
        self.use_quadratic_cost = False

        # Initialize Activation Function Settings
        # DEFAULT: ReLU for hidden layers and Sigmoid output layer
        self.use_leaky_relu = [True] * (len(self.w) - 1) + [False]
        self.use_sigmoid = [False] * (len(self.w) - 1) + [True]
        self.use_relu = [False] * len(self.w)
        self.use_tanh = [False] * len(self.w)

    # Function to perform NN training steps (iterative prediction / backpropagation)
    def train_network(self, data, labels, iter):

        # Reshape vector into 2D array if necessary
        if labels.ndim == 1:
            labels.shape = (1, -1)

        # Loop over random batches of data for "iter" training iterations
        for ation in np.arange(iter):
            if ation%1000 == 0: print("Current Training Step: " + str(ation))
            batch_idx = np.random.choice(data.shape[1], size=self.training_batch_size, replace=False)
            X = data[:,batch_idx]
            Y = labels[:,batch_idx]
            self.predict(X)
            self.learn(Y)

    # Perform a single prediction-only step over a given dataset
    def classify_data(self, data):
        self.predict(data)
        return self.y_hat

    # Function to perform NN prediction on a matrix of data columns
    def predict(self, X):

        # Empty stored training values
        self.a = [X]
        self.z = []

        # Loop over all layers
        for i in np.arange(len(self.layersizes) - 1):

            # Calculate Z (pre-activated node values for layer)
            z = np.matmul(self.w[i], self.a[i])
            self.z.append(z)

            # Calculate A (activated node values for layer)
            if self.use_leaky_relu[i]: a = leaky_ReLU(z, self.leaky_relu_rates[i])
            elif self.use_relu[i]: a = ReLU(z)
            elif self.use_tanh[i]: a = tanh(z)
            elif self.use_sigmoid[i]: a = sigmoid(z)
            else: a = ReLU(z)
            self.a.append(a)

        # Store prediction
        self.y_hat = self.a[len(self.a) - 1]
        self.y_prob = self.y_hat / np.sum(self.y_hat, axis=0)

    # Function to perform backpropagation on network weights after a prediction has been stored in self.y_hat
    def learn(self, Y):

        # Store number of datapoints
        m = Y.shape[1]

        # Loop over layers backwards
        for i in np.flip(np.arange(len(self.w))):

            # Calculate Loss Function Derivatiove dL/dA
            if self.use_huber_cost: dL = d_huber(Y, self.y_hat, self.huber_cost_delta)
            elif self.use_hellinger_cost: dL = d_hellinger(Y, self.y_hat)
            elif self.use_quadratic_cost: dL = d_quadratic(Y, self.y_hat)
            else: dL = d_hellinger(Y, self.y_hat)

            # Calculate Activation Function Derivative dA/dZ
            if self.use_leaky_relu[i]: dA = d_leaky_ReLU(self.z[i], self.leaky_relu_rates[i])
            elif self.use_relu[i]: dA = d_ReLU(self.z[i])
            elif self.use_tanh[i]: dA = d_tanh(self.z[i])
            elif self.use_sigmoid[i]: dA = d_sigmoid(self.z[i])
            else: dA = d_sigmoid(self.z[i])

            # Calculated pre-activated node derivative
            if i == (len(self.w) - 1):
                dz = dL * dA
                prev_dz = dz
            else:
                dz = np.matmul(self.w[i + 1].T, prev_dz) * dA
                prev_dz = dz

            # Calculate Weight Derivatives
            dw = (1/m) * np.matmul(dz, self.a[i].T)
            db = (1/m) * np.sum(dz, axis=1, keepdims=True)

            # Apply Learning Functions
            self.w[i] = self.w[i] - self.learning_rates[i] * dw
            self.b[i] = self.b[i] - self.learning_rates[i] * db

'''
COST FUNCTION DERIVATIVES
'''

def d_huber(Y, Y_hat, delta):
    if np.linalg.norm(Y_hat - Y) < delta: return Y_hat - Y
    else: return delta * np.sign(Y_hat - Y)

def d_hellinger(Y, Y_hat):
    return (1/np.sqrt(2))*(np.ones(Y.shape) - np.divide(np.sqrt(Y), np.sqrt(Y_hat)))

def d_quadratic(Y, Y_hat):
    return Y_hat - Y

''' 
ACTIVATION FUCNTIONS 
'''
def leaky_ReLU(x, e):
    return np.maximum(e*x, x)

def ReLU(x):
    return np.maximum(0, x)

def tanh(x):
    return (np.exp(x) - np.exp(-1*x))/(np.exp(x) + np.exp(-1*x))

def sigmoid(x):
    return 1/(1+np.exp(-1*x))

''' 
ACTIVATION FUCNTION DERIVATIVES 
'''

def d_leaky_ReLU(x, e):
    return np.where(x > 0, 1.0, e)

def d_ReLU(x):
    return np.where(x > 0, 1.0, 0)

def d_tanh(x):
    return 1 - (tanh(x))**2

def d_sigmoid(x):
    return sigmoid(x)*(1 - sigmoid(x))