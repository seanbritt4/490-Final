import pygame, sys, time, random, math, copy, Colony
from pygame.locals import *
import numpy
from tiles import *

'''
References for colors -- 7 possibilites
RED     - (255, 0, 0)
GREEN   - (0, 255, 0)
BLUE    - (0, 0, 255)
YELLOW  - (255, 255, 0)
MAGENTA - (255, 0, 255)
CYAN    - (0, 255, 255)
GREY    - (255, 255, 255)
'''

#map dimensions
TILESIZE = 5
MAPWIDTH = 250
MAPHEIGHT = 100

RESOURCE_MODIFIER = 0.1
WATER_PASS_AMOUNT = 1
WATER_MODIFIER = 0.01
NEAR_WATER_GROWTH = 1.4

#array of tile objects
tilemap = []        # [[0 for x in range(MAPWIDTH)] for y in range(MAPHEIGHT)]
tilemap_save = []    # [[0 for x in range(MAPWIDTH)] for y in range(MAPHEIGHT)]

COLS = []

#initialize font
pygame.font.init()
font = pygame.font.SysFont('Arial', 30)
textsurface = font.render(' ', False, (255,255,255))

def splitPopulation(c, tile, t):
    global tilemap, MAPWIDTH, MAPHEIGHT

    tried = [0, 0, 0, 0]
    dir_x = 0
    dir_y = 0

    children = []

    # for tile in c.occupied_tiles:
    sc = random.uniform(0.0, 1.0)
    if .80 <= c.split_chance and tile.alive == True:
    # if sc >= c.split_chance and tile.alive == True:
        x, y = tile.coordinates[0], tile.coordinates[1]
        for w in range(4):
            success = False
            while(success == False):
                if(tried[0] == 1 and tried[1] == 1 and tried[2] == 1 and tried[3] == 1):
                    break
                direction = random.randint(0, 3)
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
            if(x >= 0 and x <= MAPWIDTH-1 and y >= 0 and y <= MAPHEIGHT -1):
                new_x = x+dir_x
                new_y = y+dir_y

                if(x+dir_x < 0):
                    new_x = MAPWIDTH -1
                if(x+dir_x > MAPWIDTH-1):
                    new_x = 0
                if(y+dir_y < 0):
                    new_y = MAPHEIGHT -1
                if(y+dir_y > MAPHEIGHT-1):
                    new_y = 0
                if(t[new_x][new_y].tile_type == 'ground' and t[new_x][new_y].alive == True):
                    new_tile = Colony.Occ_Tile()
                    new_tile.resources = t[new_x][new_y].resources
                    new_tile.pop = t[x][y].pop / 2.0
                    new_color = t[x][y].col_color
                    new_tile.color = (new_color[0]*new_tile.pop, new_color[1]*new_tile.pop, new_color[2]*new_tile.pop)
                    new_tile.col_color = t[x][y].col_color
                    new_tile.consumption_rate = t[x][y].consumption_rate
                    new_tile.growth_rate = t[x][y].growth_rate / 2.0
                    new_tile.resource_growth_rate = 0
                    new_tile.alive = True
                    new_tile.coordinates = [new_x, new_y]
                    t[new_x][new_y] = new_tile

                    t[x][y].pop /= 2.0
                    t[x][y].growth_rate /= 2.0
                    p = t[x][y].pop
                    t[x][y].color = (new_color[0]*p, new_color[1]*p, new_color[2]*p)
                    child = t[new_x][new_y]
                    parent = t[x][y]
                    children.append(child)
                    break

    c.occupied_tiles.extend(children)
    pass    # end splitPopulation

def fixMatrix(matrix):
    newMatrix = [[0 for y in range(MAPHEIGHT)] for x in range(MAPWIDTH)]
    for y in range(MAPHEIGHT):
        for x in range(MAPWIDTH):
            newMatrix[x][y] = matrix[y][x]

    global tilemap
    tilemap = newMatrix

