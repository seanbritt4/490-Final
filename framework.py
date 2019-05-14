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
tilemap = [[0 for x in range(MAPWIDTH)] for y in range(MAPHEIGHT)]
tilemapSave = [[0 for x in range(MAPWIDTH)] for y in range(MAPHEIGHT)]

CIVS = []

#initialize font
pygame.font.init()
font = pygame.font.SysFont('Arial', 30)
textsurface = font.render(' ', False, (255,255,255))

def splitPopulation(c):
    global tilemap

    print 'f.sP(): ', c,
    print c.occupied_tiles
    tried = [0, 0, 0, 0]
    dirX = 0
    dirY = 0
    # if(tilemap[x][y].tile_type == 'occupied' and tilemap[x][y].alive == True):
    for tile in c.occupied_tiles:
        sc = random.uniform(0.0, 1.0)
        if sc >= c.split_chance:
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
                            dirY = 1
                            dirX = 0
                        if(direction == 1):
                            dirX = 1
                            dirY = 0
                        if(direction == 2):
                            dirY = -1
                            dirX = 0
                        if(direction == 3):
                            dirX = -1
                            dirY = 0
                #if(x > 0 and x < MAPWIDTH-1 and y > 0 and y < MAPHEIGHT -1):
                newX = x+dirX
                newY = y+dirY
                if(x+dirX < 0):
                    newX = MAPWIDTH -1
                if(x+dirX > MAPWIDTH-1):
                    newX = 0
                if(y+dirY < 0):
                    newY = MAPHEIGHT -1
                if(y+dirY > MAPHEIGHT-1):
                    newY = 0
                if(tilemap[newX][newY].tile_type == 'ground'):
                    newTile = cluster.Occ_Tile()
                    newTile.resources = tilemap[newX][newY].resources
                    newTile.pop = tilemap[x][y].pop / 2.0
                    newColor = tilemap[x][y].civColor
                    newTile.color = (newColor[0]*newTile.pop, newColor[1]*newTile.pop, newColor[2]*newTile.pop)
                    newTile.civColor = tilemap[x][y].civColor
                    newTile.consumption_rate = tilemap[x][y].consumption_rate
                    newTile.growth_rate = tilemap[x][y].growth_rate / 2.0
                    newTile.resource_growth_rate = 0
                    newTile.alive = True
                    tilemap[newX][newY] = newTile

                    tilemap[x][y].pop /= 2.0
                    tilemap[x][y].growth_rate /= 2.0
                    p = tilemap[x][y].pop
                    tilemap[x][y].color = (newColor[0]*p, newColor[1]*p, newColor[2]*p)
                    child = tilemap[newX][newY]
                    parent = tilemap[x][y]
                    break


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

                    newresources /= 16.0
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
            civ = Colony.Colony()
            x = random.randint(0, MAPWIDTH-1)
            y = random.randint(0, MAPHEIGHT-1)
            # civ.map_location = [x,y] #do we want random positions everytime?
            if(t[x][y].tile_type != 'water'):
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
                civ.occupied_tiles.append(newTile)
                t[x][y] = newTile

                successful = True
        CIVS.append(civ)


def main():
    global MAPHEIGHT, MAPWIDTH, TILESIZE, tilemap, tilemapSave, textsurface, font, CIVS

    #initialize tilemap
    for y in range(MAPHEIGHT):
        for x in range(MAPWIDTH):
            tile = Ground_Tile()
            tilemap[y][x] = tile

    fixMatrix(tilemap)
    initResources(tilemap)
    initWater(tilemap)
    growResourcesNearWater(tilemap)

    pygame.init()
    pygame.display.set_caption("Civilization V: Ultimate Edition")
    DISPLAYSURF = pygame.display.set_mode((MAPWIDTH*TILESIZE, MAPHEIGHT*TILESIZE))

    #allow map to be reinitialized with the 'r' key, hit enter to start and 'lock' the map
    tilemapSave = tilemap
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

        #save the tilemap for later iterations
        if(pygame.key.get_pressed()[pygame.K_RETURN] != 0):
            reinit = 1
            tilemapSave = copy.deepcopy(tilemap)

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
    max_time_steps = 25 #change as needed
#
    displayTile = (-1, -1) #what tile to display information on

    # while True:     #tracks generations
    while generations <= 3: # dbug
        print "---------------start generation---------------"
        timestep = 0
        #tracks timesteps in each generation
        for timestep in range(0, max_time_steps):
            updateResources()

            #draw map (and split, for testing purposes DELETE THAT LATER of course :)
            # for column in range(MAPWIDTH):
            #     for row in range(MAPHEIGHT):
            #         if(tilemap[column][row].tile_type == 'occupied' and tilemap[column][row].alive == True):
            #             splitPopulation(column, row)

            for  i in range(0, len(CIVS)):
                CIVS[i].takeTurn()

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
                tilemap = copy.deepcopy(tilemapSave)

            #display the resources of a clicked-tile on the UI
            if displayTile != (-1, -1):
                xDT = displayTile[0]
                yDT = displayTile[1]
                string = "Resources: "
                textsurface = font.render(string + str(round(tilemap[xDT][yDT].resources, 2)), False, (255,255,255))
                DISPLAYSURF.blit(textsurface,(0,0))

                string = "Population: "
                textsurface = font.render(string + str(round(tilemap[xDT][yDT].pop, 2)), False, (255,255,255))
                DISPLAYSURF.blit(textsurface,(0, 35))

            textsurface = font.render("Generation: " + str(generations) + "    Time Steps: " + str(timestep), False, (255,255,255))
            DISPLAYSURF.blit(textsurface,(0, MAPHEIGHT*TILESIZE - 35))

            '''possibly save run & computation time?'''
            # if (generations % 10) == 0: # update display every 10 generations
            if (timestep % 1) == 0:  #update display every 10 timesteps
                pygame.display.update()
            # print len(CIVS[0].occupied_tiles)
            # raw_input()
            pass #end for loop

        tilemap = copy.deepcopy(tilemapSave)
        generations += 1
        for a in CIVS:
            print a.X

        print "-----------------end generation---------------"
        CIVS = Colony.findFittest(CIVS)
        for a in CIVS:
            print a.X
        pass #end while loop
pass #end main function

if __name__ == "__main__":
    main()
