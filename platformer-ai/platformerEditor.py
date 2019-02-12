import pygame
import time
import random
import math

pygame.init()

dh = 650
dw = 1300
roomwidth = 2500

# color RGB codes
black = (0,0,0)
white = (255,255,255)
red = (255,0,0)
font = pygame.font.Font('freesansbold.ttf', 50)

gameDisplay = pygame.display.set_mode((dw, dh))
pygame.display.set_caption('platformer')
clock = pygame.time.Clock()

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


normblock = pygame.image.load('Normal Block.png')
normblocksize = 50
groundheight = normblocksize

smallblock = pygame.image.load('small block.png')
smallblocksize = 25

stillguy = pygame.image.load('man still.png')
manwid = 20
manhi = 50

smallman = pygame.image.load('smallman.png')
smallmanwid = 10
smallmanhi = 25

enemy = pygame.image.load('enemy.png')
enemywid = 30
enemyhi = 30

smallenemy = pygame.image.load('smallenemy.png')
smallenemysize = 15

collisionbuff = 2
maxspeed = 3

# block list: each elelemt [xpos,ypos,horizontal direction,vertical direction, length]
defaultblocklist = [[-1, 12, 0, -1, 15], [0, dh / normblocksize - 1, 1, 0, round(roomwidth / normblocksize)], [5, 8, 1, 0, 5],
             [15, 5, 1, 0, 5], [15, 6, 0, 1, 6], [27, 11, 0, 1, 1], [31, 8, 1, 0, 5], [40, 7, 1, 0, 5],
             [44, 11, 0, -1, 4]]
defaultenemylist = [[1000, 500], [1600, 320], [2000, 270]]
defaultmanpos = [0,dh - normblocksize - manhi]

def mouseon(mousepos,thingpos,thingsize):  #([mouse x,mouse y],[thing x,thing y],[thingwid,thinghi]).
    if (mousepos[0] > thingpos[0] and mousepos[0]< thingpos[0] + thingsize[0]) and (mousepos[1] > thingpos[1] and mousepos[1]< thingpos[1] + thingsize[1]):
        return 1
    else:
        return 0

def drawgrid(topleft, botright, gridsize,width):
    for i in range(0,int((botright[0]-topleft[0])/gridsize)+1):
        pygame.draw.line(gameDisplay,black, (topleft[0] + gridsize*i,topleft[1]),(topleft[0] + gridsize*i,botright[1]),width)
    for i in range(0,int((botright[1]-topleft[1])/gridsize)+1):
        pygame.draw.line(gameDisplay,black, (topleft[0],topleft[1]+ gridsize*i),(botright[0],topleft[1]+ gridsize*i),width)

def drawman(x,y):
    gameDisplay.blit(stillguy, (x, y))

def drawsmallman(x,y):
    gameDisplay.blit(smallman, (x, y))

def drawblock(x,y):
    gameDisplay.blit(normblock, (x, y))

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

def drawenemies(enemylist,camerax,cameray):
    for enemies in enemylist:
        drawenemy(enemies[0]+dw/2-camerax,enemies[1]+dh/2-cameray)

def drawsmallenemy(x,y):
    gameDisplay.blit(smallenemy, (x, y))

def drawsmallenemies(enemylist,camerax,cameray):
    for enemies in enemylist:
        drawsmallenemy(enemies[0]*smallblocksize+camerax + smallenemysize/2,enemies[1]*smallblocksize+smallenemysize/2+cameray)