def initWater(tilemap):
    startingNum = random.randint(1, 3)

    for i in range(startingNum):
        tilemap[0][random.randint(MAPHEIGHT/4, 3*(MAPHEIGHT/4))] = Water_Tile()

    for i in range(MAPWIDTH-1):
        for j in range(MAPHEIGHT):
            if(tilemap[i][j].tile_type == 'water'):
                pos = random.randint(-1, 1)
                if(j+pos >= 0 and j+pos < MAPHEIGHT):
                    tilemap[i+1][j+pos] = Water_Tile()

    for passes in range(WATER_PASS_AMOUNT):
        for x in range(MAPWIDTH-1):
            for y in range(MAPHEIGHT):
                if(tilemap[x][y].tile_type == 'water'):
                    if(random.uniform(0.0, 0.99) < WATER_MODIFIER):
                        #generate sub-rivers
                        posX = x
                        posY = y
                        plusOrMinus1 = 0
                        lastXMod = -1
                        while(plusOrMinus1 == 0):
                            plusOrMinus1 = random.randint(-1, 1)
                        while(random.uniform(0.0, 0.99) > WATER_MODIFIER*3):
                            if(y+plusOrMinus1 >= 0 and y+plusOrMinus1 < MAPHEIGHT):
                                xMod = random.randint(-1, 1)
                                while(xMod == 0):
                                    xMod = random.randint(-1, 1)
                                if(xMod != lastXMod):
                                    xMod = random.randint(-1, 1)
                                if(xMod != lastXMod):
                                    xMod = random.randint(-1, 1)
                                lastXMod = xMod
                                if(x+xMod >= 0 and x+xMod < MAPWIDTH):
                                    x += xMod
                                    y += plusOrMinus1
                                    tilemap[x][y] = Water_Tile()
                                    # print 'iW: water tile set'
                                    tilemap_simple = 1

def initResources(tilemap):
    #initilize starting point
    curX = 0
    curY = 0
    tilemap[curX][curY].resources = round(random.uniform(0.0, 0.05), 2)
    r = tilemap[curX][curY].resources
    tilemap[curX][curY].color = (0, 255*r, 0)
    curY += 1
    while(curX < MAPWIDTH):
        while(curY < MAPHEIGHT):
            #determine average resources around tile
            avgRes = 0
            #---take care of edge cases
            if(curX == 0):
                avgRes = tilemap[curX][curY-1].resources
            elif(curY == 0):
                avgRes = tilemap[curX-1][curY].resources + tilemap[curX-1][curY+1].resources
                avgRes /= 2.0
            elif(curY == MAPHEIGHT-1):
                avgRes = tilemap[curX-1][curY].resources + tilemap[curX-1][curY-1].resources
                avgRes /= 2.0
            else: #---base case
                avgRes = tilemap[curX-1][curY+1].resources + tilemap[curX-1][curY].resources + tilemap[curX-1][curY-1].resources
                avgRes /= 3.0

            #now we have average resources around the tile (or close to it)
            tilemap[curX][curY].resources = avgRes + round(random.uniform(RESOURCE_MODIFIER*-1, RESOURCE_MODIFIER), 2)
            if(tilemap[curX][curY].resources > 1):
                tilemap[curX][curY].resources = 1
            if(tilemap[curX][curY].resources < 0):
                tilemap[curX][curY].resources = 0
            r = tilemap[curX][curY].resources
            tilemap[curX][curY].color = (0, 255.0*r, 0)
            curY += 1

        curY = 0
        curX += 1

