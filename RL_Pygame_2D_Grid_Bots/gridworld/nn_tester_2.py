import numpy as np
from neural_network import neural_network

from sklearn.datasets import load_iris
from sklearn.model_selection import train_test_split

XT, YT = load_iris(return_X_y = True)
newYT = np.zeros([len(YT), 3])
for i, y in enumerate(YT):
    newYT[i][y] = 1

X_train, X_test, Y_train, Y_test = train_test_split(XT, newYT, test_size=0.2)

X = np.array(X_train).T
Y = np.array(Y_train).T

myNet = neural_network([4, 50, 20, 5, 3])
myNet.training_batch_size = 100
myNet.train_network(X, Y, 10000)

X = np.array(X_test).T
Y = np.array(Y_test).T

Y_hat = myNet.classify_data(X)

print("Differences: ")
print(Y)
print(Y_hat)
print(Y - Y_hat)

print("Average Squared Error: ")
print(np.sum((Y - Y_hat)**2)/Y.shape[1])


