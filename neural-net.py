import sys
import numpy as np

#sigmoid (logistic) function
def nonlin(x, deriv=False):
	if(deriv==True):
		return x*(1-x)
	return 1/(1+np.exp(-x))

#map given vector v through logistic NN
def predict(W, v):
	for w in W:
		v = nonlin(np.dot(v,w))
	return v

def three_layer_nn(X, y, iterations=20000):
	#randomly initialize our weights with mean 0
	syn0 = 2*np.random.random((3,4)) - 1
	syn1 = 2*np.random.random((4,1)) - 1

	for j in xrange(iterations):
		#feed forward through layers 0,1, and 2 (forward propogation)
		l0 = X
		l1 = nonlin(np.dot(l0,syn0))
		l2 = nonlin(np.dot(l1,syn1))

		#difference between result and the target value:
		l2_error = y - l2

		#create back-prop amounts, back one layer:
		l2_delta  = l2_error*nonlin(l2,deriv=True)

		#how much did each l1 value contribute to the l2 error
		# (according to the weights
		l1_error = l2_delta.dot(syn1.T)

		#create back-prop amounts, back two layers:
		l1_delta = l1_error * nonlin(l1, deriv=True)

		#modify neural net
		syn1 += l1.T.dot(l2_delta)
		syn0 += l0.T.dot(l1_delta)

	#return list of layers (of weights)
	return [syn0, syn1]