def mainmenu():
    mousepos = pygame.mouse.get_pos()
    mousebuttons = pygame.mouse.get_pressed()
    while 1 == 1:
        for event in pygame.event.get():
            if event.type == pygame.MOUSEMOTION:
                mousepos = pygame.mouse.get_pos()
            if event.type == pygame.MOUSEBUTTONUP:
                mousebuttons = pygame.mouse.get_pressed()
            if event.type == pygame.MOUSEBUTTONDOWN:
                mousebuttons = pygame.mouse.get_pressed()
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()

        if mouseon(mousepos,[leveleditorx,leveleditory],[leveledwid,leveledhi]) and mousebuttons[0] == 1:
            return 1
        if mouseon(mousepos,[quickplayx,quickplayy],[quickplaywid,quickplayhi]) and mousebuttons[0] == 1:
            return 2
        if mouseon(mousepos,[quickaix,quickaiy],[quickaiwid,quickaihi]) and mousebuttons[0] == 1:
            return 3
        gameDisplay.fill(white)
        gameDisplay.blit(leveleditor,(leveleditorx,leveleditory))
        gameDisplay.blit(welcome, (welcomex, welcomey))
        gameDisplay.blit(quickplay, (quickplayx, quickplayy))
        gameDisplay.blit(quickai, (quickaix, quickaiy))
        pygame.display.update()

