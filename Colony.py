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

        self.occupied_tiles = []

        self.con_chance = 0.0
        self.split_chance = 0.0

    def takeTurn(self, t):

        if self.alive:
            self.rounds_alive += 1
            decision = self.NN.forward(self.X)
            self.con_chance = decision[0]
            self.split_chance = decision[1]
            for tile in self.occupied_tiles:
                if tile.alive:
                    # tile.growth_rate = decision[0]
                    tile.consumption_rate = decision[0]
                    self.X[2] = decision[0]
                    splitPopulation(self, tile, t)

            self.updateX(t)

    def updateX(self, t):
        res, pop, c_r, g_r, rgr = 0.0, 0.0, 0.0, 0.0, 0.0
        for i in self.occupied_tiles:
            res += i.resources
            pop += i.pop
            c_r += i.consumption_rate
            g_r += i.growth_rate
            rgr += i.resource_growth_rate

        if pop == 0.0:
            self.alive = False
            self.col_color = (225,225,225)
        else:
            a = [0 for x in range(5)]
            a[0] = res/len(self.occupied_tiles)
            a[1] = pop/len(self.occupied_tiles)
            a[2] = c_r/len(self.occupied_tiles)
            a[3] = g_r/len(self.occupied_tiles)
            a[4] = rgr/len(self.occupied_tiles)

            for i in range(len(self.X)):
                if self.X[i] > 1.0:
                    self.X[i] = 1.0
                elif self.X[i] < 0.0:
                    self.X[i] = 0.0

            self.resources = round(a[0], 4)
            self.population = round(a[1], 4)
            self.consumption_rate = round(a[2], 4)
            self.growth_rate = round(a[3], 4)
            self.resource_growth_rate = round(a[4], 4)

            # self.X = [a[0], a[1], a[2], a[3], a[4]]
            self.X = [self.resources, self.population, self.consumption_rate, self.growth_rate, self.resource_growth_rate]


def findFittest(colonies, t):
    contenders = []

    fittest = 0
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


    if len(contenders) >= 2:
        max_pop = 0.0
        index = 0
        for i in contenders:
            if i.pop - deadCells[index] > max_pop:
                max_pop = i.pop
                fittest = i
            index += 1

    # print 'C.fF() fittest.g_r: {}'.format(fittest.X[3])
    c = genChildren(fittest, t)
    print 'C.fF() c: {}'.format(len(c))
    return c

def genChildren(parent, t):
    global tilemap
    c = [parent]
    while len(c) < 4:
        # print parent
        child_X = copy.deepcopy(parent.X)
        child = Colony()
        tile = Occ_Tile()
        tile.softSetCols(t)
        child.occupied_tiles.append(tile)

        for i in range(5):
            variance = r.uniform(-.20, .20)

            if child_X[i] >= 1.0:
               child_.X[i] = 1.0 - abs(variance)
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
        c.append(child)

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
                self.resources = t[x][y].resources
                self.color = (self.pop*self.col_color[0], self.pop*self.col_color[1], self.pop*self.col_color[2])
                self.alive = True
                self.coordinates = [x, y]
                t[x][y] = self

                successful = True
