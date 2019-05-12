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


#create a two-layer (nx1) neural net, where X is the training data,
# y is the desired output for the given data (n), and iterations
# is the number of iterations desired
def two_layer_nn(X, y, iterations=10000):
	#get dimensions of incoming matrix
	(m, n) = np.shape(X)

	#initialize weights of an nx1 matrix with random numbers from
	#[1,1] (with mean 0), where n is the number of inputs
	syn0 = 2*np.random.random((n,1)) - 1

	for iter in xrange(iterations):

		#forward propogation
		L0 = X
		L1 = nonlin(np.dot(L0,syn0))

		#print l1

		# how much did we miss?
		L1_error = y - L1

		#multiply how much we missed by the
		# slope of the sigmoid at the values in L1
		L1_delta = L1_error * nonlin(L1,True)

		#update weights:
		syn0 += np.dot(L0.T,L1_delta)

	#return list of layers (of weights)
	return [syn0]

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

def main(arglist):
	np.random.seed(100)

	X = np.array([
	[0,0,1],
	[0,1,1],
	[1,0,1],
	[1,1,1] ])

	y = np.array([[0,0,1,1]]).T #easy
	#y = np.array([[0,1,1,0]]).T #hard
	W = two_layer_nn(X,y, iterations=1000)

	print('output: {}\n'.format(\
	predict(W, np.array([[1,1,1]]))))
	#print(nonlin(-10))
	#print(nonlin(0))
	#print(nonlin(10))

	W2 = three_layer_nn(X,y)
	print('output: {}\n'.format(\
	predict(W2, np.array([[1,0,1]]))))
# 
# if __name__ == '__main__':
# 	main(sys.argv[1:])
