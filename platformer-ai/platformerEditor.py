import pygame
import random
import math
import copy

# initializing pygame
pygame.init()

# initializing screen sizes and display width
dh = 650                #display size
dw = 1300
roomwidth = 2500        #room size
roomheight = dh

# Longest path size for pathfinding algorithm
pathmax = 100 * roomwidth

# color RGB codes
black = (0,0,0)
white = (255,255,255)
red = (255,0,0)

#font definitions
font = pygame.font.Font('freesansbold.ttf', 50)
font2 = pygame.font.Font('freesansbold.ttf', 100)

# initializing the pygame display and clock
gameDisplay = pygame.display.set_mode((dw, dh))
pygame.display.set_caption('platformer')
clock = pygame.time.Clock()

##############################################################################################################
##############################################################################################################
#initializing all sprites used by the game
# make sure you have all images used in this game saved in the same directory
# as the game code or put the directories into the load command

leveleditor = pygame.image.load('leveleditor.png')
leveledwid = 600
leveledhi = 170
leveleditorx = dw/2 - leveledwid/2
leveleditory = 2*(dh/3) - leveledhi/2

select = pygame.image.load('select.png')
selectwid = 245
selecthi = 85
selectx = 25
selecty = 0

quickplay = pygame.image.load('quickplay.png')
quickplaywid = 500
quickplayhi = 120
quickplayx = dw/3 - quickplaywid/2 - 50
quickplayy = dh/3 - quickplayhi/2

quickai = pygame.image.load('quick AI.png')
quickaiwid = 500
quickaihi = 120
quickaix = 2*(dw/3) - quickplaywid/2 + 50
quickaiy = dh/3 - quickaihi/2


welcome = pygame.image.load('welcome.png')
welcomewid = 1000
welcomehi = 80
welcomex = dw/2 - welcomewid/2
welcomey = 0

userplay = pygame.image.load('userplay.png')
userplaywid = 260
userplayhi = 85
userplayx = 1000
userplayy = 0

aifinish = pygame.image.load('aifinish.png')
aifinishwid = 260
aifinishhi = 85
aifinishx = 1000
aifinishy = 100

ailearn = pygame.image.load('ailearn.png')
ailearnwid = 260
ailearnhi = 85
ailearnx = 1000
ailearny = 200

savelevel = pygame.image.load('savelevel.png')
savelevelsize = [260,80]
savelevelpos = [700,0]

resetlevel = pygame.image.load('reset.png')
resetsize = [260,80]
resetpos = [700,100]

setdefault = pygame.image.load('setdefault.png')
setdefaultsize = [260,80]
setdefaultpos = [700,200]

normblock = pygame.image.load('Normal Block.png')
normblocksize = 50
groundheight = normblocksize

smallblock = pygame.image.load('small block.png')
smallblocksize = 25

stillguy = pygame.image.load('man still.png').convert_alpha()
manwid = 20
manhi = 50

stillguyred = pygame.image.load('man still red.png')


smallman = pygame.image.load('smallman.png')
smallmanwid = 10
smallmanhi = 25

enemy = pygame.image.load('enemy.png').convert_alpha()
enemywid = 30
enemyhi = 30

flagpole = pygame.image.load('flagpole.png').convert_alpha()
flagsize = [60,200]
flagoffset = [25,0]

flagpolesmall = pygame.image.load('flagpolesmall.png').convert_alpha()
smallflagsize = [30,100]

coin = pygame.image.load('coin.png').convert_alpha()
coinsize = [45,45]

coinsmall = pygame.image.load('coinsmall.png').convert_alpha()
smallcoinsize = [22,22]

coinscoreim = pygame.image.load('coinscore.png').convert_alpha()
coinscoresize = [92,46]
coinscorepos = [1100,0]

wincondition = pygame.image.load('win condition.png')
winconditionsize = [293,58]
winconditionpos = [320,10]

shortestdist = pygame.image.load('Shortest Distance.png')
shortdistsize = [318,58]
shortdistpos = [320,110]

shortpath = pygame.image.load('Shortest Path.png').convert_alpha()
shortpathsize = [293,58]
shortpathpos = [320,210]

smallenemy = pygame.image.load('smallenemy.png')
smallenemysize = 15

# End of sprites
##############################################################################################################
##############################################################################################################

# buffer values

collisionbuff = 2       # buffer for all collisions
maxspeed = 3            # max vertical speed so does not got through ground
maxenemyspeed = 1

# list of output characteristics that need to be saved individually, used later in quickAIloop around line 1000
speciallist = [18,19,20,21,22,23,24,25,26]

##############################################################################################################
# default object spawns:
# block list entries are modular so use integers 1, 2 .....
# block list: each elelemt [xpos (starts left),ypos (starts top),horizontal direction (1 = left, -1 = right),
# vertical direction (1 = down, -1 = up), length]
defaultblocklist = [[-1, 12, 0, -1, 15], [0, dh / normblocksize - 1, 1, 0, round(roomwidth / normblocksize)], [5, 8, 1, 0, 5],
             [15, 5, 1, 0, 5], [15, 6, 0, 1, 6], [27, 11, 0, 1, 1], [31, 8, 1, 0, 5], [40, 7, 1, 0, 5],
             [44, 11, 0, -1, 4]]
# [xpos(pixel from left),ypos(pixel from top)]
defaultenemylist = [[1000, 500], [1600, 320], [2000, 270]]
defaultcoinslist = [[500,200]]
defaultmanpos = [0,dh - normblocksize - manhi]
defaultflagpos = [2400,400]
#end of object spawns
##############################################################################################################

##############################################################################################################
# initialization for user level maker
gridtop = 300       #spawn location (top left) by pixels of grid
gridleft = 25
topleft = [gridleft, gridtop]
botright = [gridleft + roomwidth * (smallblocksize / normblocksize), gridtop + dh * (smallblocksize / normblocksize)]

# the following position arrays follow the same format as above
# initializing saved positions used in user maker
savedmanpos = [1, int((botright[1] - topleft[1]) / smallblocksize) - 2]
savedflagpos = [int((botright[0] - topleft[0]) / smallblocksize) - 3, int((botright[1] - topleft[1]) / smallblocksize) - 5]
savedblocks = [[0, 0, 0, 1, int((botright[1] - topleft[1]) / smallblocksize)],
          [0, 0, 1, 0, int((botright[0] - topleft[0]) / smallblocksize) * 0],
          [0, int((botright[1] - topleft[1]) / smallblocksize) - 1, 1, 0,
           int((botright[0] - topleft[0]) / smallblocksize)],
          [int((botright[0] - topleft[0]) / smallblocksize) - 1, 0, 0, 1,
           int((botright[1] - topleft[1]) / smallblocksize)]]
savedenemies = []
savedcoins = []

# initializing reset positions for user maker
resetmanpos = [1, int((botright[1] - topleft[1]) / smallblocksize) - 2]
resetflagpos = [int((botright[0] - topleft[0]) / smallblocksize) - 3, int((botright[1] - topleft[1]) / smallblocksize) - 5]
resetblocks = [[0, 0, 0, 1, int((botright[1] - topleft[1]) / smallblocksize)],
          [0, 0, 1, 0, int((botright[0] - topleft[0]) / smallblocksize) * 0],
          [0, int((botright[1] - topleft[1]) / smallblocksize) - 1, 1, 0,
           int((botright[0] - topleft[0]) / smallblocksize)],
          [int((botright[0] - topleft[0]) / smallblocksize) - 1, 0, 0, 1,
           int((botright[1] - topleft[1]) / smallblocksize)]]
resetenemies = []
resetcoins = []
# end of user lever maker initialization
##############################################################################################################

##############################################################################################################
##############################################################################################################
# Shortest path algorithm
#
# Converting blocklist into a grid of 1's and 0's
def convertblockslisttogrid(blocklist):
    grid = []
    for i in range(0,int(roomwidth/normblocksize)):
        grid.append([])
        for _ in range(0,int(roomheight/normblocksize)):
            grid[i].append(0)
    for blocks in blocklist:
        for i in range(0,blocks[4]):
            grid[int(blocks[0]+i*blocks[2])][int(blocks[1]+i*blocks[3])] = 1
    return grid
# Converting a general position into a grid location (x,y) [from top left]
def convertgridpos(thingpos,thingsize):
    return [int((thingpos[0]+thingsize[0]/2)/normblocksize),int((thingpos[1]+thingsize[1]/2)/normblocksize)]