#called once at initilization, makes tiles near water have more resources
def growResourcesNearWater(tilemap):
    for x in range(MAPWIDTH):
        for y in range(MAPHEIGHT):
            #check up direction
            for i in range(8):
                if(y+i < MAPHEIGHT):
                    if(tilemap[x][y+i].tile_type == 'water' and tilemap[x][y].tile_type != 'water'):
                        if(i == 3):
                            tilemap[x][y].resources *= (1.0 + NEAR_WATER_GROWTH*0.15)
                        elif(i == 2):
                            tilemap[x][y].resources *= (1.0 + NEAR_WATER_GROWTH*0.175)
                        elif(i == 1):
                            tilemap[x][y].resources *= (1.0 + NEAR_WATER_GROWTH*0.2)
                        elif(i != 0):
                            tilemap[x][y].resources *= (1.0 + NEAR_WATER_GROWTH*0.125)
                        if(tilemap[x][y].resources > 1):
                            tilemap[x][y].resources = 0.99
                        r = tilemap[x][y].resources
                        tilemap[x][y].color = (0, 255*r, 0)

            #check down direction
            for i in range(8):
                if(y-i >= 0 ):
                    if(tilemap[x][y-i].tile_type == 'water' and tilemap[x][y].tile_type != 'water'):
                        if(i == 3):
                            tilemap[x][y].resources *= (1.0 + NEAR_WATER_GROWTH*0.15)
                        elif(i == 2):
                            tilemap[x][y].resources *= (1.0 + NEAR_WATER_GROWTH*0.175)
                        elif(i == 1):
                            tilemap[x][y].resources *= (1.0 + NEAR_WATER_GROWTH*0.2)
                        elif(i != 0):
                            tilemap[x][y].resources *= (1.0 + NEAR_WATER_GROWTH*0.125)

                        if(tilemap[x][y].resources > 1):
                            tilemap[x][y].resources = 0.99
                        r = tilemap[x][y].resources
                        tilemap[x][y].color = (0, 255*r, 0)

            #check right direction
            for i in range(8):
                if(x+i < MAPWIDTH):
                    if(tilemap[x+i][y].tile_type == 'water' and tilemap[x][y].tile_type != 'water'):
                        if(i == 3):
                            tilemap[x][y].resources *= (1.0 + NEAR_WATER_GROWTH*0.15)
                        elif(i == 2):
                            tilemap[x][y].resources *= (1.0 + NEAR_WATER_GROWTH*0.175)
                        elif(i == 1):
                            tilemap[x][y].resources *= (1.0 + NEAR_WATER_GROWTH*0.2)
                        elif(i != 0):
                            tilemap[x][y].resources *= (1.0 + NEAR_WATER_GROWTH*0.125)
                        if(tilemap[x][y].resources > 1):
                            tilemap[x][y].resources = 0.99
                        r = tilemap[x][y].resources
                        tilemap[x][y].color = (0, 255*r, 0)

            #check left direction
            for i in range(8):
                if(x-i >= 0):
                    if(tilemap[x-i][y].tile_type == 'water' and tilemap[x][y].tile_type != 'water'):
                        if(i == 3):
                            tilemap[x][y].resources *= (1.0 + NEAR_WATER_GROWTH*0.15)
                        elif(i == 2):
                            tilemap[x][y].resources *= (1.0 + NEAR_WATER_GROWTH*0.175)
                        elif(i == 1):
                            tilemap[x][y].resources *= (1.0 + NEAR_WATER_GROWTH*0.2)
                        elif(i != 0):
                            tilemap[x][y].resources *= (1.0 + NEAR_WATER_GROWTH*0.25)
                        if(tilemap[x][y].resources > 1):
                            tilemap[x][y].resources = 0.99
                        r = tilemap[x][y].resources
                        tilemap[x][y].color = (0, 255*r, 0)

#if tile is occupied or next to an occupied tile, grow the resource amount
def updateResources():
        for column in range(MAPWIDTH):
            for row in range(MAPHEIGHT):
                if tilemap[column][row].tile_type == 'occupied' and tilemap[column][row].alive == True:
                    newresources = 0
                    #left
                    if column > 0:
                        newresources += tilemap[column-1][row].resources
                    else:
                        newresources += tilemap[MAPWIDTH-1][row].resources

                    #right
                    if column < MAPWIDTH-1:
                        newresources += tilemap[column+1][row].resources
                    else:
                        newresources += tilemap[0][row].resources

                    #down
                    if row > 0:
                        newresources += tilemap[column][row-1].resources
                    else:
                        newresources += tilemap[column][MAPHEIGHT-1].resources

                    #up
                    if row < MAPHEIGHT-1:
                        newresources += tilemap[column][row+1].resources
                    else:
                        newresources += tilemap[column][0].resources

                    newresources /= 32.0
                    tilemap[column][row].resource_growth_rate = newresources
                    newresources += tilemap[column][row].resources

                    if newresources < 1 and newresources > 0:
                        tilemap[column][row].resources = newresources

                    t = tilemap[column][row]
                    t.resources = t.resources - t.consumption_rate
                    if(t.resources < 0):
                        t.resources = 0
                        t.consumption_rate = 0
                    t.growth_rate = (t.consumption_rate * t.resources) - (t.pop/16.0)
                    t.pop = t.pop + t.growth_rate
                    if t.pop > 1.0:
                        t.pop = 1.0
                        tilemap[column][row].color = (t.col_color[0]*t.pop, t.col_color[1]*t.pop, t.col_color[2]*t.pop)
                    elif t.pop <= 0.0001:
                        t.alive = False
                        t.color = (150, 150, 150)
                    else:
                        tilemap[column][row].color = (t.col_color[0]*t.pop, t.col_color[1]*t.pop, t.col_color[2]*t.pop)

                    #print column, row, t.growth_rate, t.pop, t.resources
                elif tilemap[column][row].alive == False:
                    tilemap[column][row].resources = 0
                    tilemap[column][row].population = 0
                    tilemap[column][row].color = (150, 150, 150)

