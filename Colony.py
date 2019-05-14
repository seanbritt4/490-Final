from framework import tilemap, MAPWIDTH, MAPHEIGHT, splitPopulation
# import framework
import tiles
import copy
import random as r
import nn

class Colony():
    def __init__(self):
        self.alive = True
        self.rounds_alive = 0

        self.color = (0, 0, 0) #must be set from framework
        self.col_color = (0, 0, 0) #color of their colony

        self.resources = round(r.uniform(0.0, 0.99), 2)
        self.pop = round(r.uniform(0.33, 0.66), 2)
        self.consumption_rate = round(r.uniform(0.25, 0.75), 2)
        self.growth_rate = round(r.uniform(0.25, 0.75), 2)
        self.resource_growth_rate = 0.0

        self.X = [self.resources, self.pop, self.consumption_rate, self.growth_rate, self.resource_growth_rate]
        self.NN = nn.Neural_Network()

        self.occupied_tiles = []

        self.con_chance = 0.0
        self.split_chance = 0.0
        # self.map_location = [] #do we want random positions everytime?

    def takeTurn(self):
        # print 'C.tT()'
        # print self.alive,
        # print self.X
        if self.alive:
            self.rounds_alive += 1
            decision = self.makeDecision()
            # print decision
            # print decision
            if decision == 'split': # must be 'split'
                # self.splitPopulation()
                print 'C.tT(): ', self,
                splitPopulation(self)
                self.consumption_rate *= .1
            else:
                self.consumption_rate = decision

            self.updatePop()
        # raw_input()

    def makeDecision(self):
        # print 'C.mD()'
        decision = self.NN.forward(self.X)
        # print decision
        self.con_chance = decision[0]
        self.split_chance = decision[1]
        if self.con_chance >= self.split_chance:
            return 'consume'
        else:
            return 'split'

    def updatePop(self):
        pop = 0.0
        for i in self.occupied_tiles:
            pop += i.pop

        if pop == 0.0:
            self.alive = False
            self.col_color = (225,225,225)
        else:
            self.pop = pop/len(self.occupied_tiles)

    def splitPopulation(self):
        global tilemap
        tried = [0, 0, 0, 0]
        dir_x = 0
        dir_y = 0

        for tile in self.occupied_tiles:
            sc = r.uniform(0.0, 1.0)
            if sc >= self.split_chance:
                x, y = tile.coordinates[0], tile.coordinates[1]
                for w in range(4):
                    success = False
                    while(success == False):
                        if(tried[0] == 1 and tried[1] == 1 and tried[2] == 1 and tried[3] == 1):
                            break
                        direction = r.randint(0, 3)
                        if(tried[direction] == 0):
                            tried[direction] = 1
                            success = True
                            if(direction == 0):
                                dir_y = 1
                                dir_x = 0
                            if(direction == 1):
                                dir_x = 1
                                dir_y = 0
                            if(direction == 2):
                                dir_y = -1
                                dir_x = 0
                            if(direction == 3):
                                dir_x = -1
                                dir_y = 0
                    #if(x > 0 and x < MAPWIDTH-1 and y > 0 and y < MAPHEIGHT -1):
                    new_x = x+dir_x
                    new_y = y+dir_y
                    if(x+dir_x < 0):
                        new_x = MAPWIDTH -1
                    if(x+dir_x >= MAPWIDTH-1):
                        new_x = 0
                    if(y+dir_y < 0):
                        new_y = MAPHEIGHT -1
                    if(y+dir_y >= MAPHEIGHT-1):
                        new_y = 0
                    #
                    # print x, y
                    # print new_x, new_y
                    # # print tilemap
                    # print type(tilemap[y][x])
                    # print tilemap[y][x]
                    #
                    # if(tilemap[new_x][new_y].tile_type == 'ground'):
                    #     new_tile = Colony.Occ_Tile()
                    #     self.occupied_tiles.append(new_tile)
                    #     new_tile.resources = tilemap[new_x][new_y].resources
                    #     new_tile.pop = tilemap[x][y].pop / 2.0
                    #     new_color = tilemap[x][y].col_color
                    #     new_tile.color = (new_color[0]*new_tile.pop, new_color[1]*new_tile.pop, new_color[2]*new_tile.pop)
                    #     new_tile.col_color = tilemap[x][y].col_color
                    #     new_tile.consumption_rate = tilemap[x][y].consumption_rate
                    #     new_tile.growth_rate = tilemap[x][y].growth_rate / 2.0
                    #     new_tile.resource_growth_rate = 0
                    #     new_tile.alive = True
                    #     new_tile.coordinates = [new_x, new_y]
                    #
                    #     tilemap[x][y].pop /= 2.0
                    #     tilemap[x][y].growth_rate /= 2.0
                    #     p = tilemap[x][y].pop
                    #     tilemap[x][y].color = (new_color[0]*p, new_color[1]*p, new_color[2]*p)
                    #     child = tilemap[new_x][new_y]
                    #     parent = tilemap[x][y]
                    #     break

def findFittest(colonies):
    contenders = []

    fittest = 0
    max_rounds = 1
    for i in colonies:
        if i.rounds_alive >= max_rounds:
            contenders.append(i)

    # print len(contenders)
    if len(contenders) >= 2:
        max_pop = 0.0
        for i in contenders:
            if i.pop > max_pop:
                max_pop = i.pop
                fittest = i
            # print i.pop

    print "fittest {}:".format(fittest.col_color), fittest.X
    return genChildren(fittest)
    # raw_input()

def genChildren(parent):
    c = [parent]
    while len(c) < 4:
        child_X = copy.deepcopy(parent.X)
        child = Colony()

        for i in range(5):
            variance = r.uniform(-.25, .25)

            if child_X[i] >= 1.0:
               chil_.X[i] = 1.0 - abs(variance)
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
        self.col_color_color = (0, 0, 0)
        self.alive = True
        self.resource_growth_rate = 0
        self.coordinates = []

    def printOcc(self):
        print self.tile_type
        print self.resources
        print self.pop
        print self.consumption_rate
        print self.growth_rate

    def printColor(self):
        print self.color
