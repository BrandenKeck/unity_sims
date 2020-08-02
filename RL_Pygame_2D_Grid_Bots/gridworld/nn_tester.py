import numpy as np
from neural_network import neural_network

from sklearn.datasets import load_iris
from sklearn.model_selection import train_test_split

XT, YT = load_iris(return_X_y = True)
X_train, X_test, Y_train, Y_test = train_test_split(XT, YT, test_size=0.2)

myNet = neural_network([4, 10, 1])
