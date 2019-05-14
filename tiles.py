import random

class Tile():
    resources = 0
    def __init__(self):
        self.tile_type = 'tile'
        self.color = (0, 0, 0)

    def find_color(self):
#        print self.tile_type
        pass

class Ground_Tile(Tile):
    def __init__(self):
        self.tile_type = 'ground'
        self.resources = round(random.uniform(0.0, 0.99), 2)
        self.color = (255.0*self.resources, 255.0*self.resources, 255.0*self.resources)
        self.pop = 0
        self.consumption_rate = 0
        self.growth_rate = 0
        self.color = (0, 0, 0)
        self.col_color = (0, 0, 0)
        self.alive = True #Set them alive initially, because it's inconsequential, and saves time :)
        self.resource_growth_rate = 0

    def print_color(self):
        print self.color, " ", self.resources

class Water_Tile(Tile):
    def __init__(self):
        self.tile_type = 'water'
        self.color = (0,0,255)
        self.resources = 0
        self.pop = 0
        self.consumption_rate = 0
        self.growth_rate = 0
        self.col_color = (0, 0, 0)
        self.alive = True
        self.resource_growth_rate = 0