# algorithm for shortest pathfinding
def findshortestpath(playerpos,flagpos,grid):
    playergridpos = []
    playergridpos.append(convertgridpos(playerpos,[manwid,manhi]))  # start with current grid position
    flaggridpos = convertgridpos(flagpos,flagsize)  # final goal grid position
    length = 0  # variable used to store how much extension is needed ie shortest path
    finalpos = [playergridpos[0][0],playergridpos[0][1]]    # final position so know when to add to length
    for locations in playergridpos:                         # search through the grid positions (recursively)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()

        if locations[0] == flaggridpos[0] and locations[1] == flaggridpos[1]:       # if on flag end loop
            return length
        ##############################
        # list extending algorithm
        # checking if blocks are around current position, if not check if
        # position already exists in list, if not, then add to list
        if grid[locations[0]+1][locations[1]] == 0:
            flag = 0
            for positions in playergridpos:
                if locations[0]+1 == positions[0] and locations[1] == positions[1]:
                    flag = 1
                    break
            if flag == 0:
                playergridpos.append([locations[0]+1,locations[1]])

        if grid[locations[0]-1][locations[1]] == 0:
            flag = 0
            for positions in playergridpos:
                if locations[0] - 1 == positions[0] and locations[1] == positions[1]:
                    flag = 1
                    break
            if flag == 0:
                playergridpos.append([locations[0]-1,locations[1]])

        if grid[locations[0]][locations[1]+1] == 0:
            flag = 0
            for positions in playergridpos:
                if locations[0] == positions[0] and locations[1]+1 == positions[1]:
                    flag = 1
                    break
            if flag == 0:
                playergridpos.append([locations[0],locations[1]+1])

        if grid[locations[0]][locations[1]-1] == 0 and locations[1]>0:
            flag = 0
            for positions in playergridpos:
                if locations[0] == positions[0] and locations[1]-1 == positions[1]:
                    flag = 1
                    break
            if flag == 0:
                playergridpos.append([locations[0],locations[1]-1])
        # end of list extending algorithm
        ###########################################################
        # if at previous end of list, then increment length and
        # store new end of list
        if locations[0] == finalpos[0] and locations[1] == finalpos[1]:
            length = length +1
            finalpos = [playergridpos[-1][0],playergridpos[-1][1]]

    return (pathmax)            # if no path found, return very large number so it knows no solution

# is the mouse over a given object
def mouseon(mousepos,thingpos,thingsize):  #([mouse x,mouse y],[thing x,thing y],[thingwid,thinghi]).
    if (mousepos[0] > thingpos[0] and mousepos[0]< thingpos[0] + thingsize[0]) and (
            mousepos[1] > thingpos[1] and mousepos[1]< thingpos[1] + thingsize[1]):
        return 1
    else:
        return 0

#drawing the grid for the user maker loop
def drawgrid(topleft, botright, gridsize,width): #([topleft x , topleft y],[bottom right x, bottom right y],grid spacing, width of line)
    for i in range(0,int((botright[0]-topleft[0])/gridsize)+1):
        pygame.draw.line(gameDisplay,black, (topleft[0] + gridsize*i,topleft[1]),(topleft[0] + gridsize*i,botright[1]),width)
    for i in range(0,int((botright[1]-topleft[1])/gridsize)+1):
        pygame.draw.line(gameDisplay,black, (topleft[0],topleft[1]+ gridsize*i),(botright[0],topleft[1]+ gridsize*i),width)

##############################################################################################################
# sprite display funcions

def drawman(x,y):
    gameDisplay.blit(stillguy, (x, y))

def drawmanred(x,y):
    gameDisplay.blit(stillguyred, (x, y))

def drawsmallman(x,y):
    gameDisplay.blit(smallman, (x, y))

def drawblock(x,y):
    gameDisplay.blit(normblock, (x, y))

def drawflag(flagpos,camerax,cameray):
    gameDisplay.blit(flagpole,(flagpos[0]+dw/2-camerax,flagpos[1]+dh/2-cameray))

def drawsmallflag(flagpos):
    gameDisplay.blit(flagpolesmall,(flagpos[0],flagpos[1]))

def drawblockstrips(blocklist,camerax,cameray):  # block list: each elelemt [xpos,ypos,horizontal direction,vertical direction, length]
    for blocks in blocklist:
        for i in range(0,blocks[4]):
            drawblock((blocks[0]*normblocksize+blocks[2]*normblocksize*i)+dw/2-camerax,(blocks[1]*normblocksize+blocks[3]*normblocksize*i)+dh/2-cameray)

def drawsmallblock(x, y):
    gameDisplay.blit(smallblock, (x, y))

def drawsmallblockstrips(blocklist, camerax,cameray):  # block list: each elelemt [xpos,ypos,horizontal direction,vertical direction, length]
    for blocks in blocklist:
        for i in range(0, blocks[4]):
            drawsmallblock((blocks[0] * smallblocksize + blocks[2] * smallblocksize * i)+camerax,
                      (blocks[1] * smallblocksize + blocks[3] * smallblocksize * i) + cameray)

def drawenemy(x,y):
    gameDisplay.blit(enemy, (x, y))

def drawenemies(enemylist,camerax,cameray): # enemy list: each element [enemy x, enemy y]
    for enemies in enemylist:
        drawenemy(enemies[0]+dw/2-camerax,enemies[1]+dh/2-cameray)

def drawsmallenemy(x,y):
    gameDisplay.blit(smallenemy, (x, y))

def drawsmallenemies(enemylist,camerax,cameray):# enemy list: each element [enemy x grid, enemy y grid]
    for enemies in enemylist:
        drawsmallenemy(enemies[0]*smallblocksize+camerax + smallenemysize/2,enemies[1]*smallblocksize+smallenemysize/2+cameray)

def drawcoin(x,y):
    gameDisplay.blit(coin, (x, y))

def drawcoins(coinlist,camerax,cameray):    # coin list: [coin x, coin y]
    for coins in coinlist:
        drawcoin(coins[0]+dw/2-camerax,coins[1]+dh/2-cameray)

def drawsmallcoin(x,y):
    gameDisplay.blit(coinsmall, (x, y))

def drawsmallcoins(coinlist,camerax,cameray): # coint list [coin x grid, coin y grid]
    for coins in coinlist:
        drawsmallcoin(coins[0]*smallblocksize+camerax+2,coins[1]*smallblocksize+cameray + 2)

def drawcoinscore(coinpos):
    gameDisplay.blit(coinscoreim,(coinpos[0],coinpos[1]))

def displaycoinscore(score,coinpos):
    text = font.render(str(score),True,black)
    gameDisplay.blit(text,(coinpos[0]+coinscoresize[0],coinpos[1]))

# end of sprite display functions
##############################################################################################################
# distance between two points on the screen
def distancebetween(firstpos,secondpos):
    return (math.sqrt((firstpos[0]-secondpos[0])**2+(firstpos[1]-secondpos[1])**2))

# check circular collision between two objects, (are their centres too close)
def generalcirclecollision(firstpos,firstrad,secondpos,secondrad):
    if distancebetween(firstpos,secondpos) <= firstrad+secondrad:
        return 1
    else:
        return 0

##############################################################################################################
# main menu loop:
def mainmenu():
    mousepos = pygame.mouse.get_pos()       # getting initial mouse position and button status
    mousebuttons = pygame.mouse.get_pressed()   # position: [x,y] , buttons (0 or 1) [Left, right, middle]
    while 1 == 1:
        for event in pygame.event.get():
            # if mouse attributes change, record the new values
            if event.type == pygame.MOUSEMOTION:
                mousepos = pygame.mouse.get_pos()
            if event.type == pygame.MOUSEBUTTONUP:
                mousebuttons = pygame.mouse.get_pressed()
            if event.type == pygame.MOUSEBUTTONDOWN:
                mousebuttons = pygame.mouse.get_pressed()
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()

        # cecking is mouse left button is pressed and mouse is over a command block
        # return the code for executing the command in the main game loop
        if mouseon(mousepos,[leveleditorx,leveleditory],[leveledwid,leveledhi]) and mousebuttons[0] == 1:
            return 1
        if mouseon(mousepos,[quickplayx,quickplayy],[quickplaywid,quickplayhi]) and mousebuttons[0] == 1:
            return 2
        if mouseon(mousepos,[quickaix,quickaiy],[quickaiwid,quickaihi]) and mousebuttons[0] == 1:
            return 3

        # pygame dislay
        gameDisplay.fill(white)
        gameDisplay.blit(leveleditor,(leveleditorx,leveleditory))
        gameDisplay.blit(welcome, (welcomex, welcomey))
        gameDisplay.blit(quickplay, (quickplayx, quickplayy))
        gameDisplay.blit(quickai, (quickaix, quickaiy))
        pygame.display.update()
#end of main menu loop
##############################################################################################################

