import numpy as np
import Neural_Net
'''
test file showing off the NN

population, consumption_rate, growth_rate

1.0             -> split
0.0~0.99...9    -> wait, consume 0.x amount of resources
'''

X = np.array([0.4, 0.5, 0.6, 0.3, 0.4])

NN = Neural_Net1.Neural_Network()
# NN.forward(w)



print "Predicted Output: ", str(NN.forward(X))
