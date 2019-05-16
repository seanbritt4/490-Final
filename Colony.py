from framework import tilemap, MAPWIDTH, MAPHEIGHT, splitPopulation
import tiles
import copy
import random as r
import nn
import numpy as np

class Colony():
    def __init__(self):
        self.alive = True
        self.rounds_alive = 0

        self.color = (0, 0, 0)      #must be set from framework
        self.col_color = (0, 0, 0)  #color of their colony

        self.resources = round(r.uniform(0.0, 0.99), 2)         # available resources
        self.pop = round(r.uniform(0.50, 0.66), 2)              # cluster population
        self.consumption_rate = round(r.uniform(0.25, 0.75), 2) # resource consumption rate
        self.growth_rate = round(r.uniform(0.25, 0.75), 2)      # population growth rate
        self.resource_growth_rate = 0.0                         # resource growth rate

        self.X = [self.resources, self.pop, self.consumption_rate, self.growth_rate, self.resource_growth_rate]
        self.NN = nn.Neural_Network()
        # self.NN
        self.occupied_tiles = []

        self.con_chance = 0.0
        self.split_chance = 0.0


    def takeTurn(self, t):
        decision = self.makeDecision()
        if self.alive:
            self.rounds_alive += 1
            if decision == 'split':
                # print 'split'
                splitPopulation(self, t)
                self.pop *= 1.5
                self.consumption_rate *= .5
            else:                           # must be 'consume'
                self.consumption_rate = decision
            self.updateX()


    def makeDecision(self):
        decision = self.NN.forward(self.X)
        self.con_chance = decision[0]
        self.split_chance = decision[1]
        if self.con_chance >= self.split_chance:
            return 'consume'
        else:
            return 'split'

    def updateX(self):
        pop = 0.0
        for i in self.occupied_tiles:
            pop += i.pop

        if pop == 0.0:
            self.alive = False
            self.col_color = (225,225,225)
        else:
            self.X[1] = round(pop/len(self.occupied_tiles), 4)

def findFittest(colonies, t):
    contenders = []

    fittest = Colony()
    max_rounds = 1
    for i in colonies:
        if i.rounds_alive >= max_rounds:
            contenders.append(i)

    #this is an array for holding dead cells in each of the colonies
    deadCells = [0 for x in range(len(contenders))]
    index = 0
    for colony in contenders:
        for tile in range(len(colony.occupied_tiles)):
            if colony.occupied_tiles[tile].alive == False:
                deadCells[index] += 1
        index += 1


    # print len(contenders)
    if len(contenders) >= 2:
        max_pop = 0.0
        index = 0
        for i in contenders:
            if i.pop - deadCells[index] > max_pop:
                max_pop = i.pop
                fittest = i
            index += 1

    print "fittest: {}".format(fittest.X)
    c = genChildren(fittest, t)
    return c

def genChildren(parent, t):
    global tilemap
    nn = parent.NN
    c = [parent , parent, parent, parent]
    for a in range(4):
        child_X = copy.deepcopy(parent.X)
        child = Colony()
        tile = Occ_Tile()
        tile.softSetCols(t)
        child.occupied_tiles.append(tile)

        for i in range(5):
            variance = r.uniform(-.05, .05)

            if child_X[i] >= 1.0:
               child_X[i] = 1.0 - abs(variance)
            elif child_X[i] <= 0.0:
                child_X[i] = 0.0 + abs(variance)
            else:
                child_X[i] += variance

            if child_X[i] <= 0.0:
                child_X[i] = 0.0
            elif child_X[i] >= 1.0:
                child_X[i] = 1.0

            child_X[i] = round(child_X[i], 4)
            child.X = child_X
            child.NN = nn
        c[a] = child

    return c


class Occ_Tile(Colony, tiles.Ground_Tile):
    def __init__(self):
        self.tile_type = 'occupied'
        self.color = (255, 0, 0)
        self.resources = 0
        self.pop = 0
        self.consumption_rate = 0
        self.growth_rate = 0
        self.col_color = (0, 0, 0)
        self.alive = True
        self.resource_growth_rate = 0
        self.coordinates = []


    def softSetCols(self, t):
        global tilemap
        successful = False
        while(successful == False):
            x = r.randint(0, MAPWIDTH-1)
            y = r.randint(0, MAPHEIGHT-1)
            if(t[x][y].tile_type != 'water'):
                self.color = (self.pop*self.col_color[0], self.pop*self.col_color[1], self.pop*self.col_color[2])
                self.alive = True
                self.coordinates = [x, y]
                t[x][y] = self

                successful = True