##############################################################################################################
# loop for user creating levels
def leveleditorloop():

    # get current mouse stats
    # position [x,y] buttons (0 or 1) [Left, right, middle]
    mousepos = pygame.mouse.get_pos()
    mousebuttons = pygame.mouse.get_pressed()

    # setting initial positions for display items
    guydispx = 70
    guydispy = 100
    enemydispx = 130
    enemydispy = 115
    blockdispx = 150
    blockdispy = 190
    coindispx = 190
    coindispy = 120
    flagdispx = 65
    flagdispy = 170
    enemyoffset = 0.2
    flagoffset = 0.4

    ##############################################################################################################
    # copying the input arguments so that they are preserved as global variables
    manpos = copy.deepcopy(savedmanpos)
    flagpos = copy.deepcopy(savedflagpos)
    blocks = copy.deepcopy(savedblocks)
    enemies = copy.deepcopy(savedenemies)
    coins = copy.deepcopy(savedcoins)

    manpostempsaved = copy.deepcopy(savedmanpos)
    flagpostempsaved = copy.deepcopy(savedflagpos)
    blockstempsaved = copy.deepcopy(savedblocks)
    enemiestempsaved = copy.deepcopy(savedenemies)
    coinstempsaved = copy.deepcopy(savedcoins)

    manpostempdef = copy.deepcopy(defaultmanpos)
    flagpostempdef = copy.deepcopy(defaultflagpos)
    blockstempdef = copy.deepcopy(defaultblocklist)
    enemiestempdef = copy.deepcopy(defaultenemylist)
    coinstempdef = copy.deepcopy(defaultcoinslist)
    ##############################################################################################################

    wintype = 2     # type of win condition for the genetic algorithm
    objtype = 0     # type of object being placed
    rectbuffer = 12 # buffer for rectangular display outline
    rectwid = 7     # width of the rectangular outline
    while 1 == 1:
        for event in pygame.event.get():
            #####################################################################
            # use key inputs to change type of block being placed
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_q:
                    return -1,[manpostempsaved,flagpostempsaved,blockstempsaved,enemiestempsaved,coinstempsaved],[manpostempdef,flagpostempdef,blockstempdef,enemiestempdef,coinstempdef]
                if event.key == pygame.K_n:
                    objtype = 0
                if event.key == pygame.K_b:
                    objtype = 1
                if event.key == pygame.K_e:
                    objtype = 2
                if event.key == pygame.K_m:
                    objtype = 3
                if event.key == pygame.K_f:
                    objtype = 4
                if event.key == pygame.K_c:
                    objtype = 5
            ##############################################################################################################

            ##############################################################################################################
            # update mouse stats if changed
            if event.type == pygame.MOUSEMOTION:
                mousepos = pygame.mouse.get_pos()
            if event.type == pygame.MOUSEBUTTONUP:
                mousebuttons = pygame.mouse.get_pressed()
            if event.type == pygame.MOUSEBUTTONDOWN:
                mousebuttons = pygame.mouse.get_pressed()
            ##############################################################################################################
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
        ##############################################################################################################
        # placing objects on the screen to create level
        # if mouse button is pressed and within the bounds of the level maker grid
        if mouseon(mousepos,[topleft[0],topleft[1]],[botright[0]-topleft[0],botright[1]-topleft[1]]) and mousebuttons[0]==1:
            # use flag to check is block is not available to be placed
            # to prevent repeated instances on the same space
            flag = 0
            ####################################################################
            # check if empty:
            # check if on the border of the level
            if int((mousepos[0] - topleft[0]) / smallblocksize)<1 or int((mousepos[0] - topleft[0]) / smallblocksize)>= int(
                    roomwidth/normblocksize)-1:
                flag = 1
            if int((mousepos[1] - topleft[1]) / smallblocksize)>=int(roomheight/normblocksize)-1:
                flag = 1
            # check if on an existing block string
            for block in blocks:
                if block == [int((mousepos[0] - topleft[0]) / smallblocksize),
                             int((mousepos[1] - topleft[1]) / smallblocksize), 0, 1, 1]:
                    flag = 1
            # check if on an existing enemy
            for enemy in enemies:
                if enemy == [int((mousepos[0] - topleft[0]) / smallblocksize),
                             int((mousepos[1] - topleft[1]) / smallblocksize)]:
                    flag = 1
            # check if on an existing coin
            for coin in coins:
                if coin == [int((mousepos[0] - topleft[0]) / smallblocksize),
                            int((mousepos[1] - topleft[1]) / smallblocksize)]:
                    flag = 1
            #########################################################################################################

            #########################################################################################################
            # if square is empty add the current type of object at that position
            if objtype == 1:
                if flag == 0:
                    blocks.append([int((mousepos[0]-topleft[0])/smallblocksize),int((mousepos[1]-topleft[1])/smallblocksize),0,1,1])
            if objtype == 2:
                if flag == 0:
                    enemies.append(
                    [int((mousepos[0] - topleft[0]) / smallblocksize), int((mousepos[1] - topleft[1]) / smallblocksize)])
            if objtype == 3:
                if flag == 0:
                    manpos = [int((mousepos[0] - topleft[0]) / smallblocksize), int((mousepos[1] - topleft[1]) / smallblocksize)]
            if objtype == 4:
                if flag == 0:
                    flagpos = [int((mousepos[0] - topleft[0]) / smallblocksize), int((mousepos[1] - topleft[1]) / smallblocksize)]
            if objtype == 5:
                if flag == 0:
                    coins.append(
                    [int((mousepos[0] - topleft[0]) / smallblocksize), int((mousepos[1] - topleft[1]) / smallblocksize)])
            ######################################################################################################

        ##############################################################################################################
        # if right click then delete object at that location
        if mouseon(mousepos,[topleft[0],topleft[1]],[botright[0]-topleft[0],botright[1]-topleft[1]]) and mousebuttons[2]==1:
            # use delete index to find if an element exists at that location
            # if an instance is found at the current location, delete that index
            deleteindex = -1
            for i in range(0,len(blocks)):
                if blocks[i] == [int((mousepos[0]-topleft[0])/smallblocksize),int((mousepos[1]-topleft[1])/smallblocksize),0,1,1]:
                    deleteindex = i
            if deleteindex >=0:
                del blocks[deleteindex]

            deleteindex = -1
            for i in range(0, len(enemies)):
                if enemies[i] == [int((mousepos[0] - topleft[0]) / smallblocksize),
                                 int((mousepos[1] - topleft[1]) / smallblocksize)]:
                    deleteindex = i
            if deleteindex >= 0:
                del enemies[deleteindex]

            deleteindex = -1
            for i in range(0, len(coins)):
                if coins[i] == [int((mousepos[0] - topleft[0]) / smallblocksize),
                                  int((mousepos[1] - topleft[1]) / smallblocksize)]:
                    deleteindex = i
            if deleteindex >= 0:
                del coins[deleteindex]
        ##############################################################################################################

        ##############################################################################################################
        # if mouse clicks on a type of object, change the placing object type
        if mouseon(mousepos, [blockdispx, blockdispy], [normblocksize, normblocksize]) and mousebuttons[0] == 1:
            objtype = 1
        if mouseon(mousepos, [enemydispx, enemydispy], [enemywid, enemyhi]) and mousebuttons[0] == 1:
            objtype = 2
        if mouseon(mousepos, [guydispx, guydispy], [manwid, manhi]) and mousebuttons[0] == 1:
            objtype = 3
        if mouseon(mousepos, [flagdispx, flagdispy], smallflagsize) and mousebuttons[0] == 1:
            objtype = 4
        if mouseon(mousepos, [coindispx, coindispy], smallcoinsize) and mousebuttons[0] == 1:
            objtype = 5
        ##############################################################################################################

        # mouse clicking on changing win condition type
        if mouseon(mousepos, shortpathpos, shortpathsize) and mousebuttons[0] == 1:
            wintype = 1
        if mouseon(mousepos, shortdistpos, shortdistsize) and mousebuttons[0] == 1:
            wintype = 2

        ##############################################################################################################
        # reset lists, save lists using the global and temp variables
        if mouseon(mousepos, resetpos, resetsize) and mousebuttons[0] == 1:
            manpos = copy.deepcopy(resetmanpos)
            flagpos = copy.deepcopy(resetflagpos)
            blocks = copy.deepcopy(resetblocks)
            enemies = copy.deepcopy(resetenemies)
            coins = copy.deepcopy(resetcoins)

        if mouseon(mousepos, savelevelpos, savelevelsize) and mousebuttons[0] == 1:
            manpostempsaved = copy.deepcopy(manpos)
            flagpostempsaved = copy.deepcopy(flagpos)
            blockstempsaved = copy.deepcopy(blocks)
            enemiestempsaved = copy.deepcopy(enemies)
            coinstempsaved = copy.deepcopy(coins)

        if mouseon(mousepos, setdefaultpos, setdefaultsize) and mousebuttons[0] == 1:
            manpostempdef = copy.deepcopy(manpos)
            flagpostempdef = copy.deepcopy(flagpos)
            blockstempdef = copy.deepcopy(blocks)
            enemiestempdef = copy.deepcopy(enemies)
            coinstempdef = copy.deepcopy(coins)
            ##########################################################################################################
            # converting grid positions to absolute locations
            manpostempdef[0] = manpostempdef[0] * normblocksize
            manpostempdef[1] = manpostempdef[1] * normblocksize
            flagpostempdef[0] = flagpostempdef[0] * normblocksize + normblocksize*flagoffset
            flagpostempdef[1] = flagpostempdef[1] * normblocksize
            for enemy in enemiestempdef:
                enemy[0] = enemy[0] * normblocksize + enemyoffset * normblocksize
                enemy[1] = enemy[1] * normblocksize + enemyoffset * normblocksize
            for coin in coinstempdef:
                coin[0] = coin[0] * normblocksize
                coin[1] = coin[1] * normblocksize
            ##############################################################################################################

        ##############################################################################################################
        # start user play loop using current lists if click on play
        if mouseon(mousepos,[userplayx,userplayy],[userplaywid,userplayhi]) and mousebuttons[0] ==1:

            #########################################################################################################
            #convert lists to absolute locations
            manpos[0] = manpos[0]*normblocksize
            manpos[1] = manpos[1] * normblocksize
            flagpos[0] = flagpos[0] * normblocksize + normblocksize*flagoffset
            flagpos[1] = flagpos[1] * normblocksize
            for enemy in enemies:
                enemy[0]= enemy[0]*normblocksize + enemyoffset*normblocksize
                enemy[1] = enemy[1] * normblocksize + enemyoffset*normblocksize
            for coin in coins:
                coin[0]= coin[0]*normblocksize
                coin[1] = coin[1] * normblocksize
            ##############################################################################################################
            # run user game loop
            # if quit out of loop, return to main menu, or else return back to user maker
            if quickgameloop(blocks,enemies,manpos,flagpos,coins) == -1:
                return -1,[manpostempsaved,flagpostempsaved,blockstempsaved,enemiestempsaved,coinstempsaved],[manpostempdef,flagpostempdef,blockstempdef,enemiestempdef,coinstempdef]
            else:
                return 1,[manpostempsaved,flagpostempsaved,blockstempsaved,enemiestempsaved,coinstempsaved],[manpostempdef,flagpostempdef,blockstempdef,enemiestempdef,coinstempdef]
        ##############################################################################################################

        ##############################################################################################################
        # start an AI learning loop with graphics
        if mouseon(mousepos, [ailearnx, ailearny], [ailearnwid, ailearnhi]) and mousebuttons[0] == 1:
            #########################################################################################################
            # convert lists to absolute grid positions
            manpos[0] = manpos[0] * normblocksize
            manpos[1] = manpos[1] * normblocksize
            flagpos[0] = flagpos[0] * normblocksize+ normblocksize*flagoffset
            flagpos[1] = flagpos[1] * normblocksize
            for enemy in enemies:
                enemy[0] = enemy[0] * normblocksize + enemyoffset * normblocksize
                enemy[1] = enemy[1] * normblocksize + enemyoffset * normblocksize
            for coin in coins:
                coin[0]= coin[0]*normblocksize
                coin[1] = coin[1] * normblocksize
            ##############################################################################################################

            # run AI loop with graphics
            # if quit out of it return to main menu, or else return to user maker
            if quickAIloop(blocks, enemies, manpos,1,flagpos,coins,wintype) ==-1:
                return -1,[manpostempsaved,flagpostempsaved,blockstempsaved,enemiestempsaved,coinstempsaved],[manpostempdef,flagpostempdef,blockstempdef,enemiestempdef,coinstempdef]
            else:
                return 1,[manpostempsaved,flagpostempsaved,blockstempsaved,enemiestempsaved,coinstempsaved],[manpostempdef,flagpostempdef,blockstempdef,enemiestempdef,coinstempdef]
        ##############################################################################################################

        ##############################################################################################################
        # run AI loop without graphics if clicked on
        if mouseon(mousepos, [aifinishx, aifinishy], [aifinishwid, aifinishhi]) and mousebuttons[0] == 1:
            ########################################################################################################
            # convert lists to absolute grid positions
            manpos[0] = manpos[0] * normblocksize
            manpos[1] = manpos[1] * normblocksize
            flagpos[0] = flagpos[0] * normblocksize+ normblocksize*flagoffset
            flagpos[1] = flagpos[1] * normblocksize
            for enemy in enemies:
                enemy[0] = enemy[0] * normblocksize + enemyoffset * normblocksize
                enemy[1] = enemy[1] * normblocksize + enemyoffset * normblocksize
            for coin in coins:
                coin[0]= coin[0]*normblocksize
                coin[1] = coin[1] * normblocksize
            ##############################################################################################################

            # if quit out of loop, return to main menu, else go back to user maker
            if quickAIloop(blocks, enemies, manpos,0,flagpos,coins,wintype) ==-1:
                return -1,[manpostempsaved,flagpostempsaved,blockstempsaved,enemiestempsaved,coinstempsaved],[manpostempdef,flagpostempdef,blockstempdef,enemiestempdef,coinstempdef]
            else:
                return 1,[manpostempsaved,flagpostempsaved,blockstempsaved,enemiestempsaved,coinstempsaved],[manpostempdef,flagpostempdef,blockstempdef,enemiestempdef,coinstempdef]
        ##############################################################################################################

        gameDisplay.fill(white)

        ##############################################################################################################
        # draw a rectange aroud the current object type and win condition
        if objtype == 1:
            pygame.draw.rect(gameDisplay, red, [blockdispx - rectbuffer,blockdispy - rectbuffer,normblocksize+2*rectbuffer,normblocksize+2*rectbuffer],rectwid)
        if objtype == 2:
            pygame.draw.rect(gameDisplay, red, [enemydispx - rectbuffer,enemydispy - rectbuffer,enemywid+2*rectbuffer,enemyhi+2*rectbuffer],rectwid)
        if objtype == 3:
            pygame.draw.rect(gameDisplay, red, [guydispx - rectbuffer,guydispy - rectbuffer,manwid+2*rectbuffer,manhi+2*rectbuffer],rectwid)
        if objtype == 4:
            pygame.draw.rect(gameDisplay, red, [flagdispx - rectbuffer,flagdispy - rectbuffer,smallflagsize[0]+2*rectbuffer,smallflagsize[1]+2*rectbuffer],rectwid)
        if objtype == 5:
            pygame.draw.rect(gameDisplay, red, [coindispx - rectbuffer,coindispy - rectbuffer,smallcoinsize[0]+2*rectbuffer,smallcoinsize[1]+2*rectbuffer],rectwid)

        if wintype == 1:
            pygame.draw.rect(gameDisplay, black, [shortpathpos[0] - rectbuffer,shortpathpos[1] - rectbuffer,shortpathsize[0]+2*rectbuffer,shortpathsize[1]+2*rectbuffer],rectwid)
        if wintype == 2:
            pygame.draw.rect(gameDisplay, black, [shortdistpos[0] - rectbuffer,shortdistpos[1] - rectbuffer,shortdistsize[0]+2*rectbuffer,shortdistsize[1]+2*rectbuffer],rectwid)
        ##############################################################################################################

        ##############################################################################################################
        # pygame display images
        drawgrid(topleft, botright, smallblocksize, 1)
        drawsmallman(manpos[0]*smallblocksize+topleft[0]+ smallmanwid/2,manpos[1]*smallblocksize+topleft[1])
        drawsmallenemies(enemies,topleft[0],topleft[1])
        drawsmallcoins(coins,topleft[0],topleft[1])
        drawsmallblockstrips(blocks, topleft[0], topleft[1])
        drawsmallflag([flagpos[0]*smallblocksize+topleft[0] + smallflagsize[0]/2,flagpos[1]*smallblocksize+topleft[1]])
        gameDisplay.blit(userplay, (userplayx, userplayy))
        gameDisplay.blit(ailearn, (ailearnx, ailearny))
        gameDisplay.blit(aifinish, (aifinishx, aifinishy))
        gameDisplay.blit(select,(selectx,selecty))
        gameDisplay.blit(resetlevel, resetpos)
        gameDisplay.blit(savelevel, savelevelpos)
        gameDisplay.blit(setdefault, setdefaultpos)
        gameDisplay.blit(shortestdist, shortdistpos)
        gameDisplay.blit(shortpath, shortpathpos)
        gameDisplay.blit(wincondition, winconditionpos)
        drawman(guydispx,guydispy)
        drawenemy(enemydispx, enemydispy)
        drawblock(blockdispx, blockdispy)
        drawsmallflag([flagdispx,flagdispy])
        drawsmallcoin(coindispx,coindispy)
        ##############################################################################################################

        pygame.display.update()

