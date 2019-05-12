import random as r
'''
test file illustrating how to implement variance through generations
'''

successful = [0.5, 0.5, 0.0, 1.0]

for j in range(0,100):
    for i in range(0, len(successful)):
        variance = r.uniform(-.10, .10)

        if successful[i] >= 1.0:
            successful[i] = 1.0 - abs(variance)
        elif successful[i] <= 0.0:
            successful[i] = 0.0 + abs(variance)
        else:
            successful[i] += variance

        if successful[i] <= 0.0:
            successful[i] = 0.0
        elif successful[i] >= 1.0:
            successful[i] = 1.0
        successful[i] = round(successful[i], 4)

    print j, successful
