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
tilemapSave = [[0 for x in range(MAPWIDTH)] for y in range(MAPHEIGHT)]


#initialize font
pygame.font.init()
font = pygame.font.SysFont('Arial', 30)
textsurface = font.render(' ', False, (255,255,255))

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
                if tilemap[column][row].tile_type == 'occupied':
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

                    newresources /= 128.0
                    newresources += tilemap[column][row].resources
                    
                    if newresources < 1:
                        tilemap[column][row].resources = newresources
                        if tilemap[column][row].tile_type != 'occupied':
                            tilemap[column][row].color = (0, 255*newresources, 0)


def mouseHoverOver(font, DISPLAYSURF):
    global textsurface
    textsurface = font.render(' ', False, (255,255,255))
    for y in range(MAPHEIGHT):
        for x in range(MAPWIDTH):
            if pygame.mouse.get_pos()[0] >= x*TILESIZE and pygame.mouse.get_pos()[0] < (x+1)*TILESIZE:
                if pygame.mouse.get_pos()[1] >= y*TILESIZE and pygame.mouse.get_pos()[1] < (y+1)*TILESIZE:
                    textsurface = font.render(str(round(tilemap[x][y].resources, 2)), False, (255,255,255))
    return textsurface


def splitPopulation(x, y):
    global tilemap
    tried = [0, 0, 0, 0]
    dirX = 0
    dirY = 0
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
        if(tilemap[x+dirX][y+dirY].tile_type == 'ground'):
            newTile = Occ_Tile()
            newTile.resources = tilemap[x+dirX][y+dirY].resources
            newTile.pop = tilemap[x][y].pop / 2.0
            newColor = tilemap[x][y].civColor
            newTile.color = (newColor[0]*newTile.pop, newColor[1]*newTile.pop, newColor[2]*newTile.pop)
            newTile.civColor = tilemap[x][y].civColor
            newTile.consumption_rate = tilemap[x][y].consumption_rate / 2.0
            newTile.growth_rate = tilemap[x][y].growth_rate / 2.0
            
            tilemap[x+dirX][y+dirY] = newTile
            
            tilemap[x][y].pop /= 2.0
            tilemap[x][y].consumption_rate /= 2.0
            tilemap[x][y].growth_rate /= 2.0
            p = tilemap[x][y].pop
            tilemap[x][y].color = (newColor[0]*p, newColor[1]*p, newColor[2]*p)
            child = tilemap[x+dirX][y+dirY]
            parent = tilemap[x][y]
            break 

def printTilemap(t):
    for y in range(MAPHEIGHT):
        for x in range(MAPWIDTH):
            print round(t[x][y].resources, 1),
        print

def main():
    global MAPHEIGHT
    global MAPWIDTH
    global TILESIZE
    global tilemap
    global tilemapSave
    global textsurface
    global font

    #initialize the font

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

        #save the tilemap for later iterations (May not work??)
        if(pygame.key.get_pressed()[pygame.K_RETURN] != 0):
            reinit = 1
            for y in range(MAPHEIGHT):
                for x in range(MAPWIDTH):
                    tilemapSave[x][y] = tilemap[x][y]
                    tilemapSave[x][y].tile_type = tilemap[x][y].tile_type
                    tilemapSave[x][y].resources = tilemap[x][y].resources
                    tilemapSave[x][y].color = tilemap[x][y].color
                    tilemapSave[x][y].pop = tilemap[x][y].pop
                    tilemapSave[x][y].consumption_rate = tilemap[x][y].consumption_rate
                    tilemapSave[x][y].growth_rate = tilemap[x][y].growth_rate
                    tilemapSave[x][y].civColor = tilemap[x][y].civColor

            #for testing
            occ = Occ_Tile()
            occ.resources = tilemap[50][50].resources
            occ.pop = 0.8
            occ.consumption_rate = 0.01
            occ.growth_rate = 0.01
            occ.color = (255*occ.pop, 0*occ.pop, 0*occ.pop)
            occ.civColor = (255, 0, 0)
            tilemap[50][50] = occ


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
    printTilemap(tilemap)
    print
    printTilemap(tilemapSave)
    i = 0
    while True:

        #sleep for half a second, change this later when we invent time
        time.sleep(1) 

        updateResources()
        #print i
        i += 1

        if(i > 5):
            splitPopulation(50, 50)

        #draw map
        for column in range(MAPWIDTH):
            for row in range(MAPHEIGHT):
                pygame.draw.rect(DISPLAYSURF, tilemap[column][row].color, (column*TILESIZE, row*TILESIZE, TILESIZE, TILESIZE))

        #exit if 'x' is pressed or 'esc' key is pressed
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                textsurface = mouseHoverOver(font, DISPLAYSURF)

        if(pygame.key.get_pressed()[pygame.K_ESCAPE] != 0):
            pygame.quit()
            sys.exit()

        #reset the map if r is pressed (DOES NOT WORK..yet)
        if(pygame.key.get_pressed()[pygame.K_r] != 0):
            for y in range(MAPHEIGHT):
                for x in range(MAPWIDTH):
                    tilemap[x][y] = tilemapSave[x][y]
                    tilemap[x][y].tile_type = tilemapSave[x][y].tile_type
                    tilemap[x][y].resources = tilemapSave[x][y].resources
                    tilemap[x][y].pop = tilemapSave[x][y].pop
                    tilemap[x][y].consumption_rate = tilemapSave[x][y].consumption_rate
                    tilemap[x][y].growth_rate = tilemapSave[x][y].growth_rate
                    tilemap[x][y].color = tilemapSave[x][y].color
                    tilemap[x][y].civColor = tilemapSave[x][y].civColor
                    if tilemap[x][y].tile_type == 'occupied':
                        print x, y

        #display the resources of a clicked-tile on the UI
        DISPLAYSURF.blit(textsurface,(0,0))
       
        pygame.display.update()

if __name__ == "__main__":
    main()