##############################################################################################################
# loop for AI playing through a game generation
def quickAIgame(playerlists,currsteps,repeat,totalsteps,blocklist,enemylistinput,manpos,graphics,previousdatainput,generation,genswait,flagpos,coinlist,wintype):
    # copy the previous data as not to overwrite it
    previousdata = copy.deepcopy(previousdatainput)
    # copy the enemy list as not to overrite it
    enemylist = []
    i = 0
    for enemy in enemylistinput:
        enemylist.append([])
        for things in enemy:
            blah = things
            enemylist[i].append(blah)
        i = i + 1

    ############################################################################################################
    # defining variables
    enbouncesp = 2  # vertical speed to bounce off enemies
    clockspeed = 1000  # speed of game frame rate
    horspeed = 1.2      # player horizontal speed
    enspeed = 0.8       # enemy horizontal speed
    #roomwidth = 3000
    roomheight = dh     # height of the room (display height)
    screenbuffer = 300  # how close to get to boundary before movng camera
    jumpspeed = 3.8     # upward speed of jump
    gravacc = 0.03      # accelleration due to gravity
    ##############################################################################################################

    ##############################################################################################################
    # previous state initializations for no graphics to speed things up
    # if graphics is on or first round of generations
    # or no previous data, then start from beginning
    # initialize values to starting values
    if graphics == 1 or generation <= genswait or previousdata == 0:
        dead = []
        manxabs= []
        manyabs = []
        manxrel = []
        manyrel = []
        manyspeed = []
        deadenemies = []
        blkchncollef = [] #starts at 0
        blkchncolrig = []
        blkchncolup = []
        blkchncoldow = []
        topcoll = []    # INITIALIZE TO 1
        botcoll = []
        leftcoll = []
        rightcoll = []
        deathcoll = []
        goodcoll = []
        collindex = []

        # initialize for each player in the generation
        for _ in playerlists:
            dead.append(0)
            manxabs.append(manpos[0])
            manyabs.append(manpos[1])
            manxrel.append(manpos[0])
            manyrel.append(manpos[1])
            manyspeed.append(0)
            blkchncollef.append(0)  # starts at 0
            blkchncolrig.append(0)
            blkchncolup.append(0)
            blkchncoldow.append(0)
            topcoll.append(1)  # INITIALIZE TO 1
            botcoll.append(1)
            leftcoll.append(1)
            rightcoll.append(1)
            deathcoll.append(0)
            goodcoll.append(0)
            collindex.append(0)

        # starts each enemy moving left
        enemyspeeds = []
        for _ in enemylist:
            enemyspeeds.append([-enspeed,0])

        # initialize dead enemies to 0 to react to enemies
        for i in range(0,len(playerlists)):
            deadenemies.append([])
            for _ in enemylist:
                deadenemies[i].append(0)

        # enemy collision stats, 1 means not hit a wall
        encollef = []
        encolrig = []
        encoltop = []
        encolbot = []

        for _ in enemylist:
            encollef.append(1)
            encolrig.append(1)
            encoltop.append(1)
            encolbot.append(1)

        # initialize camera position
        if manxabs[0] <= dw / 2 - 20:
            camerax = dw / 2 - 20
        elif manxabs[0] >= roomwidth - dw / 2 + 10:
            camerax = roomwidth - dw / 2 + 10
        else:
            camerax = manxabs[0]
        cameray = dh/2

        # intilize frame count
        frame = 0
    # if running no graphics, need to initialize to previous data
    else:
        dead = previousdata[0]
        manxabs = previousdata[1]
        manyabs = previousdata[2]
        manxrel = previousdata[3]
        manyrel = previousdata[4]
        manyspeed = previousdata[5]
        deadenemies = previousdata[6]
        blkchncollef = previousdata[7]  # starts at 0
        blkchncolrig = previousdata[8]
        blkchncolup = previousdata[9]
        blkchncoldow = previousdata[10]
        topcoll = previousdata[11]  # INITIALIZE TO 1
        botcoll = previousdata[12]
        leftcoll = previousdata[13]
        rightcoll = previousdata[14]
        deathcoll = previousdata[15]
        goodcoll = previousdata[16]
        collindex = previousdata[17]
        enemyspeeds = previousdata[18]
        encollef = previousdata[19]
        encolrig = previousdata[20]
        encoltop = previousdata[21]
        encolbot = previousdata[22]
        camerax = previousdata[23]
        cameray = previousdata[24]
        frame = previousdata[25]
        enemylist = previousdata[26]
    ##############################################################################################################

    ##############################################################################################################
    # actual running the game loop until run frames to end of generation
    while frame < currsteps:
        #
        # check user input for quit commands and slow motion
        #
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_q:
                    return (-1,[])
                if event.key == pygame.K_r:
                    return (1,[])
                if event.key == pygame.K_SPACE:
                    clockspeed = 1
            if event.type == pygame.KEYUP:
                if event.key == pygame.K_SPACE:
                    clockspeed = 10
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()

        ##############################################################################################################
        # enemy and player motion calcuations
        # only move when not collided with walls and not dead
        # acheived using bollean operations with the flags
        # also capped by max vertical speed to prevent falling through floor
        for i in range(0,len(enemylist)):
            enemyspeeds[i][1]=(enemyspeeds[i][1]+gravacc*encoltop[i])*(enemyspeeds[i][1]<maxenemyspeed)+maxenemyspeed*(
                    enemyspeeds[i][1]>=maxenemyspeed)
            enemylist[i][1]=enemylist[i][1]+enemyspeeds[i][1]

            enemylist[i][0] = enemylist[i][0]+enemyspeeds[i][0]
        for i in range(0,len(playerlists)):
            if dead[i]==0:
                manxabs[i] = manxabs[i]+(-horspeed*(playerlists[i][int(frame/repeat)] == 0 or playerlists[i][int(
                    frame/repeat)] == 3))*rightcoll[i]+(horspeed*(playerlists[i][int(frame/repeat)] == 1 or playerlists[i][
                    int(frame/repeat)] == 4))*leftcoll[i]
                manxrel[i] = manxabs[i]+dw/2-camerax

                manyspeed[i] = (manyspeed[i] + gravacc*topcoll[i])*(manyspeed[i] < maxspeed)+maxspeed*(manyspeed[i]>=maxspeed)
                manyabs[i] = manyabs[i] + manyspeed[i]
                manyrel[i] = manyabs[i] + dh/2 - cameray
        ##############################################################################################################

        ##############################################################################################################
        # display if graphics is set on
        if graphics == 1:
            # decide which player is closest to flag to follow with camera
            distances = []
            for i in range(0,len(manyabs)):
                distances.append(distancebetween([manxabs[i],manyabs[i]],flagpos))
            followindex = distances.index(min(distances))
            if manxabs[followindex] <= dw / 2-20:
                camerax = dw / 2 - 20
            elif manxabs[followindex] >= roomwidth - dw / 2+10:
                camerax = roomwidth - dw / 2 + 10
            else:
                camerax = manxabs[followindex]

            gameDisplay.fill(white)
            drawblockstrips(blocklist,camerax,cameray)
            drawcoins(coinlist, camerax, cameray)
            drawenemies(enemylist,camerax,cameray)
            drawflag(flagpos,camerax,cameray)
            # draw all of the player still alive
            for i in range(0,len(playerlists)):
                if dead[i] == 0:
                   drawman(manxrel[i], manyrel[i])
        # if no graphics display the current generation
        else:
            gameDisplay.fill(white)
            text = font.render("AI LEARNING PLEASE WAIT", True, black)
            gameDisplay.blit(text,(290,100))
            text = font.render("CURRENTLY RUNNING" ,True, black)
            gameDisplay.blit(text,(360,230))
            text = font2.render("GENERATION  " + str(generation), True, (126,30,200))
            gameDisplay.blit(text, (250, 400))
        ##############################################################################################################

    ##############################################################################################################
    # checking game collisions
        ##############################################################################################################
        # collisions of players with blocks and enemies with blocks
        for i in range(0,len(playerlists)):
            # initialize flag variables
            blkchncollef[i] = 0
            blkchncolrig[i] = 0
            blkchncolup[i] = 0
            blkchncoldow[i] = 0
            deathcoll[i] = 0
            goodcoll[i] = 0
            collindex[i] = -1

        # initialize flag variables
        encollef = []
        encolrig = []
        encoltop = []
        encolbot = []

        for _ in enemylist:
            encollef.append(1)
            encolrig.append(1)
            encoltop.append(1)
            encolbot.append(1)

        for blocks in blocklist:
            # calculate the boundary of each block chain
            lbound = normblocksize * (blocks[0] * (blocks[2] != -1) + (blocks[0] - blocks[4] + 1) * (blocks[2] == -1))
            rbound = normblocksize * ((blocks[0] + blocks[4]) * (blocks[2] == 1) + (blocks[0] + 1) * (blocks[2] != 1))
            ubound = normblocksize * (blocks[1] * (blocks[3] != -1) + (blocks[1] - blocks[4] + 1) * (blocks[3] == -1))
            dbound = normblocksize * ((blocks[1] + blocks[4]) * (blocks[3] == 1) + (blocks[1] + 1) * (blocks[3] != 1))

            ##############################################################################################################
            # check for collisions of player with block
            for i in range(0,len(playerlists)):
                # left collision
                if (manxabs[i] >= lbound - manwid - collisionbuff and manxabs[i] <= lbound - manwid + collisionbuff) and (
                        (manyabs[i] >= ubound and manyabs[i] <= dbound) or (manyabs[i] + manhi >= ubound and manyabs[
                    i] + manhi <= dbound) or (manyabs[i] + manhi <= dbound and manyabs[i] >= ubound)):
                    blkchncollef[i] = 1
                # right collisions
                if (manxabs[i] >= rbound - collisionbuff and manxabs[i] <= rbound + collisionbuff) and (
                        (manyabs[i] >= ubound and manyabs[i] <= dbound) or (manyabs[i] + manhi >= ubound and manyabs[
                    i] + manhi <= dbound) or (manyabs[i] + manhi <= dbound and manyabs[i] >= ubound)):
                    blkchncolrig[i] = 1
                # collisions with bottom of block
                if (manyabs[i]>= dbound - collisionbuff and manyabs[i]<= dbound + collisionbuff) and (
                        (manxabs[i]>= lbound and manxabs[i]<= rbound) or (manxabs[i]+ manwid >= lbound and manxabs[
                    i]+ manwid <= rbound) or (manxabs[i]+ manwid <= rbound and manxabs[i]>= lbound)):
                    blkchncoldow[i] = 1
                    # need to stop moving vertically
                    manyspeed[i] = 0
                # collision with top of block (ie ground)
                if (manyabs[i]+ manhi >= ubound - collisionbuff and manyabs[i]+ manhi <= ubound + collisionbuff) and (
                        (manxabs[i]>= lbound and manxabs[i]<= rbound) or (manxabs[i]+ manwid >= lbound and manxabs[
                    i]+ manwid <= rbound) or (manxabs[i]+ manwid <= rbound and manxabs[i]>= lbound)):
                    blkchncolup[i] = 1
                    # if trying to jump then jump or else stop
                    if playerlists[i][int(frame/repeat)] >= 2:
                        manyspeed[i] = -jumpspeed
                    else:
                        manyspeed[i] = 0
            ##############################################################################################################

            ##############################################################################################################
            # check enemy collisions with blocks
            for i in range(0,len(enemylist)):
                # left collision
                if (enemylist[i][0] >= lbound - enemywid - collisionbuff and enemylist[i][0] <= lbound - enemywid + collisionbuff) and (
                        (enemylist[i][1] >= ubound and enemylist[i][1] <= dbound) or (
                        enemylist[i][1] + enemyhi >= ubound and enemylist[i][1] + enemyhi <= dbound) or (
                                enemylist[i][1] + enemyhi <= dbound and enemylist[i][1] >= ubound)):
                    encollef[i] = 0
                    # bounce off wall
                    enemyspeeds[i][0]=-enemyspeeds[i][0]
                # right collision
                if (enemylist[i][0] >= rbound - collisionbuff and enemylist[i][0] <= rbound + collisionbuff) and (
                        (enemylist[i][1] >= ubound and enemylist[i][1] <= dbound) or (
                        enemylist[i][1] + enemyhi >= ubound and enemylist[i][1] + enemyhi <= dbound) or (
                        enemylist[i][1] + enemyhi <= dbound and enemylist[i][1] >= ubound)):
                    encolrig[i] = 0
                    # bounce off wall
                    enemyspeeds[i][0] = -enemyspeeds[i][0]
                # collision with bottom
                if (enemylist[i][1] >= dbound - collisionbuff and enemylist[i][1] <= dbound + collisionbuff) and (
                        (enemylist[i][0] >= lbound and enemylist[i][0] <= rbound) or (
                        enemylist[i][0] + enemywid >= lbound and enemylist[i][0] + enemywid <= rbound) or (
                        enemylist[i][0] + enemywid <= rbound and enemylist[i][0] >= lbound)):
                    encolbot[i] = 0
                    # stop moving up
                    enemyspeeds[i][1] = 0
                # collision with top
                if (enemylist[i][1] + enemyhi >= ubound - collisionbuff and enemylist[i][1] + enemyhi <= ubound + collisionbuff) and (
                        (enemylist[i][0] >= lbound and enemylist[i][0] <= rbound) or (
                        enemylist[i][0] + enemywid >= lbound and enemylist[i][0] + enemywid <= rbound) or (
                        enemylist[i][0] + enemywid <= rbound and enemylist[i][0] >= lbound)):
                    encoltop[i] = 0
                    # stop moving down
                    enemyspeeds[i][1] = 0
                ##############################################################################################################
        ##############################################################################################################

        ##############################################################################################################
        # player to enemy collisoion checks
        for i in range(0,len(enemylist)):
            for j in range(0,len(playerlists)) :
                # left collision
                if (enemylist[i][0] >= manxabs[j]- enemywid - collisionbuff and enemylist[i][
                    0] <= manxabs[j]- enemywid + collisionbuff) and (
                        (enemylist[i][1] >= manyabs[j]and enemylist[i][1] <= manyabs[j]+manhi) or (
                        enemylist[i][1] + enemyhi >= manyabs[j]and enemylist[i][1] + enemyhi <= manyabs[j]+manhi) or (
                                enemylist[i][1] + enemyhi <= manyabs[j]+manhi and enemylist[i][1] >= manyabs[j])):
                    # death of player
                    deathcoll[j] = 1
                    collindex[j] = i
                #right collision
                if (enemylist[i][0] >= manxabs[j]+manwid - collisionbuff and enemylist[i][0] <= manxabs[j]+manwid + collisionbuff) and (
                        (enemylist[i][1] >= manyabs[j]and enemylist[i][1] <= manyabs[j]+manhi) or (
                        enemylist[i][1] + enemyhi >= manyabs[j]and enemylist[i][1] + enemyhi <= manyabs[j]+manhi) or (
                                enemylist[i][1] + enemyhi <= manyabs[j]+manhi and enemylist[i][1] >= manyabs[j])):
                    # death of player
                    deathcoll[j] = 1
                    collindex[j] = i
                # top collision
                if (enemylist[i][1] >= manyabs[j]+manhi - collisionbuff-10 and enemylist[i][1] <= manyabs[j]+ manhi + collisionbuff+10) and (
                        (enemylist[i][0] >= manxabs[j]and enemylist[i][0] <= manxabs[j]+manwid) or (
                        enemylist[i][0] + enemywid >= manxabs[j]and enemylist[i][0] + enemywid <= manxabs[j]+manwid) or (
                                enemylist[i][0] + enemywid <= manxabs[j]+manwid and enemylist[i][0] >= manxabs[j]) or (
                        manxabs[j]>= enemylist[i][0] and manxabs[j]+ manwid <= enemylist[i][0]+enemywid)):
                    # death of enemy
                    goodcoll[j] = 1
                    collindex[j] = i
                # bottom collision
                if (enemylist[i][1] + enemyhi >= manyabs[j]- collisionbuff and enemylist[i][
                    1] + enemyhi <= manyabs[j]+ collisionbuff) and (
                        (enemylist[i][0] >= manxabs[j]and enemylist[i][0] <= manxabs[j]+manwid) or (
                        enemylist[i][0] + enemywid >= manxabs[j]and enemylist[i][0] + enemywid <= manxabs[j]+manwid) or (
                                enemylist[i][0] + enemywid <= manxabs[j]+manwid and enemylist[i][0] >= manxabs[j]) or (
                        manxabs[j]>= enemylist[i][0] and manxabs[j]+ manwid <= enemylist[i][0]+enemywid)):
                    # death of player
                    deathcoll[j] = 1
                    collindex[j] = i
        ##############################################################################################################

        # flag collision check
        for i in range(0,len(playerlists)):
            if (((manxabs[i] + manwid >= flagpos[0] + flagoffset[0] and manxabs[i] + manwid <= flagpos[0] + flagsize[0] -flagoffset[0]) or (
                             manxabs[i] >= flagpos[0] + flagoffset[0] and manxabs[i] <= flagpos[0] + flagsize[0] - flagoffset[
                         0])) and ((manyabs[i] <= flagpos[1] + flagsize[1] - flagoffset[1] and manyabs[i] >= flagpos[1] +
                                    flagoffset[1]) or (manyabs[i] + manhi <= flagpos[1] + flagsize[1] - flagoffset[
                    1] and manyabs[i] + manhi >= flagpos[1] + flagoffset[1]))):
                print("THIS SHOULD REACH FLAG")
                # return winning player index
                return 2,i

        ##############################################################################################################
        # general collision checks
        for i in range(0,len(playerlists)):
            # convert block collions into general collisions for each player
            if blkchncolup[i] == 1:
                topcoll[i] = 0
            else:
                topcoll[i] = 1
            if blkchncollef[i] == 1:
                leftcoll[i] = 0
            else:
                leftcoll[i] = 1
            if blkchncolrig[i] == 1:
                rightcoll[i] = 0
            else:
                rightcoll[i] = 1
            if blkchncoldow[i] == 1:
                botcoll[i] = 0
            else:
                botcoll[i] = 1
            # kill player if collided badly with enemy
            if collindex[i] != -1:
                if deathcoll[i] == 1 and deadenemies[i][collindex[i]]== 0:
                    dead[i] = 1
                if goodcoll[i] == 1 and deadenemies[i][collindex[i]]== 0:
                    manyspeed[i] = -enbouncesp
                    if playerlists[i][int(frame/repeat)] >= 2:
                        manyspeed[i] = -jumpspeed
                    deadenemies[i][collindex[i]] = 1
        ##############################################################################################################

        # update display and increment frame
        pygame.display.update()
        clock.tick(clockspeed)
        frame = frame+1

    ##############################################################################################################
    # prepare output data
    outdata = []
    blockgrid = convertblockslisttogrid(blocklist)

    # calculate win condition for each player
    for i in range(0,len(playerlists)):
        #outdata.append(math.sqrt(manxabs[i]**2+(roomheight-manyabs[i])**2))      # win condition function
        #outdata.append(distancebetween([manxabs[i],manyabs[i]],flagpos))
        if dead[i] == 1:
            outdata.append(pathmax)
        else:
            if wintype == 1:
                outdata.append(findshortestpath([manxabs[i],manyabs[i]],flagpos,blockgrid))
            if wintype == 2:
                outdata.append(distancebetween([manxabs[i], manyabs[i]], flagpos))

    # if at end of a generation cycle, save new state to be reloaded
    if generation%genswait == 0:
        restoredata = []
        restoredata.append(dead)
        restoredata.append(manxabs)
        restoredata.append(manyabs)
        restoredata.append(manxrel)
        restoredata.append(manyrel)
        restoredata.append(manyspeed)
        restoredata.append(deadenemies)
        restoredata.append(blkchncollef)
        restoredata.append(blkchncolrig)
        restoredata.append(blkchncolup)
        restoredata.append(blkchncoldow)
        restoredata.append(topcoll)
        restoredata.append(botcoll)
        restoredata.append(leftcoll)
        restoredata.append(rightcoll)
        restoredata.append(deathcoll)
        restoredata.append(goodcoll)
        restoredata.append(collindex)
        restoredata.append(enemyspeeds)
        restoredata.append(encollef)
        restoredata.append(encolrig)
        restoredata.append(encoltop)
        restoredata.append(encolbot)
        restoredata.append(camerax)
        restoredata.append(cameray)
        restoredata.append(frame)
        restoredata.append(enemylist)
        return (outdata,restoredata)
    # if not at end of generation cycle, return previous data
    else:
        return (outdata,previousdatainput)

