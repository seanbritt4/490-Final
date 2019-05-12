import tiles
import random

class Cluster():
    def __init__(self):
        self.resources = round(random.uniform(0.0, 0.99), 2)
        self.pop = round(random.uniform(0.33, 0.66), 2)
        self.consumption_rate = round(random.uniform(0.25, 0.75), 2)
        self.growth_rate = round(random.uniform(0.25, 0.75), 2)
        self.color = (0, 0, 0) #must be set from framework
        self.civColor = (0, 0, 0) #color of their civilization
        self.alive = True
        self.rounds_alive = 0

        self.X = [self.resourcesself, self.pop, self.consumption_rate, self.growth_rate]

        self.NN = Neural_Network()

    def checkStatus(self):
        if self.pop == 0:
            self.alive = False

class Occ_Tile(Cluster, tiles.Ground_Tile):
    def __init__(self):
        self.tile_type = 'occupied'

    def print_occ(self):
        print self.tile_type
        print self.resources
        print self.pop
        print self.consumption_rate
        print self.growth_rate

    def print_color(self):
        print self.color