def leveleditorloop():
    mousepos = pygame.mouse.get_pos()
    mousebuttons = pygame.mouse.get_pressed()
    gridtop = 300
    gridleft = 25
    guydispx = 70
    guydispy = 120
    enemydispx = 170
    enemydispy = 135
    blockdispx = 120
    blockdispy = 200
    topleft = [gridleft,gridtop]
    botright = [gridleft+roomwidth*(smallblocksize/normblocksize),gridtop+dh*(smallblocksize/normblocksize)]
    manpos = [1,int((botright[1]-topleft[1])/smallblocksize)-2]
    blocks = [[0,0,0,1,int((botright[1]-topleft[1])/smallblocksize)],[0,0,1,0,int((botright[0]-topleft[0])/smallblocksize)*0],[0,int((botright[1]-topleft[1])/smallblocksize)-1,1,0,int((botright[0]-topleft[0])/smallblocksize)],[int((botright[0]-topleft[0])/smallblocksize)-1,0,0,1,int((botright[1]-topleft[1])/smallblocksize)]]
    enemies = []
    objtype = 0
    rectbuffer = 12
    rectwid = 7
    while 1 == 1:
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_q:
                    return -1
                if event.key == pygame.K_n:
                    objtype = 0
                if event.key == pygame.K_b:
                    objtype = 1
                if event.key == pygame.K_e:
                    objtype = 2
                if event.key == pygame.K_m:
                    objtype = 3
            if event.type == pygame.MOUSEMOTION:
                mousepos = pygame.mouse.get_pos()
            if event.type == pygame.MOUSEBUTTONUP:
                mousebuttons = pygame.mouse.get_pressed()
            if event.type == pygame.MOUSEBUTTONDOWN:
                mousebuttons = pygame.mouse.get_pressed()
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
        if mouseon(mousepos,[topleft[0],topleft[1]],[botright[0]-topleft[0],botright[1]-topleft[1]]) and mousebuttons[0]==1:
            if objtype == 1:
                flag = 0
                for block in blocks:
                    if block == [int((mousepos[0]-topleft[0])/smallblocksize),int((mousepos[1]-topleft[1])/smallblocksize),0,1,1]:
                        flag = 1
                if flag == 0:
                    blocks.append([int((mousepos[0]-topleft[0])/smallblocksize),int((mousepos[1]-topleft[1])/smallblocksize),0,1,1])
            if objtype == 2:
                flag = 0
                for enemy in enemies:
                    if enemy == [int((mousepos[0] - topleft[0]) / smallblocksize), int((mousepos[1] - topleft[1]) / smallblocksize)]:
                        flag = 1
                if flag == 0:
                    enemies.append(
                    [int((mousepos[0] - topleft[0]) / smallblocksize), int((mousepos[1] - topleft[1]) / smallblocksize)])
            if objtype == 3:
                manpos = [int((mousepos[0] - topleft[0]) / smallblocksize), int((mousepos[1] - topleft[1]) / smallblocksize)]
        if mouseon(mousepos,[topleft[0],topleft[1]],[botright[0]-topleft[0],botright[1]-topleft[1]]) and mousebuttons[2]==1:
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

        if mouseon(mousepos, [blockdispx, blockdispy], [normblocksize, normblocksize]) and mousebuttons[0] == 1:
            objtype = 1
        if mouseon(mousepos, [enemydispx, enemydispy], [enemywid, enemyhi]) and mousebuttons[0] == 1:
            objtype = 2
        if mouseon(mousepos, [guydispx, guydispy], [manwid, manhi]) and mousebuttons[0] == 1:
            objtype = 3

        if mouseon(mousepos,[userplayx,userplayy],[userplaywid,userplayhi]) and mousebuttons[0] ==1:
            manpos[0] = manpos[0]*normblocksize
            manpos[1] = manpos[1] * normblocksize
            for enemy in enemies:
                enemy[0]= enemy[0]*normblocksize
                enemy[1] = enemy[1] * normblocksize
            quickgameloop(blocks,enemies,manpos)
            return -1
        if mouseon(mousepos, [ailearnx, ailearny], [ailearnwid, ailearnhi]) and mousebuttons[0] == 1:
            manpos[0] = manpos[0] * normblocksize
            manpos[1] = manpos[1] * normblocksize
            for enemy in enemies:
                enemy[0] = enemy[0] * normblocksize
                enemy[1] = enemy[1] * normblocksize
            quickAIloop(blocks, enemies, manpos,1)
            return -1
        if mouseon(mousepos, [aifinishx, aifinishy], [aifinishwid, aifinishhi]) and mousebuttons[0] == 1:
            manpos[0] = manpos[0] * normblocksize
            manpos[1] = manpos[1] * normblocksize
            for enemy in enemies:
                enemy[0] = enemy[0] * normblocksize
                enemy[1] = enemy[1] * normblocksize
            quickAIloop(blocks, enemies, manpos,0)
            return -1
        gameDisplay.fill(white)
        if objtype == 1:
            pygame.draw.rect(gameDisplay, red, [blockdispx - rectbuffer,blockdispy - rectbuffer,normblocksize+2*rectbuffer,normblocksize+2*rectbuffer],rectwid)
        if objtype == 2:
            pygame.draw.rect(gameDisplay, red, [enemydispx - rectbuffer,enemydispy - rectbuffer,enemywid+2*rectbuffer,enemyhi+2*rectbuffer],rectwid)
        if objtype == 3:
            pygame.draw.rect(gameDisplay, red, [guydispx - rectbuffer,guydispy - rectbuffer,manwid+2*rectbuffer,manhi+2*rectbuffer],rectwid)

        drawgrid(topleft, botright, smallblocksize, 1)
        drawsmallman(manpos[0]*smallblocksize+topleft[0]+ smallmanwid/2,manpos[1]*smallblocksize+topleft[1])
        drawsmallenemies(enemies,topleft[0],topleft[1])
        drawsmallblockstrips(blocks, topleft[0], topleft[1])
        gameDisplay.blit(userplay, (userplayx, userplayy))
        gameDisplay.blit(ailearn, (ailearnx, ailearny))
        gameDisplay.blit(aifinish, (aifinishx, aifinishy))
        gameDisplay.blit(select,(selectx,selecty))
        drawman(guydispx,guydispy)
        drawenemy(enemydispx, enemydispy)
        drawblock(blockdispx, blockdispy)

        pygame.display.update()