##############################################################################################################
# Genetic algorithm AI execution
def quickAIloop(blocklist,enemylist,manpos,graphics,flagpos,coinlist,wintype):
    ##############################################################################################################
    # initialize evolution parameters
    numplayers = 200   # number of players per batch
    genswait = 2       # generations before adding more steps to the batch
    finalgen = 20      # generations before quitting if not reached flag
    playersteps = []   # array for storing the players' choices
    keepers = 10       # number of top players choices that are brought to next gen
    mutation = 0.33    # chance of mutating each move when mutating
    repeat = 48        # number of frames each choice is executed for (makes more smooth motions)
    stepsadded = 7     # THIS FACTOR IS NUMBER OF CHOICES added per generations waited
    totalsteps = stepsadded     # keeping track of current number of choices for the generation
    ##############################################################################################################

    ##############################################################################################################
    # initializing random choices to start
    # generate random directions, 0 = LEFT, 1 = RIGHT, 2 = UP, 3 = Up LEFT, 4 = up RIGHT
    for i in range(0, numplayers):
        playersteps.append([])
        for _ in range(0, stepsadded):
            playersteps[i].append(
                random.randint(0, 4))  # implement -1 to introduce stopping, put at mutation as well, end of program
            # while playersteps[i] == 2:
            #   playersteps[i] = random.randint(0,4)           #ELIMINATES OPTION 2 (jump straight)
    ##############################################################################################################

    winnersteps = []
    restoredata = []

    ##############################################################################################################
    # check for quit commands
    for generation in range(1, finalgen + 1):
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_q:
                    return -1
                if event.key == pygame.K_r:
                    return 1
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
        savedata = []
    ##############################################################################################################

        # run an AI game loop with current generation stats
        testdata,restoredata = quickAIgame(playersteps, totalsteps * repeat,repeat,totalsteps,blocklist,enemylist,manpos,graphics,restoredata,generation,genswait,flagpos,coinlist,wintype)
        print("finished generation", generation)

        ##############################################################################################################
        # check for quit commands from AI loop
        if testdata == -1:
            return -1
        if testdata == 1:
            return 1
        if testdata == 2: # if found flag
            # find the index of the winning player and store steps
            # winnersteps = playersteps[testdata.index(max(testdata))]  # alternate when not using find algorithm
            winnersteps = playersteps[restoredata]
            print("THIS REALLY SHOULD REACH FLAG")
            break
        # if flag identified as impossible break out of loop
        if min(testdata) == pathmax:
            print("Could Not Solve")
            return 1
        ##############################################################################################################

        # if at end of generations, return the best possible player
        if generation == finalgen:
            # winnersteps = playersteps[testdata.index(max(testdata))]
            winnersteps = playersteps[testdata.index(min(testdata))]
            break

        saverestore = []
        for i in range(0, len(restoredata)):
            saverestore.append([])

        ##############################################################################################################
        # EVOLVING ALGORITHM
        # Speciallist: values that must be handled specially because they are not dependent on the player
        if generation >= genswait:
            for i in speciallist:
                saverestore[i].append(restoredata[i])
            #########################################################################################################
            #ISOLATE BEST PLAYERS OF THE GENERATION
        for _ in range(0, keepers):
            #goodindex = testdata.index(max(testdata))
            goodindex = testdata.index(min(testdata))
            savedata.append(playersteps[goodindex])
            # make a copy of the best player if past the first round of steps
            # with special handling of special list
            if generation >= genswait:
                for i in range(0, len(restoredata)):
                    flag = 0
                    for item in speciallist:
                        if item == i:
                            flag = 1
                    if flag == 0:
                        saverestore[i].append(restoredata[i][goodindex])
                        del restoredata[i][goodindex]
            # delete that player data to find the next best
            del testdata[goodindex]
            del playersteps[goodindex]
            #########################################################################################################

        # add more steps if at end of round
        if generation % genswait == 0 and generation != finalgen:
            totalsteps = totalsteps + stepsadded

        ##############################################################################################################
        # mutations to create next player steps using saverestore and savedata
        # if past first round of generation steps
        playersteps = []
        if generation >= genswait:
            for i in range(0,len(restoredata)):
                restoredata[i] = []
            # copy all special list values becasue independent of player
            for i in speciallist:
                restoredata[i].append(saverestore[i][0])
                restoredata[i] = restoredata[i][0]
        for k in range(0, round(numplayers / len(savedata))):
            for j in range(0, len(savedata)):
                playersteps.append([])
                #######################################################################################################
                # making restore data for the new players
                if generation >= genswait:
                    for i in range(0,len(restoredata)):
                        flag = 0
                        for item in speciallist:
                            if item == i:
                                flag = 1
                        if flag == 0:
                            # special handling of deadenemies - need to make deepcopy so they are not
                            # linked for each player's copy
                            if i == 6:
                                restoredata[i].append(copy.deepcopy(saverestore[i][j]))
                            else:
                                restoredata[i].append(saverestore[i][j])
                ##############################################################################################################

                ##############################################################################################################
                # making player steps (with mutations) of new generation
                for i in range(0, totalsteps):
                    # preserve the steps that have already been trained
                    if i < totalsteps - stepsadded:
                        playersteps[k * len(savedata) + j].append(savedata[j][i])
                    # change the "new" steps with probability of the mutation rate
                    elif generation % genswait == 0 or random.randint(0, 100) <= mutation * 100:
                        playersteps[k * len(savedata) + j].append(random.randint(0, 4))             #change to -1 to introduce stopping
                    else:
                        playersteps[k * len(savedata) + j].append(savedata[j][i])
                ##############################################################################################################

        pygame.display.update()
    # play the obtained solution to show the user the AI reaching the flag
    quickAIgame([winnersteps], totalsteps * repeat, repeat, totalsteps, blocklist, enemylist, manpos,1,0,finalgen,genswait,flagpos,coinlist,wintype)
    return 1