def mouseHoverOver():
    for y in range(MAPHEIGHT):
        for x in range(MAPWIDTH):
            if pygame.mouse.get_pos()[0] >= x*TILESIZE and pygame.mouse.get_pos()[0] < (x+1)*TILESIZE:
                if pygame.mouse.get_pos()[1] >= y*TILESIZE and pygame.mouse.get_pos()[1] < (y+1)*TILESIZE:
                    return (x, y)
    return (-1, -1)

def printTilemap(t):
    for y in range(MAPHEIGHT):
        for x in range(MAPWIDTH):
            print round(t[x][y].resources, 1),
        print

def initColonies(t):
    for p in range(0, 4):
        successful = False
        while(successful == False):
            c = Colony.Colony()
            x = random.randint(0, MAPWIDTH-1)
            y = random.randint(0, MAPHEIGHT-1)
            c.coordinates = [x,y]
            if ((t[x][y].tile_type != 'water') and (t[x][y].tile_type != 'occupied')):
                newTile = Colony.Occ_Tile()
                newTile.tile_type = 'occupied'
                if(p == 0):
                    newTile.col_color = (255,0,0)
                if(p == 1):
                    newTile.col_color = (255,255,0)
                if(p == 2):
                    newTile.col_color = (255,0,255)
                if(p == 3):
                    newTile.col_color = (0,255,255)
                newTile.resources = t[x][y].resources
                newTile.pop = random.uniform(0.45, 0.75)
                newTile.consumption_rate = random.uniform(0.01, 0.1)
                newTile.growth_rate = 0
                newTile.color = (newTile.pop*newTile.col_color[0], newTile.pop*newTile.col_color[1], newTile.pop*newTile.col_color[2])
                newTile.alive = True
                newTile.resource_growth_rate = 0
                newTile.coordinates = [x, y]
                t[x][y] = newTile
                c.occupied_tiles.append(newTile)

                successful = True
        COLS.append(c)

def main():
    global MAPHEIGHT, MAPWIDTH, TILESIZE, tilemap, tilemap_save, textsurface, font, COLS
    #initialize tilemap
    for y in range(MAPHEIGHT):
        a = []
        for x in range(MAPWIDTH):
            tile = Ground_Tile()
            # tilemap[y][x] = tile
            a.append(tile)
        tilemap.append(a)

    fixMatrix(tilemap)
    initResources(tilemap)
    initWater(tilemap)
    growResourcesNearWater(tilemap)

    pygame.init()
    pygame.display.set_caption("Civilization V: Ultimate Edition")
    DISPLAYSURF = pygame.display.set_mode((MAPWIDTH*TILESIZE, MAPHEIGHT*TILESIZE))

    #allow map to be reinitialized with the 'r' key, hit enter to start and 'lock' the map
    tilemap_save = tilemap
    reinit = 0
    while(reinit == 0):
        for column in range(MAPWIDTH):
            for row in range(MAPHEIGHT):
                pygame.draw.rect(DISPLAYSURF, tilemap[column][row].color, (column*TILESIZE, row*TILESIZE, TILESIZE, TILESIZE))

        pygame.display.update()

        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()

        if(pygame.key.get_pressed()[pygame.K_r] != 0):
            for y in range(MAPHEIGHT):
                for x in range(MAPWIDTH):
                    tile = Ground_Tile()
                    tilemap[x][y] = tile
            initResources(tilemap)
            initWater(tilemap)
            growResourcesNearWater(tilemap)

        #sa'''ve the tilemap for later iterations
        if(pygame.key.get_pressed()[pygame.K_RETURN] != 0):
            reinit = 1
            tilemap_save = copy.deepcopy(tilemap)

            initColonies(tilemap)

    '''
        |~~~\/~~\/~~~\/~~\/~~~|~~~\/~~\/~~~\/~~\/~~~|~~~\/~~\/~~~\/~~\/~~~|
        | /\/ /\/ /~\/ /\/ /\ | /\/ /\/ /~\/ /\/ /\ | /\/ /\/ /~\/ /\/ /\ |
        | \/ /\/ /\_/ /\/ /\/ | \/ /\/ /\_/ /\/ /\/ | \/ /\/ /\_/ /\/ /\/ |
        \ \/\ \/\ | /\ \/\ \/~\ \/\ \/\ | /\ \/\ \/~\ \/\ \/\ | /\ \/\ \/
        /\ \/\ \/ | \/\ \/\ \_/\ \/\ \/ | \/\ \/\ \_/\ \/\ \/ | \/\ \/\ \
        | /\/ /\___|___/\/ /\___/\/ /\___|___/\/ /\___/\/ /\___|___/\/ /\ |
        | \/ /\/   |   \/ /\/   \/ /\/   |   \/ /\/   \/ /\/   |   \/ /\/ |
        \ \/\ \/\ | /\ \/\ \/~\ \/\ \/\ | /\ \/\ \/~\ \/\ \/\ | /\ \/\ \/
        /\ \/\ \/ | \/\ \/\ \_/\ \/\ \/ | \/\ \/\ \_/\ \/\ \/ | \/\ \/\ \
        | /\/ /\/ /~\/ /\/ /\ | /\/ /\/ /~\/ /\/ /\ | /\/ /\/ /~\/ /\/ /\ |
        | \/ /\/ /\_/ /\/ /\/ | \/ /\/ /\_/ /\/ /\/ | \/ /\/ /\_/ /\/ /\/ |
        |___/\__/\___/\__/\___|___/\__/\___/\__/\___|___/\__/\___/\__/\___|
    '''

    generations = 1
    max_time_steps = 15     # change as needed
