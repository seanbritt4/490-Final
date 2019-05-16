import numpy as np

class Neural_Network(object):
  def __init__(self):
    self.inputSize = 5
    self.hiddenSize1 = 5
    self.hiddenSize2 = 4
    self.hiddenSize3 = 5
    self.outputSize = 2

    self.W1 = np.random.randn(self.inputSize, self.hiddenSize1) # (3x2) weight matrix from input to hidden layer
    self.W2 = np.random.randn(self.hiddenSize1, self.hiddenSize2)
    self.W3 = np.random.randn(self.hiddenSize2, self.hiddenSize3)
    self.W4 = np.random.randn(self.hiddenSize3, self.outputSize) # (3x1) weight matrix from hidden to output layer

  def forward(self, X):
    self.z = np.dot(X, self.W1) # dot product of X (input) and first set of weights
    self.z2 = self.sigmoid(self.z) # activation function
    self.z3 = np.dot(self.z2, self.W2) # dot product of hidden layer (z2) and second set of weights
    o = self.sigmoid(self.z3)

    #input to hlayer 1
    self.z = np.dot(X, self.W1)
    self.z2 = self.sigmoid(self.z)
    #hlayer1 to hlayer2
    self.z3 = np.dot(self.z2, self.W2)
    self.z4 = self.sigmoid(self.z3)
    #hlayer2 to hlayer 3
    self.z5 = np.dot(self.z4, self.W3)
    self.z6 = self.sigmoid(self.z5)
    #hlayer3 to output layer
    self.z7 = np.dot(self.z6, self.W4)
    o = self.sigmoid(self.z7) #
    return o

  def sigmoid(self, s):
    # activation function
    return 1/(1+np.exp(-s))
