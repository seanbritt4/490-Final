import copy
import random as r
'''
test file illustrating how to implement variance through generations
'''
def gv(X):
    child = copy.deepcopy(X)
    for i in range(0, len(X)):
        variance = r.uniform(-.10, .10)

        if X[i] >= 1.0:
            X[i] = 1.0 - abs(variance)
        elif X[i] <= 0.0:
            X[i] = 0.0 + abs(variance)
        else:
            X[i] += variance

        if X[i] <= 0.0:
            X[i] = 0.0
        elif X[i] >= 1.0:
            X[i] = 1.0
        X[i] = round(X[i], 4)
    # print j, X
    return child


if __name__ == "__main__":
    X = [0.5, 0.5, 0.0, 1.0]
    gv(X)
