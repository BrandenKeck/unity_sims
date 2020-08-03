import numpy as np
from neural_network import neural_network

from sklearn.model_selection import train_test_split

n = 1000 # number of samples per cluster
X1 = np.random.multivariate_normal([0,0], [[1,0],[0,1]], n)             # Cluster 1
X2 = np.random.multivariate_normal([0,5], [[1,0.25],[0.25,1]], n)       # Cluster 2
X3 = np.random.multivariate_normal([5,2.5], [[1,0.5],[0.5,1]], n)       # Cluster 3
XT = np.concatenate((X1, X2, X3), 0)

YT = np.zeros([XT.shape[0], 3])
YT[0:n, 0] = 1
YT[n+1:2*n, 1] = 1
YT[2*n+1:3*n, 2] = 1

XT = XT.T
YT = YT.T

myNet = neural_network([2, 50, 20, 3])
myNet.training_batch_size = 10
myNet.train_network(XT, YT, 10000)

while True:
    i = np.random.randint(0, XT.shape[1], 1)
    Y_hat = myNet.classify_data(XT[:,i])
    print(Y_hat)
    print(YT[:,i])
    input()