#
    displayTile = (-1, -1) #what tile to display information on

    while True:     #tracks generations
    # while generations <= 1: # dbug
        print "---------------start generation", generations, "---------------"
        # initColonies(tilemap)
        print "beginning len():", len(COLS)
        print 'beg. loop: [res,  pop,  c_r,  g_r,  rgr]'
        for a in COLS:
            print "beg. loop:", a.X

        timestep = 0
        '''==================================================='''
        #tracks timesteps in each generation
        for timestep in range(1, max_time_steps+1):
            #end loop early if only one colony is still alive
            surviving = 0
            for a in COLS:
                if a.alive:
                    surviving += 1

            updateResources()

            for  i in range(0, len(COLS)):
                COLS[i].takeTurn(tilemap)


            for column in range(MAPWIDTH):
                for row in range(MAPHEIGHT):
                   pygame.draw.rect(DISPLAYSURF, tilemap[column][row].color, (column*TILESIZE, row*TILESIZE, TILESIZE, TILESIZE))

            #exit if 'x' is pressed or 'esc' key is pressed
            for event in pygame.event.get():
                if event.type == QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.MOUSEBUTTONDOWN:
                    displayTile = mouseHoverOver()

            if(pygame.key.get_pressed()[pygame.K_ESCAPE] != 0):
                pygame.quit()
                sys.exit()

            #reset the map if r is pressed
            if(pygame.key.get_pressed()[pygame.K_r] != 0):
                tilemap = copy.deepcopy(tilemap_save)

            #display the resources of a clicked-tile on the UI
            if displayTile != (-1, -1):
                xDT = displayTile[0]
                yDT = displayTile[1]
                string = "Resources: "
                textsurface = font.render(string + str(round(tilemap[xDT][yDT].resources, 4)), False, (255,255,255))
                DISPLAYSURF.blit(textsurface,(0,0))

                string = "Population: "
                textsurface = font.render(string + str(round(tilemap[xDT][yDT].pop, 4)), False, (255,255,255))
                DISPLAYSURF.blit(textsurface,(0, 35))

                string = "Consumption: "
                textsurface = font.render(string + str(round(tilemap[xDT][yDT].consumption_rate, 4)), False, (255,255,255))
                DISPLAYSURF.blit(textsurface,(0,70))

            textsurface = font.render("Generation: " + str(generations) + "    Time Steps: " + str(timestep), False, (255,255,255))
            DISPLAYSURF.blit(textsurface,(0, MAPHEIGHT*TILESIZE - 35))

            for i in range(len(COLS)):
                print 'f.m() COLS[i].X: {}'.format(COLS[i].X)
            print

            pygame.display.update()
            pass #end for loop

        # print '==============================================='
        tilemap = copy.deepcopy(tilemap_save)
        COLS = copy.deepcopy(Colony.findFittest(COLS, tilemap))
        # print len(COLS)

        # print "-----------------end generation {}----------------\n".format(generations)
        # initColonies(tilemap)
        generations += 1
        # raw_input('Enter to continue') # pause after
        pass #end while loop
pass #end main function

if __name__ == "__main__":
    main()