##############################################################################################################
# user play loop (very similar to AI game so see above for details)
def quickgameloop(blocklist,enemylistinput,manpos,flagpos,coinlistinput):
    coinlist = copy.deepcopy(coinlistinput)
    enemylist = []
    i = 0
    for enemy in enemylistinput:
        enemylist.append([])
        for things in enemy:
            blah = things
            enemylist[i].append(blah)
        i = i+1
    enbouncesp = 2
    dead = 0
    win = 0
    clockspeed = 300
    horspeed = 1.2
    enspeed = 0.8
    #roomwidth = 3000
    screenbuffer = 300
    manxabs = manpos[0]
    manyabs = manpos[1]
    manxrel = 0
    manyrel = manyabs
    manyspeed = 0
    jumpspeed = 3.8
    gravacc = 0.03
    score = 0


    enemyspeeds = []
    for enemies in enemylist:
        enemyspeeds.append([-enspeed,0])
    encollef = []
    encolrig = []
    encoltop = []
    encolbot = []

    for _ in enemylist:
        encollef.append(1)
        encolrig.append(1)
        encoltop.append(1)
        encolbot.append(1)

    ldir = 0
    rdir = 0
    udir = 0
    ddir = 0

    blkchncollef = 0
    blkchncolrig = 0
    blkchncolup = 0
    blkchncoldow = 0



    topcoll = 1
    botcoll = 1
    leftcoll = 1
    rightcoll = 1
    if manxabs<=dw/2:
        camerax = dw/2 - 50
    elif manxabs>= roomwidth-dw/2:
        camerax = roomwidth-dw/2+10
    else:
        camerax = manxabs
    cameray = dh/2

    while dead == 0 and win == 0:
        #
        #check user input
        #
        for event in pygame.event.get():

            if event.type == pygame.QUIT:
                pygame.quit()
                quit()

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_q:
                    return -1
                if event.key == pygame.K_r:
                    return 1
                if event.key == pygame.K_LEFT:
                    ldir = -horspeed
                elif event.key == pygame.K_RIGHT:
                    rdir = horspeed
                if event.key == pygame.K_DOWN:
                    ddir = 1
                elif event.key == pygame.K_UP:
                    udir = 1
            if event.type == pygame.KEYUP:
                if event.key == pygame.K_RIGHT:
                    rdir = 0
                elif event.key == pygame.K_DOWN:
                    ddir = 0
                elif event.key == pygame.K_UP:
                    udir = 0
                elif event.key == pygame.K_LEFT:
                    ldir = 0
        #
        #motion stuff here
        #
        manxabs = manxabs+ldir*rightcoll+rdir*leftcoll
        manxrel = manxabs+dw/2-camerax

        manyspeed = (manyspeed + gravacc*topcoll)*(manyspeed < maxspeed)+maxspeed*(manyspeed>=maxspeed)
        manyabs = manyabs + manyspeed
        manyrel = manyabs + dh/2 - cameray

        for i in range(0,len(enemylist)):
            enemyspeeds[i][1]=(enemyspeeds[i][1]+gravacc*encoltop[i])*(enemyspeeds[i][1]<maxenemyspeed)+maxenemyspeed*(
                    enemyspeeds[i][1]>=maxenemyspeed)
            enemylist[i][1]=enemylist[i][1]+enemyspeeds[i][1]

            enemylist[i][0] = enemylist[i][0]+enemyspeeds[i][0]

        if manxrel+manwid/2<screenbuffer and (ldir*leftcoll+rdir*rightcoll)<0 and camerax>dw/2:
            camerax = camerax - horspeed
        elif manxrel+manwid/2>dw-screenbuffer and (ldir*leftcoll+rdir*rightcoll)>0 and camerax<roomwidth-dw/2:
            camerax = camerax + horspeed


        #
        #display stuff here
        #
        gameDisplay.fill(white)
        drawblockstrips(blocklist,camerax,cameray)
        drawcoinscore(coinscorepos)
        displaycoinscore(score,coinscorepos)
        drawcoins(coinlist, camerax, cameray)
        drawenemies(enemylist,camerax,cameray)
        drawman(manxrel, manyrel)
        drawflag(flagpos,camerax,cameray)

        #
        #game checks here
        #

        #block string collision checks
        blkchncollef = 0
        blkchncolrig = 0
        blkchncolup = 0
        blkchncoldow = 0

        encollef = []
        encolrig = []
        encoltop = []
        encolbot = []

        for _ in enemylist:
            encollef.append(1)
            encolrig.append(1)
            encoltop.append(1)
            encolbot.append(1)

        for blocks in blocklist:
            lbound = normblocksize*(blocks[0]*(blocks[2] != -1) + (blocks[0]-blocks[4]+1)*(blocks[2] == -1))
            rbound = normblocksize*((blocks[0]+blocks[4])*(blocks[2] == 1) + (blocks[0]+1)*(blocks[2] != 1))
            ubound = normblocksize * (blocks[1] * (blocks[3] != -1) + (blocks[1] - blocks[4] + 1) * (blocks[3] == -1))
            dbound = normblocksize * ((blocks[1] + blocks[4]) * (blocks[3] == 1) + (blocks[1] + 1) * (blocks[3] != 1))
            if (manxabs >= lbound - manwid - collisionbuff and manxabs <= lbound - manwid + collisionbuff) and (
                    (manyabs >= ubound and manyabs <= dbound) or (manyabs + manhi >= ubound and manyabs + manhi <= dbound) or (
                    manyabs + manhi <= dbound and manyabs >= ubound)):
                blkchncollef = 1
            if (manxabs >= rbound - collisionbuff and manxabs <= rbound + collisionbuff) and (
                    (manyabs >= ubound and manyabs <= dbound) or (manyabs + manhi >= ubound and manyabs + manhi <= dbound) or (
                    manyabs + manhi <= dbound and manyabs >= ubound)):
                blkchncolrig = 1
            if (manyabs >= dbound - collisionbuff and manyabs <= dbound + collisionbuff) and (
                    (manxabs >= lbound and manxabs <= rbound) or (manxabs + manwid >= lbound and manxabs + manwid <= rbound) or (
                    manxabs + manwid <= rbound and manxabs >= lbound)):
                blkchncoldow = 1
                manyspeed = 0
            if (manyabs + manhi >= ubound - collisionbuff and manyabs + manhi <= ubound + collisionbuff) and (
                    (manxabs >= lbound and manxabs <= rbound) or (manxabs + manwid >= lbound and manxabs + manwid <= rbound) or (
                    manxabs + manwid <= rbound and manxabs >= lbound)):
                blkchncolup = 1
                if udir == 1:
                    manyspeed = -jumpspeed
                else:
                    manyspeed = 0
            for i in range(0,len(enemylist)):
                if (enemylist[i][0] >= lbound - enemywid - collisionbuff and enemylist[i][0] <= lbound - enemywid + collisionbuff) and (
                        (enemylist[i][1] >= ubound and enemylist[i][1] <= dbound) or (
                        enemylist[i][1] + enemyhi >= ubound and enemylist[i][1] + enemyhi <= dbound) or (
                                enemylist[i][1] + enemyhi <= dbound and enemylist[i][1] >= ubound)):
                    encollef[i] = 0
                    enemyspeeds[i][0]=-enemyspeeds[i][0]
                if (enemylist[i][0] >= rbound - collisionbuff and enemylist[i][0] <= rbound + collisionbuff) and (
                        (enemylist[i][1] >= ubound and enemylist[i][1] <= dbound) or (
                        enemylist[i][1] + enemyhi >= ubound and enemylist[i][1] + enemyhi <= dbound) or (
                        enemylist[i][1] + enemyhi <= dbound and enemylist[i][1] >= ubound)):
                    encolrig[i] = 0
                    enemyspeeds[i][0] = -enemyspeeds[i][0]
                if (enemylist[i][1] >= dbound - collisionbuff and enemylist[i][1] <= dbound + collisionbuff) and (
                        (enemylist[i][0] >= lbound and enemylist[i][0] <= rbound) or (
                        enemylist[i][0] + enemywid >= lbound and enemylist[i][0] + enemywid <= rbound) or (
                        enemylist[i][0] + enemywid <= rbound and enemylist[i][0] >= lbound)):
                    encolbot[i] = 0
                    enemyspeeds[i][1] = 0
                if (enemylist[i][1] + enemyhi >= ubound - collisionbuff and enemylist[i][1] + enemyhi <= ubound + collisionbuff) and (
                        (enemylist[i][0] >= lbound and enemylist[i][0] <= rbound) or (
                        enemylist[i][0] + enemywid >= lbound and enemylist[i][0] + enemywid <= rbound) or (
                        enemylist[i][0] + enemywid <= rbound and enemylist[i][0] >= lbound)):
                    encoltop[i] = 0
                    enemyspeeds[i][1] = 0

        deathcoll = 0
        goodcoll = 0
        collindex = 0
        for i in range (0,len(enemylist)):
            if (enemylist[i][0] >= manxabs - enemywid - collisionbuff and enemylist[i][
                0] <= manxabs - enemywid + collisionbuff) and (
                    (enemylist[i][1] >= manyabs and enemylist[i][1] <= manyabs+manhi) or (
                    enemylist[i][1] + enemyhi >= manyabs and enemylist[i][1] + enemyhi <= manyabs+manhi) or (
                            enemylist[i][1] + enemyhi <= manyabs+manhi and enemylist[i][1] >= manyabs)):
                deathcoll = 1
                collindex = i
            if (enemylist[i][0] >= manxabs+manwid - collisionbuff and enemylist[i][0] <= manxabs+manwid + collisionbuff) and (
                    (enemylist[i][1] >= manyabs and enemylist[i][1] <= manyabs+manhi) or (
                    enemylist[i][1] + enemyhi >= manyabs and enemylist[i][1] + enemyhi <= manyabs+manhi) or (
                            enemylist[i][1] + enemyhi <= manyabs+manhi and enemylist[i][1] >= manyabs)):
                deathcoll = 1
                collindex = i
            if (enemylist[i][1] >= manyabs+manhi - collisionbuff-10 and enemylist[i][1] <= manyabs + manhi + collisionbuff+10) and (
                    (enemylist[i][0] >= manxabs and enemylist[i][0] <= manxabs+manwid) or (
                    enemylist[i][0] + enemywid >= manxabs and enemylist[i][0] + enemywid <= manxabs+manwid) or (
                            enemylist[i][0] + enemywid <= manxabs+manwid and enemylist[i][0] >= manxabs) or (
                    manxabs >= enemylist[i][0] and manxabs + manwid <= enemylist[i][0]+enemywid)):
                goodcoll = 1
                collindex = i
            if (enemylist[i][1] + enemyhi >= manyabs - collisionbuff and enemylist[i][
                1] + enemyhi <= manyabs + collisionbuff) and (
                    (enemylist[i][0] >= manxabs and enemylist[i][0] <= manxabs+manwid) or (
                    enemylist[i][0] + enemywid >= manxabs and enemylist[i][0] + enemywid <= manxabs+manwid) or (
                            enemylist[i][0] + enemywid <= manxabs+manwid and enemylist[i][0] >= manxabs) or (
                    manxabs >= enemylist[i][0] and manxabs + manwid <= enemylist[i][0]+enemywid)):
                deathcoll = 1
                collindex = i

        i=0
        coinindex = -1
        for coin in coinlist:
            if generalcirclecollision(coin,coinsize[0]/2,[manxabs,manyabs],manwid/2)==1:
                coinindex = i
            i = i+1
        if coinindex >= 0:
            del coinlist[coinindex]
            score = score + 1


        #flag collision check
        if (((manxabs+manwid >= flagpos[0]+flagoffset[0] and manxabs+manwid <= flagpos[0]+flagsize[0]-flagoffset[0]) or
             (manxabs >= flagpos[0]+flagoffset[0] and manxabs <= flagpos[0]+flagsize[0]-flagoffset[0])) and
                ((manyabs <= flagpos[1] + flagsize[1] - flagoffset[1] and manyabs >= flagpos[1]+flagoffset[1]) or
                 (manyabs + manhi <= flagpos[1] + flagsize[1] - flagoffset[1] and manyabs + manhi >= flagpos[1]+flagoffset[1]))):
            win = 1

        #general collision checks
        if blkchncolup == 1:
            topcoll = 0
        else:
            topcoll = 1
        if blkchncollef == 1:
            leftcoll = 0
        else:
            leftcoll = 1
        if blkchncolrig == 1:
            rightcoll = 0
        else:
            rightcoll = 1
        if blkchncoldow == 1:
            botcoll = 0
        else:
            botcoll = 1
        if deathcoll == 1:
            dead = 1
        if goodcoll == 1:
            manyspeed = -enbouncesp
            if udir == 1:
                manyspeed = -jumpspeed
            del enemylist[collindex]
            del enemyspeeds[collindex]
        #
        #end loop stuff
        #
        pygame.display.update()
        clock.tick(clockspeed)
    return 1

while 1==1:
    directive = mainmenu()
    if directive == 1:
        done = 0
        while done >= 0:
            done,saved,defs = leveleditorloop()
            defaultblocklist = defs[2]
            defaultenemylist = defs[3]
            defaultcoinslist = defs[4]
            defaultmanpos = defs[0]
            defaultflagpos = defs[1]
            savedmanpos = saved[0]
            savedflagpos = saved[1]
            savedblocks = saved[2]
            savedenemies = saved[3]
            savedcoins = saved[4]
    if directive == 2:
        quickgameloop(defaultblocklist,defaultenemylist,defaultmanpos,defaultflagpos,defaultcoinslist)
    if directive == 3:
        quickAIloop(defaultblocklist,defaultenemylist,defaultmanpos,1,defaultflagpos,defaultcoinslist,2)

pygame.quit()
quit()

