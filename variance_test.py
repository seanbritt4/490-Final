import numpy as np
import copy
import Neural_Net as nn
import generational_variance as gv
import random as r
'''
test file showing off the NN

population, consumption_rate, growth_rate

1.0             -> split
0.0~0.99...9    -> wait, consume 0.x amount of resources
'''
pop = r.uniform(0.1, 0.9)
res = r.uniform(0.1, 0.9)
res_consum_rate = r.uniform(0.1, 0.9)
pop_growth_rate = r.uniform(0.1, 0.9)
res_growth_rate = r.uniform(0.1, 0.9)

X1 = [pop, res, res_consum_rate, pop_growth_rate, res_growth_rate]

NN1 = nn.Neural_Network()
NN2 = nn.Neural_Network()
NN3 = nn.Neural_Network()
X2 = copy.copy(gv.gv(X1))
X3 = copy.copy(gv.gv(X1))

for j in range(0,4):
    print X1
    print X2
    print X3

    for i in range(0,2):
        # gv.gv(X)
        print "\n[pop, res, res_consum_rate, pop_growth_rate, res_growth_rate]"
        print 'X1:', X1
        print i, "Predicted Output: ", str(NN1.forward(X1))

        print "\n[pop, res, res_consum_rate, pop_growth_rate, res_growth_rate]"
        print "X2:", X2
        print i, "Predicted Output: ", str(NN2.forward(X2))

        print "\n[pop, res, res_consum_rate, pop_growth_rate, res_growth_rate]"
        print "X3:", X3
        print i, "Predicted Output: ", str(NN3.forward(X3))

    fittest = r.randint(1,3)
    if fittest == 1:
        print '----------------X1 is the fittest-----------------------'
        X2 = gv.gv(X1)
        X3 = gv.gv(X1)
    elif fittest == 2:
        print '----------------X2 is the fittest-----------------------'
        X1 = gv.gv(X2)
        X3 = gv.gv(X2)
    else:
        print '----------------X3 is the fittest-----------------------'
        X1 = gv.gv(X3)
        X2 = gv.gv(X3)