def quickAIgame(playerlists,currsteps,repeat,totalsteps,blocklist,enemylist,manpos,graphics):

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

    enbouncesp = 2
    clockspeed = 1000  # 300 ideal
    horspeed = 1.2
    enspeed = 0.8
    #roomwidth = 3000
    roomheight = dh
    screenbuffer = 300
    jumpspeed = 3.8
    gravacc = 0.03

    # block list: each elelemt [xpos,ypos,horizontal direction,vertical direction, length]
    enemyspeeds = []
    for _ in enemylist:
        enemyspeeds.append([-enspeed,0])

    for i in range(0,len(playerlists)):
        deadenemies.append([])
        for _ in enemylist:
            deadenemies[i].append(0)

    encollef = []
    encolrig = []
    encoltop = []
    encolbot = []

    for _ in enemylist:
        encollef.append(1)
        encolrig.append(1)
        encoltop.append(1)
        encolbot.append(1)

    camerax = manxabs[0]+dw/2 - 50
    cameray = dh/2

    frame = 0

    while frame < currsteps:
        #
        #check user input
        #
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_q:
                    return -1
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()

        #
        #motion stuff here
        #

        for i in range(0,len(enemylist)):
            enemyspeeds[i][1]=(enemyspeeds[i][1]+gravacc*encoltop[i])*(enemyspeeds[i][1]<maxspeed)+maxspeed*(enemyspeeds[i][1]>=maxspeed)
            enemylist[i][1]=enemylist[i][1]+enemyspeeds[i][1]

            enemylist[i][0] = enemylist[i][0]+enemyspeeds[i][0]

        for i in range(0,len(playerlists)):
            if dead[i]==0:

                manxabs[i] = manxabs[i]+(-horspeed*(playerlists[i][min(round(frame/repeat),totalsteps-1)] == 0 or playerlists[i][min(round(frame/repeat),totalsteps-1)] == 3))*rightcoll[i]+(horspeed*(playerlists[i][min(round(frame/repeat),totalsteps-1)] == 1 or playerlists[i][min(round(frame/repeat),totalsteps-1)] == 4))*leftcoll[i]
                manxrel[i] = manxabs[i]+dw/2-camerax

                manyspeed[i] = (manyspeed[i] + gravacc*topcoll[i])*(manyspeed[i] < maxspeed)+maxspeed*(manyspeed[i]>=maxspeed)
                manyabs[i] = manyabs[i] + manyspeed[i]
                manyrel[i] = manyabs[i] + dh/2 - cameray



        if manxrel[manxabs.index(max(manxabs))]+manwid/2<screenbuffer and ((-horspeed*(playerlists[manxabs.index(max(manxabs))][min(round(frame/repeat),totalsteps-1)] == 0 or playerlists[manxabs.index(max(manxabs))][min(round(frame/repeat),totalsteps-1)] == 3))*leftcoll[manxabs.index(max(manxabs))]+(horspeed*(playerlists[manxabs.index(max(manxabs))][min(round(frame/repeat),totalsteps-1)] == 1))*rightcoll[manxabs.index(max(manxabs))])<0 and camerax>dw/2:
            camerax = camerax - horspeed
        elif manxrel[manxabs.index(max(manxabs))]+manwid/2>dw-screenbuffer and ((-horspeed*(playerlists[manxabs.index(max(manxabs))][min(round(frame/repeat),totalsteps-1)] == 0 or playerlists[manxabs.index(max(manxabs))][min(round(frame/repeat),totalsteps-1)] == 3))*leftcoll[manxabs.index(max(manxabs))]+(horspeed*(playerlists[manxabs.index(max(manxabs))][min(round(frame/repeat),totalsteps-1)] == 1 or playerlists[manxabs.index(max(manxabs))][min(round(frame/repeat),totalsteps-1)] == 4))*rightcoll[manxabs.index(max(manxabs))])>0 and camerax<roomwidth-dw/2:
            camerax = camerax + horspeed


        #
        #display stuff here
        #
        if graphics == 1:
            gameDisplay.fill(white)
            drawblockstrips(blocklist,camerax,cameray)
            drawenemies(enemylist,camerax,cameray)
            for i in range(0,len(playerlists)):
                if dead[i] == 0:
                    drawman(manxrel[i], manyrel[i])
        else:
            gameDisplay.fill(white)
            pygame.draw.rect(gameDisplay, red, [dw/2,dh/2,50,50])  # drawing enemy rectangles


        #
        #game checks here
        #

        #block string collision checks

        for i in range(0,len(playerlists)):
            blkchncollef[i] = 0
            blkchncolrig[i] = 0
            blkchncolup[i] = 0
            blkchncoldow[i] = 0
            deathcoll[i] = 0
            goodcoll[i] = 0
            collindex[i] = 0

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
            lbound = normblocksize * (blocks[0] * (blocks[2] != -1) + (blocks[0] - blocks[4] + 1) * (blocks[2] == -1))
            rbound = normblocksize * ((blocks[0] + blocks[4]) * (blocks[2] == 1) + (blocks[0] + 1) * (blocks[2] != 1))
            ubound = normblocksize * (blocks[1] * (blocks[3] != -1) + (blocks[1] - blocks[4] + 1) * (blocks[3] == -1))
            dbound = normblocksize * ((blocks[1] + blocks[4]) * (blocks[3] == 1) + (blocks[1] + 1) * (blocks[3] != 1))

            for i in range(0,len(playerlists)):
                if (manxabs[i] >= lbound - manwid - collisionbuff and manxabs[i] <= lbound - manwid + collisionbuff) and ((manyabs[i] >= ubound and manyabs[i] <= dbound) or (manyabs[i] + manhi >= ubound and manyabs[i] + manhi <= dbound) or (manyabs[i] + manhi <= dbound and manyabs[i] >= ubound)):
                    blkchncollef[i] = 1
                if (manxabs[i] >= rbound - collisionbuff and manxabs[i] <= rbound + collisionbuff) and ((manyabs[i] >= ubound and manyabs[i] <= dbound) or (manyabs[i] + manhi >= ubound and manyabs[i] + manhi <= dbound) or (manyabs[i] + manhi <= dbound and manyabs[i] >= ubound)):
                    blkchncolrig[i] = 1
                if (manyabs[i]>= dbound - collisionbuff and manyabs[i]<= dbound + collisionbuff) and ((manxabs[i]>= lbound and manxabs[i]<= rbound) or (manxabs[i]+ manwid >= lbound and manxabs[i]+ manwid <= rbound) or (manxabs[i]+ manwid <= rbound and manxabs[i]>= lbound)):
                    blkchncoldow[i] = 1
                    manyspeed[i] = 0
                if (manyabs[i]+ manhi >= ubound - collisionbuff and manyabs[i]+ manhi <= ubound + collisionbuff) and ((manxabs[i]>= lbound and manxabs[i]<= rbound) or (manxabs[i]+ manwid >= lbound and manxabs[i]+ manwid <= rbound) or (manxabs[i]+ manwid <= rbound and manxabs[i]>= lbound)):
                    blkchncolup[i] = 1
                    if playerlists[i][min(round(frame/repeat),totalsteps-1)] >= 2:
                        manyspeed[i] = -jumpspeed
                    else:
                        manyspeed[i] = 0
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

        for i in range(0,len(enemylist)):
            for j in range(0,len(playerlists)) :
                if (enemylist[i][0] >= manxabs[j]- enemywid - collisionbuff and enemylist[i][
                    0] <= manxabs[j]- enemywid + collisionbuff) and (
                        (enemylist[i][1] >= manyabs[j]and enemylist[i][1] <= manyabs[j]+manhi) or (
                        enemylist[i][1] + enemyhi >= manyabs[j]and enemylist[i][1] + enemyhi <= manyabs[j]+manhi) or (
                                enemylist[i][1] + enemyhi <= manyabs[j]+manhi and enemylist[i][1] >= manyabs[j])):
                    deathcoll[j] = 1
                    collindex[j] = i
                if (enemylist[i][0] >= manxabs[j]+manwid - collisionbuff and enemylist[i][0] <= manxabs[j]+manwid + collisionbuff) and (
                        (enemylist[i][1] >= manyabs[j]and enemylist[i][1] <= manyabs[j]+manhi) or (
                        enemylist[i][1] + enemyhi >= manyabs[j]and enemylist[i][1] + enemyhi <= manyabs[j]+manhi) or (
                                enemylist[i][1] + enemyhi <= manyabs[j]+manhi and enemylist[i][1] >= manyabs[j])):
                    deathcoll[j] = 1
                    collindex[j] = i
                if (enemylist[i][1] >= manyabs[j]+manhi - collisionbuff-10 and enemylist[i][1] <= manyabs[j]+ manhi + collisionbuff+10) and (
                        (enemylist[i][0] >= manxabs[j]and enemylist[i][0] <= manxabs[j]+manwid) or (
                        enemylist[i][0] + enemywid >= manxabs[j]and enemylist[i][0] + enemywid <= manxabs[j]+manwid) or (
                                enemylist[i][0] + enemywid <= manxabs[j]+manwid and enemylist[i][0] >= manxabs[j]) or (manxabs[j]>= enemylist[i][0] and manxabs[j]+ manwid <= enemylist[i][0]+enemywid)):
                    goodcoll[j] = 1
                    collindex[j] = i
                if (enemylist[i][1] + enemyhi >= manyabs[j]- collisionbuff and enemylist[i][
                    1] + enemyhi <= manyabs[j]+ collisionbuff) and (
                        (enemylist[i][0] >= manxabs[j]and enemylist[i][0] <= manxabs[j]+manwid) or (
                        enemylist[i][0] + enemywid >= manxabs[j]and enemylist[i][0] + enemywid <= manxabs[j]+manwid) or (
                                enemylist[i][0] + enemywid <= manxabs[j]+manwid and enemylist[i][0] >= manxabs[j]) or (manxabs[j]>= enemylist[i][0] and manxabs[j]+ manwid <= enemylist[i][0]+enemywid)):
                    deathcoll[j] = 1
                    collindex[j] = i


        #general collision checks
        for i in range(0,len(playerlists)):
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
            if deathcoll[i] == 1 and deadenemies[i][collindex[i]]== 0:
                dead[i] = 1
            if goodcoll[i] == 1 and deadenemies[i][collindex[i]]== 0:
                manyspeed[i] = -enbouncesp
                if playerlists[i][min(round(frame/repeat),totalsteps-1)] >= 2:
                    manyspeed[i] = -jumpspeed
                deadenemies[i][collindex[i]] = 1
        #
        #end loop stuff
        #
        pygame.display.update()
        #clock.tick(clockspeed)
        frame = frame+1
    outdata = []
    for i in range(0,len(playerlists)):
        outdata.append(math.sqrt(manxabs[i]**2+(roomheight-manyabs[i])**2))      # win condition function
    return (outdata)

