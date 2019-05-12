import numpy as np
'''
cleaned up neural net. TODO: FIX COMMENTS & MAKE THEM RELEVANT
'''
class Neural_Network(object):
  def __init__(self):
  #parameters
    self.inputSize = 5
    self.hiddenSize2 = 6
    self.hiddenSize3 = 4
    self.outputSize = 2
    self.hiddenSize1 = 8

  #weights
    self.W1 = np.random.randn(self.inputSize, self.hiddenSize1) # (3x2) weight matrix from input to hidden layer
    self.W2 = np.random.randn(self.hiddenSize1, self.hiddenSize2)
    self.W3 = np.random.randn(self.hiddenSize2, self.hiddenSize3)
    self.W4 = np.random.randn(self.hiddenSize3, self.outputSize) # (3x1) weight matrix from hidden to output layer

  def forward(self, X):
    #Reference
    self.z = np.dot(X, self.W1) # dot product of X (input) and first set of 3x2 weights
    self.z2 = self.sigmoid(self.z) # activation function
    self.z3 = np.dot(self.z2, self.W2) # dot product of hidden layer (z2) and second set of 3x1 weights
    o = self.sigmoid(self.z3) # final activation function

    #forward propagation through our network
    #input to hlayer 1
    self.z = np.dot(X, self.W1) # dot product of X (input) and first set of 3x2 weights
    self.z2 = self.sigmoid(self.z) # activation function
    #hlayer1 to hlayer2
    self.z3 = np.dot(self.z2, self.W2) # dot product of X (input) and first set of 3x2 weights
    self.z4 = self.sigmoid(self.z3) # activation function
    #hlayer2 to hlayer 3
    self.z5 = np.dot(self.z4, self.W3) # dot product of X (input) and first set of 3x2 weights
    self.z6 = self.sigmoid(self.z5) # activation function
    #hlayer3 to output layer
    self.z7 = np.dot(self.z6, self.W4) # dot product of X (input) and first set of 3x2 weights
    o = self.sigmoid(self.z7) # final activation function
    return o

  def sigmoid(self, s):
    # activation function
    return 1/(1+np.exp(-s))

  def sigmoidPrime(self, s):
    #derivative of sigmoid
    return s * (1 - s)

  def train(self, X, y):
    o = self.forward(X)
