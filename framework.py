import pygame, sys, time, random, math
from pygame.locals import *
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

#RESOURCE_MODIFIER = 0.1
#WATER_PASS_AMOUNT = 3
#WATER_MODIFIER = 0.01
#NEAR_WATER_GROWTH = 1.4

RESOURCE_MODIFIER = 0.1
WATER_PASS_AMOUNT = 3
WATER_MODIFIER = 0.01
NEAR_WATER_GROWTH = 1.4

#array of tile objects
tilemap = [[0 for x in range(MAPWIDTH)] for y in range(MAPHEIGHT)]


'''
Ignore everything you see until you get to the game loop, this code is awful
and should not be looked at by anyone, by tommorow I will have mostly forgotten
what it does.
'''

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
    tilemap[curX][curY].resources = round(random.uniform(0.0, 0.15), 2)
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




def main():
    global MAPHEIGHT
    global MAPWIDTH
    global TILESIZE
    global tilemap

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

        if(pygame.key.get_pressed()[pygame.K_RETURN] != 0):
            reinit = 1
            tilemapSave = tilemap

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
    while True:
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
        if(pygame.key.get_pressed()[pygame.K_ESCAPE] != 0):
            pygame.quit()
            sys.exit()

        #sleep for half a second, change this later when we invent time
        time.sleep(0.5) 
 
        for column in range(MAPWIDTH):
            for row in range(MAPHEIGHT):
                pygame.draw.rect(DISPLAYSURF, tilemap[column][row].color, (column*TILESIZE, row*TILESIZE, TILESIZE, TILESIZE))

        pygame.display.update()

if __name__ == "__main__":
    main()