def quickAIloop(blocklist,enemylist,manpos,graphics):
    numplayers = 150
    genswait = 3
    finalgen = 50
    playersteps = []
    keepers = 10
    mutation = 0.1
    repeat = 48
    stepsadded = 7  # THIS FACTOR IS NUMBER OF CHOICES
    totalsteps = stepsadded
    # generate random directions, 0 = LEFT, 1 = RIGHT, 2 = UP, 3 = Up LEFT, 4 = up RIGHT
    for i in range(0, numplayers):
        playersteps.append([])
        for _ in range(0, stepsadded):
            playersteps[i].append(
                random.randint(0, 4))  # implement -1 to introduce stopping, put at mutation as well, end of program
            # while playersteps[i] == 2:
            #   playersteps[i] = random.randint(0,4)           ELIMINATES OPTION 2 (jump straight)
    winnersteps = []
    for generation in range(1, finalgen + 1):

        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_q:
                    return -1
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
        savedata = []
        testdata = quickAIgame(playersteps, totalsteps * repeat,repeat,totalsteps,blocklist,enemylist,manpos,graphics)
        print("finished generation",generation)
        if testdata == -1:
            return -1
        if generation == finalgen:
            winnersteps = playersteps[testdata.index(max(testdata))]
        for _ in range(0, keepers):
            goodindex = testdata.index(max(testdata))
            savedata.append(playersteps[goodindex])
            del testdata[goodindex]
            del playersteps[goodindex]
        if generation % genswait == 0 and generation != finalgen:
            totalsteps = totalsteps + stepsadded
        playersteps = []

        for k in range(0, round(numplayers / len(savedata))):
            for j in range(0, len(savedata)):
                playersteps.append([])
                for i in range(0, totalsteps):
                    if i < totalsteps - stepsadded:
                        playersteps[k * len(savedata) + j].append(savedata[j][i])
                    elif generation % genswait == 0 or random.randint(0, 100) <= mutation * 100:
                        playersteps[k * len(savedata) + j].append(random.randint(0, 4))
                    else:
                        playersteps[k * len(savedata) + j].append(savedata[j][i])
        pygame.display.update()
    quickAIgame([winnersteps], totalsteps * repeat, repeat, totalsteps, blocklist, enemylist, manpos,1)

def quickgameloop(blocklist,enemylist,manpos):

    enbouncesp = 2
    dead = 0
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

    camerax = manxabs+dw/2 - 50
    cameray = dh/2

    while dead == 0:
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
            enemyspeeds[i][1]=(enemyspeeds[i][1]+gravacc*encoltop[i])*(enemyspeeds[i][1]<maxspeed)+maxspeed*(enemyspeeds[i][1]>=maxspeed)
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
        drawenemies(enemylist,camerax,cameray)
        drawman(manxrel, manyrel)

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
            if (manxabs >= lbound - manwid - collisionbuff and manxabs <= lbound - manwid + collisionbuff) and ((manyabs >= ubound and manyabs <= dbound) or (manyabs + manhi >= ubound and manyabs + manhi <= dbound) or (manyabs + manhi <= dbound and manyabs >= ubound)):
                blkchncollef = 1
            if (manxabs >= rbound - collisionbuff and manxabs <= rbound + collisionbuff) and ((manyabs >= ubound and manyabs <= dbound) or (manyabs + manhi >= ubound and manyabs + manhi <= dbound) or (manyabs + manhi <= dbound and manyabs >= ubound)):
                blkchncolrig = 1
            if (manyabs >= dbound - collisionbuff and manyabs <= dbound + collisionbuff) and ((manxabs >= lbound and manxabs <= rbound) or (manxabs + manwid >= lbound and manxabs + manwid <= rbound) or (manxabs + manwid <= rbound and manxabs >= lbound)):
                blkchncoldow = 1
                manyspeed = 0
            if (manyabs + manhi >= ubound - collisionbuff and manyabs + manhi <= ubound + collisionbuff) and ((manxabs >= lbound and manxabs <= rbound) or (manxabs + manwid >= lbound and manxabs + manwid <= rbound) or (manxabs + manwid <= rbound and manxabs >= lbound)):
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
                            enemylist[i][0] + enemywid <= manxabs+manwid and enemylist[i][0] >= manxabs) or (manxabs >= enemylist[i][0] and manxabs + manwid <= enemylist[i][0]+enemywid)):
                goodcoll = 1
                collindex = i
            if (enemylist[i][1] + enemyhi >= manyabs - collisionbuff and enemylist[i][
                1] + enemyhi <= manyabs + collisionbuff) and (
                    (enemylist[i][0] >= manxabs and enemylist[i][0] <= manxabs+manwid) or (
                    enemylist[i][0] + enemywid >= manxabs and enemylist[i][0] + enemywid <= manxabs+manwid) or (
                            enemylist[i][0] + enemywid <= manxabs+manwid and enemylist[i][0] >= manxabs) or (manxabs >= enemylist[i][0] and manxabs + manwid <= enemylist[i][0]+enemywid)):
                deathcoll = 1
                collindex = i



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


while 1==1:
    directive = mainmenu()
    if directive == 1:
        leveleditorloop()
    if directive == 2:
        quickgameloop(defaultblocklist,defaultenemylist,defaultmanpos)
    if directive == 3:
        quickAIloop(defaultblocklist,defaultenemylist,defaultmanpos,1)



pygame.quit()
quit()

