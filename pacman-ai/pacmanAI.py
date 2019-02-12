import random
import tflearn
import numpy as np
from tflearn.layers.core import input_data, dropout, fully_connected
from tflearn.layers.estimator import regression
from statistics import mean, median
from collections import Counter
import pygame
import time         # importing libraries
import math

LR = 1e-8
goal_steps = 2500
score_req = 900
initial_games = 1000
nepocs = 1
switchtime = 4
dor = 0.8
games = 5

inputdim = 11
enemythresh = 100
borderthresh = 100

dh = 600
dw = 800        # define room boundaries

black = (0, 0, 0)
white = (255, 255, 255) # defining basic colour codes
red = (255, 0, 0)

pacImg = pygame.image.load('pacman.png')        # loading the object sprite
pacwid = 75                                     # dimensions of the pacman object sprite
pachi = 75


def initpop():
    traindata = []
    scores = []
    goodscores = []
    for _ in range(initial_games):
        score = 0
        gamemem = []
        prevob = []

        observation, score = gamelooprandom()
        gamemem = observation

        if score >= score_req:
            goodscores.append(score)
            for data in gamemem:
                if data[0] == 0:
                    output = [1, 0, 0, 0, 0 ,0 ,0 ,0, 0]
                elif data[0] == 1/8:
                    output = [0, 1, 0, 0, 0 ,0 ,0 ,0, 0]
                elif data[0] == 2/8:
                    output = [0, 0, 1, 0, 0 ,0 ,0 ,0, 0]
                elif data[0] == 3/8:
                    output = [0, 0, 0, 1, 0 ,0 ,0 ,0, 0]
                elif data[0] == 4/8:
                    output = [0, 0, 0, 0, 1,0 ,0 ,0, 0]
                elif data[0] == 5/8:
                    output = [0, 0, 0, 0, 0 ,1 ,0 ,0, 0]
                elif data[0] == 6/8:
                    output = [0, 0, 0, 0, 0 ,0 ,1 ,0, 0]
                elif data[0] == 7/8:
                    output = [0, 0, 0, 0, 0 ,0 ,0 ,1, 0]
                elif data[0] == 8/8:
                    output = [0, 0, 0, 0, 0 ,0 ,0 ,0, 1]
                traindata.append([[data[5]],[data[1]],[data[2]],[data[3]],[data[4]],output,[data[6]],[data[7]],[data[8]],[data[9]],[data[10]],[data[11]]])

        scores.append(score)

    traindatasave = np.array(traindata)
    np.save('saved.npy',traindatasave)

    print('Ave good score', mean(goodscores))
    print('Med good score', median(goodscores))
    print(Counter(goodscores))

    return traindata

def neuralnet(input_size):
    network = input_data(shape = [None, input_size,1], name = 'input')

    network = fully_connected(network,512,activation='relu')
    network = dropout(network, dor)

#    network = fully_connected(network,256,activation='relu')
 #   network = dropout(network, dor)
#
 #   network = fully_connected(network,512,activation='relu')
  #  network = dropout(network, dor)
#
 #   network = fully_connected(network,256,activation='relu')
  #  network = dropout(network, dor)
#
 #   network = fully_connected(network,128,activation='relu')
  #  network = dropout(network, dor)

    network = fully_connected(network, 9, activation='sigmoid')
    network = regression(network, optimizer='Adam',learning_rate=LR, loss='categorical_crossentropy',name='targets')

    model = tflearn.DNN(network, tensorboard_dir='log')

    return model

def trainmodel(traindata,testin,testout,model=False):
    input = []
    for i in traindata:
        input.append(i[0])
    #for i in traindata:
        input.append(i[1])
    #for i in traindata:
        input.append(i[2])
    #for i in traindata:
        input.append(i[3])
    #for i in traindata:
        input.append(i[4])
        input.append(i[6])
        input.append(i[7])
        input.append(i[8])
        input.append(i[9])
        input.append(i[10])
        input.append(i[11])


    X = np.array(input).reshape(-1,inputdim,1)
    y = [i[5] for i in traindata]
    if not model:
        model = neuralnet(input_size=len(X[0]))

    model.fit({'input':X},{'targets':y}, n_epoch=nepocs,validation_set=({'input': np.array(testin).reshape(-1,inputdim,1)},{'targets': testout}),snapshot_step=500, show_metric=True, run_id='mnist') #MAYBE NEED [] around in and out
    pygame.event.pump()
    return model


def dotsgood(score):                        # funtion for rendering score
    font = pygame.font.SysFont(None, 25)
    text = font.render("Score:" + str(score), True, black)
    gameDisplay.blit(text,(0,0))            # blit the text to the screen

def things(x,y,w,h,c):
    pygame.draw.rect(gameDisplay,c,[x,y,w,h])   # drawing enemy rectangles


def text_objects(text, font):
    textSurf = font.render(text, True, black)       # setting up text displays
    return textSurf, textSurf.get_rect()

def message_display(text):
    largeText = pygame.font.Font('freesansbold.ttf',115)
    TextSurf, TextRect = text_objects(text, largeText)
    TextRect.center = ((dw/2),(dh/2))       # defining message text and location
    gameDisplay.blit(TextSurf, TextRect)

    pygame.display.update()         # update the display

    time.sleep(2)           # pause the game for 2 seconds

    gameloopgraphics()          # restart the game loop

def crash():
    message_display('you died')

def pac(x,y):
    gameDisplay.blit(pacImg,(x,y))      # plot the position of pacman

def gamelooprandom():  # main loop for playing the game

    # defining game variables
    clockspeed = 90  # speed of the game (bigger = faster)
    x = (dw - pacwid) / 2  # starting position (centre of screen)
    y = (dh - pachi) / 2
    speed = 4  # speed of pacman
    objfact = 0.75  # proportional enemy speed

    addobj = 5  # frequency of adding an enemy (per score)
    objcount = 1  # starting number of enemies
    anglevar = 20  # accuracy hitting pacman
    objw = 50  # dimensions of enemies
    objh = 50
    objspeed = speed * objfact
    incfreq = 1  # how often the speed increases
    increase = 0  # how much the speed increases each time
    score = 0  # initial score
    crashed = 0 # crashed flag
    gameduration = 0 # length of game frames
    observes = []

    objyi = []
    objxi = []  # defining arrays to store enemy positions
    objdir = []

    for i in range(0, objcount):
        objyi.append(0)
        objxi.append(0)
        objdir.append(0)

    for i in range(0, objcount):  # defining initial enemy traits
        side = random.randrange(0, 2)
        if side == 1:
            horside = random.randrange(-1, 2, 2)
            horrand = 0
            verside = 0
            verrand = 1
        else:
            horside = 0
            horrand = 1
            verside = random.randrange(-1, 2, 2)
            verrand = 0
        porp = random.randrange(0, 100) / 100
        objxi[i] = abs(horside * (
                    dw - pacwid) / 2) + horside * dw / 2 + horrand * porp * dw  # start somewhere on the edge of the screen
        objyi[i] = abs(verside * (dh - pachi) / 2) + verside * dh / 2 + verrand * porp * dh
        if x - objxi[i] == 0:
            angle = math.atan((y - objyi[i]) / (x - objxi[i]+0.00001))
        else:
            angle = math.atan((y - objyi[i]) / (x - objxi[i]))

        if x - objxi[i] < 0:
            angle = 3.14159265 + angle  # aim within the given accuracy of pacman
        angle = int(angle * 180 / 3.1415926535)
        objdir[i] = random.randrange(angle - anglevar, angle + anglevar) * 3.1415926535 / 180

    for duration in range(goal_steps):  # gameplay phase
        if duration % switchtime ==0:
            choice = random.randrange(0,9)

        if choice == 0:                     # choosing random directions
            directions = [0,0,0,0]          # assigning to array
        elif choice == 1:                   # [left, right, up, down]
            directions = [1,0,0,0]
        elif choice == 2:
            directions = [0,1,0,0]
        elif choice == 3:
            directions = [0,0,1,0]
        elif choice == 4:
            directions = [0,0,0,1]
        elif choice == 5:
            directions = [1,0,1,0]
        elif choice == 6:
            directions = [1,0,0,1]
        elif choice == 7:
            directions = [0,1,1,0]
        elif choice == 8:
            directions = [0,1,0,1]
        else:
            directions = [0,0,0,0]


        x += speed*(directions[1]-directions[0])  # update pacmans position
        y += speed*(directions[3]-directions[2])

        for i in range(0, objcount):
            objxi[i] += objspeed * math.cos(objdir[i])  # update enemy positions
            objyi[i] += objspeed * math.sin(objdir[i])

        if x > dw - pacwid / 2 or x < -pacwid / 2:  # check if pacman off screen
            # crashed = 1
            if x > dw - pacwid / 2:
                x = 0
            else:  # screenwarp
                x = dw - pacwid
        if y > dh - pachi / 2 or y < -pachi / 2:
            # crashed = 1
            if y > dh - pachi / 2:
                y = 0
            else:  # screenwarp
                y = dh - pachi

        for i in range(0, objcount):  # enemy checks

            if objyi[i] < -objh or objyi[i] > dh or objxi[i] < -objw or objxi[i] > dw:  # if enemy off screen

                side = random.randrange(0, 2)
                if side == 1:
                    horside = random.randrange(-1, 2, 2)
                    horrand = 0
                    verside = 0
                    verrand = 1
                else:  # generate new enemy positions
                    horside = 0
                    horrand = 1
                    verside = random.randrange(-1, 2, 2)
                    verrand = 0
                porp = random.randrange(0, 100) / 100
                objxi[i] = abs(horside * (dw - pacwid) / 2) + horside * dw / 2 + horrand * porp * dw
                objyi[i] = abs(verside * (dh - pachi) / 2) + verside * dh / 2 + verrand * porp * dh  # respawn enemy
                if x - objxi[i] == 0:
                    angle = math.atan((y - objyi[i]) / (x - objxi[i] + 0.00001))
                else:
                    angle = math.atan((y - objyi[i]) / (x - objxi[i]))
                if x - objxi[i] < 0:
                    angle = 3.14159265 + angle
                angle = int(angle * 180 / 3.1415926535)
                objdir[i] = random.randrange(angle - anglevar, angle + anglevar) * 3.1415926535 / 180

                if score % incfreq == 0:
                    objspeed += increase  # increase enemy speed

                score += 1  # increment score

                if score % addobj == 0:  # adding additional enemy

                    objcount += 1  # increment count

                    side = random.randrange(0, 2)
                    if side == 1:
                        horside = random.randrange(-1, 2, 2)
                        horrand = 0
                        verside = 0
                        verrand = 1
                    else:  # generate new position
                        horside = 0
                        horrand = 1
                        verside = random.randrange(-1, 2, 2)
                        verrand = 0
                    porp = random.randrange(0, 100) / 100
                    objxi.append(
                        abs(horside * (dw - pacwid) / 2) + horside * dw / 2 + horrand * porp * dw)  # append position list
                    objyi.append(abs(verside * (dh - pachi) / 2) + verside * dh / 2 + verrand * porp * dh)
                    if x - objxi[objcount - 1]==0:
                        angle = math.atan((y - objyi[objcount - 1]) / (x - objxi[objcount - 1]+0.0001))
                    else:
                        angle = math.atan((y - objyi[objcount - 1]) / (x - objxi[objcount - 1]))
                    if x - objxi[objcount - 1] < 0:
                        angle = 3.14159265 + angle
                    angle = int(angle * 180 / 3.1415926535)
                    objdir.append(random.randrange(angle - anglevar, angle + anglevar) * 3.1415926535 / 180)  # create new object

            if (y > objyi[i] and y < objyi[i] + objh) or (y + pachi > objyi[i] and y + pachi < objyi[i] + objh) or (
                    y < objyi[i] and y + pachi > objyi[i] + objh):
                if (x > objxi[i] and x < objxi[i] + objw) or (x + pacwid > objxi[i] and x + pacwid < objxi[i] + objw) or (
                        x < objxi[i] and x + pacwid > objxi[i] + objw):
                    crashed = 1
                    # ^^^^^ crash condition
        observes.append([choice/8,(abs(objxi[0]-x) < enemythresh),(abs(objyi[0]-y)<enemythresh),(x < borderthresh),(y < borderthresh),objdir[0]/360,(dw-x < borderthresh),(dh-y < borderthresh),(objxi[0]-x)/dw,(objyi[0]-y)/dh,x/dw,y/dh])
        if crashed == 1:
            gameduration = duration
            break
        pygame.event.pump()
    if crashed == 1:
        return observes, gameduration
    else:
        return observes, goal_steps

def gameloopusertrain():  # main loop for playing the game

    # defining game variables
    clockspeed = 90  # speed of the game (bigger = faster)
    x = (dw - pacwid) / 2  # starting position (centre of screen)
    y = (dh - pachi) / 2
    speed = 4  # speed of pacman
    objfact = 0.75  # proportional enemy speed
    ldir = 0                # directional flags
    rdir = 0
    udir = 0
    ddir = 0
    output = []
    testinputs = []
    testoutputs = []

    addobj = 5  # frequency of adding an enemy (per score)
    objcount = 1  # starting number of enemies
    anglevar = 20  # accuracy hitting pacman
    objw = 50  # dimensions of enemies
    objh = 50
    objspeed = speed * objfact
    incfreq = 1  # how often the speed increases
    increase = 0  # how much the speed increases each time
    score = 0  # initial score
    gameduration = 0  # length of game frames
    observes = []
    prevob = []

    objyi = []
    objxi = []  # defining arrays to store enemy positions
    objdir = []

    for i in range(0, objcount):
        objyi.append(0)
        objxi.append(0)
        objdir.append(0)

    for i in range(0, objcount):  # defining initial enemy traits
        side = random.randrange(0, 2)
        if side == 1:
            horside = random.randrange(-1, 2, 2)
            horrand = 0
            verside = 0
            verrand = 1
        else:
            horside = 0
            horrand = 1
            verside = random.randrange(-1, 2, 2)
            verrand = 0
        porp = random.randrange(0, 100) / 100
        objxi[i] = abs(horside * (
                    dw - pacwid) / 2) + horside * dw / 2 + horrand * porp * dw  # start somewhere on the edge of the screen
        objyi[i] = abs(verside * (dh - pachi) / 2) + verside * dh / 2 + verrand * porp * dh
        angle = math.atan((y - objyi[i]) / (x - objxi[i]))
        if x - objxi[i] < 0:
            angle = 3.14159265 + angle  # aim within the given accuracy of pacman
        angle = int(angle * 180 / 3.1415926535)
        objdir[i] = random.randrange(angle - anglevar, angle + anglevar) * 3.1415926535 / 180

    crashed = 0

    for duration in range(100000):  # gameplay phase  # gameplay phase
        for event in pygame.event.get():        # checking events occuring on the frame

            if event.type == pygame.QUIT:       # exit condition
                pygame.quit()
                quit()

            if event.type == pygame.KEYDOWN:            # checking keystrokes for direction
                if event.key == pygame.K_LEFT:
                    ldir = -speed
                elif event.key == pygame.K_RIGHT:
                    rdir = speed
                if event.key == pygame.K_DOWN:
                    ddir = speed
                elif event.key == pygame.K_UP:
                    udir = -speed
            if event.type == pygame.KEYUP:              # key release checks
                if event.key == pygame.K_RIGHT:
                    rdir = 0
                elif event.key == pygame.K_DOWN:
                    ddir = 0
                elif event.key == pygame.K_UP:
                    udir = 0
                elif event.key == pygame.K_LEFT:
                    ldir = 0
        if ldir +rdir == 0 and udir +ddir ==0:
            output = [1,0,0,0,0,0,0,0,0]
        elif ldir +rdir == -speed and udir +ddir ==0:
            output = [0, 1, 0, 0, 0, 0, 0, 0, 0]
        elif ldir +rdir == speed and udir +ddir ==0:
            output = [0, 0, 1, 0, 0, 0, 0, 0, 0]
        elif ldir +rdir == 0 and udir +ddir ==-speed:
            output = [0, 0, 0, 1, 0, 0, 0, 0, 0]
        elif ldir +rdir == 0 and udir +ddir ==speed:
            output = [0, 0, 0, 0, 1, 0, 0, 0, 0]
        elif ldir +rdir == -speed and udir +ddir ==-speed:
            output = [0, 0, 0, 0, 0, 1, 0, 0, 0]
        elif ldir +rdir == -speed and udir +ddir ==speed:
            output = [0, 0, 0, 0, 0, 0, 1, 0, 0]
        elif ldir +rdir == speed and udir +ddir ==-speed:
            output = [0, 0, 0, 0, 0, 0, 0, 1, 0]
        elif ldir +rdir == speed and udir +ddir ==speed:
            output = [0, 0, 0, 0, 0, 0, 0, 0, 1]
        x += ldir + rdir  # update pacmans position
        y += udir + ddir
        gameDisplay.fill(white)  # background colour

        for i in range(0, objcount):
            things(objxi[i], objyi[i], objw, objh, red)  # draw the enemy positions

            objxi[i] += objspeed * math.cos(objdir[i])  # update enemy positions
            objyi[i] += objspeed * math.sin(objdir[i])

        pac(x, y)  # draw pacmans position
        dotsgood(score)  # draw score

        if x > dw - pacwid / 2 or x < -pacwid / 2:  # check if pacman off screen
            crashed = 1
        if y > dh - pachi / 2 or y < -pachi / 2:
            crashed = 1

        for i in range(0, objcount):  # enemy checks

            if objyi[i] < -objh or objyi[i] > dh or objxi[i] < -objw or objxi[i] > dw:  # if enemy off screen

                side = random.randrange(0, 2)
                if side == 1:
                    horside = random.randrange(-1, 2, 2)
                    horrand = 0
                    verside = 0
                    verrand = 1
                else:  # generate new enemy positions
                    horside = 0
                    horrand = 1
                    verside = random.randrange(-1, 2, 2)
                    verrand = 0
                porp = random.randrange(0, 100) / 100
                objxi[i] = abs(horside * (dw - pacwid) / 2) + horside * dw / 2 + horrand * porp * dw
                objyi[i] = abs(verside * (dh - pachi) / 2) + verside * dh / 2 + verrand * porp * dh  # respawn enemy
                angle = math.atan((y - objyi[i]) / (x - objxi[i]))
                if x - objxi[i] < 0:
                    angle = 3.14159265 + angle
                angle = int(angle * 180 / 3.1415926535)
                objdir[i] = random.randrange(angle - anglevar, angle + anglevar) * 3.1415926535 / 180

                if score % incfreq == 0:
                    objspeed += increase  # increase enemy speed

                score += 1  # increment score

                if score % addobj == 0:  # adding additional enemy

                    objcount += 1  # increment count

                    side = random.randrange(0, 2)
                    if side == 1:
                        horside = random.randrange(-1, 2, 2)
                        horrand = 0
                        verside = 0
                        verrand = 1
                    else:  # generate new position
                        horside = 0
                        horrand = 1
                        verside = random.randrange(-1, 2, 2)
                        verrand = 0
                    porp = random.randrange(0, 100) / 100
                    objxi.append(
                        abs(horside * (dw - pacwid) / 2) + horside * dw / 2 + horrand * porp * dw)  # append position list
                    objyi.append(abs(verside * (dh - pachi) / 2) + verside * dh / 2 + verrand * porp * dh)
                    angle = math.atan((y - objyi[objcount - 1]) / (x - objxi[objcount - 1]))
                    if x - objxi[objcount - 1] < 0:
                        angle = 3.14159265 + angle
                    angle = int(angle * 180 / 3.1415926535)
                    objdir.append(
                        random.randrange(angle - anglevar, angle + anglevar) * 3.1415926535 / 180)  # create new object

            if (y > objyi[i] and y < objyi[i] + objh) or (y + pachi > objyi[i] and y + pachi < objyi[i] + objh) or (
                    y < objyi[i] and y + pachi > objyi[i] + objh):
                if (x > objxi[i] and x < objxi[i] + objw) or (x + pacwid > objxi[i] and x + pacwid < objxi[i] + objw) or (
                        x < objxi[i] and x + pacwid > objxi[i] + objw):
                    crashed = 1
            # ^^^^^ crash condition

        prevob = []
        prevob.append(objdir[0]/360)
        prevob.append(abs(objxi[0]-x) < enemythresh)
        prevob.append(abs(objyi[0]-y) < enemythresh)
        prevob.append(x < borderthresh)
        prevob.append(y < borderthresh)
        prevob.append(dw-x < borderthresh)
        prevob.append(dh-y < borderthresh)
        prevob.append((objxi[0] - x)/dw)
        prevob.append((objyi[0] - y)/dh)
        prevob.append(x/dw)
        prevob.append(y/dh)
        testinputs.append(prevob)
        testoutputs.append(output)



        if crashed == 1:
            gameduration = duration
            break
        pygame.display.update()  # update screen
        clock.tick(clockspeed)  # clock progress
    if crashed == 1:
        return testinputs, testoutputs
    else:
        return testinputs, testoutputs

def gameloopgraphics(model):  # main loop for playing the game

    # defining game variables
    clockspeed = 90  # speed of the game (bigger = faster)
    x = (dw - pacwid) / 2  # starting position (centre of screen)
    y = (dh - pachi) / 2
    speed = 4  # speed of pacman
    objfact = 0.75  # proportional enemy speed

    addobj = 5  # frequency of adding an enemy (per score)
    objcount = 1  # starting number of enemies
    anglevar = 20  # accuracy hitting pacman
    objw = 50  # dimensions of enemies
    objh = 50
    objspeed = speed * objfact
    incfreq = 1  # how often the speed increases
    increase = 0  # how much the speed increases each time
    score = 0  # initial score
    gameduration = 0  # length of game frames
    observes = []
    prevob = []

    objyi = []
    objxi = []  # defining arrays to store enemy positions
    objdir = []

    for i in range(0, objcount):
        objyi.append(0)
        objxi.append(0)
        objdir.append(0)

    for i in range(0, objcount):  # defining initial enemy traits
        side = random.randrange(0, 2)
        if side == 1:
            horside = random.randrange(-1, 2, 2)
            horrand = 0
            verside = 0
            verrand = 1
        else:
            horside = 0
            horrand = 1
            verside = random.randrange(-1, 2, 2)
            verrand = 0
        porp = random.randrange(0, 100) / 100
        objxi[i] = abs(horside * (
                    dw - pacwid) / 2) + horside * dw / 2 + horrand * porp * dw  # start somewhere on the edge of the screen
        objyi[i] = abs(verside * (dh - pachi) / 2) + verside * dh / 2 + verrand * porp * dh
        angle = math.atan((y - objyi[i]) / (x - objxi[i]))
        if x - objxi[i] < 0:
            angle = 3.14159265 + angle  # aim within the given accuracy of pacman
        angle = int(angle * 180 / 3.1415926535)
        objdir[i] = random.randrange(angle - anglevar, angle + anglevar) * 3.1415926535 / 180

    crashed = 0

    for duration in range(goal_steps):  # gameplay phase  # gameplay phase
        #print(prevob)
        if len(prevob) == 0:
            choice = random.randrange(0,9)
        else:
            choice = np.argmax(model.predict(prevob.reshape(-1, len(prevob),1))[0])

        if choice == 0:                     # choosing random directions
            directions = [0,0,0,0]          # assigning to array
        elif choice == 1:                   # [left, right, up, down]
            directions = [1,0,0,0]
        elif choice == 2:
            directions = [0,1,0,0]
        elif choice == 3:
            directions = [0,0,1,0]
        elif choice == 4:
            directions = [0,0,0,1]
        elif choice == 5:
            directions = [1,0,1,0]
        elif choice == 6:
            directions = [1,0,0,1]
        elif choice == 7:
            directions = [0,1,1,0]
        elif choice == 8:
            directions = [0,1,0,1]
        else:
            directions = [0,0,0,0]


        x += speed*(directions[1]-directions[0])  # update pacmans position
        y += speed*(directions[3]-directions[2])
        gameDisplay.fill(white)  # background colour

        for i in range(0, objcount):
            things(objxi[i], objyi[i], objw, objh, red)  # draw the enemy positions

            objxi[i] += objspeed * math.cos(objdir[i])  # update enemy positions
            objyi[i] += objspeed * math.sin(objdir[i])

        pac(x, y)  # draw pacmans position
        dotsgood(score)  # draw score

        if x > dw - pacwid / 2 or x < -pacwid / 2:  # check if pacman off screen
            #crashed = 1
            if x > dw - pacwid / 2:
                x = 0
            else:                                   #screenwarp
                x = dw-pacwid
        if y > dh - pachi / 2 or y < -pachi / 2:
            #crashed = 1
            if y > dh - pachi / 2:
                y = 0
            else:                                   #screenwarp
                y = dh-pachi
        for i in range(0, objcount):  # enemy checks

            if objyi[i] < -objh or objyi[i] > dh or objxi[i] < -objw or objxi[i] > dw:  # if enemy off screen

                side = random.randrange(0, 2)
                if side == 1:
                    horside = random.randrange(-1, 2, 2)
                    horrand = 0
                    verside = 0
                    verrand = 1
                else:  # generate new enemy positions
                    horside = 0
                    horrand = 1
                    verside = random.randrange(-1, 2, 2)
                    verrand = 0
                porp = random.randrange(0, 100) / 100
                objxi[i] = abs(horside * (dw - pacwid) / 2) + horside * dw / 2 + horrand * porp * dw
                objyi[i] = abs(verside * (dh - pachi) / 2) + verside * dh / 2 + verrand * porp * dh  # respawn enemy
                angle = math.atan((y - objyi[i]) / (x - objxi[i]))
                if x - objxi[i] < 0:
                    angle = 3.14159265 + angle
                angle = int(angle * 180 / 3.1415926535)
                objdir[i] = random.randrange(angle - anglevar, angle + anglevar) * 3.1415926535 / 180

                if score % incfreq == 0:
                    objspeed += increase  # increase enemy speed

                score += 1  # increment score

                if score % addobj == 0:  # adding additional enemy

                    objcount += 1  # increment count

                    side = random.randrange(0, 2)
                    if side == 1:
                        horside = random.randrange(-1, 2, 2)
                        horrand = 0
                        verside = 0
                        verrand = 1
                    else:  # generate new position
                        horside = 0
                        horrand = 1
                        verside = random.randrange(-1, 2, 2)
                        verrand = 0
                    porp = random.randrange(0, 100) / 100
                    objxi.append(
                        abs(horside * (dw - pacwid) / 2) + horside * dw / 2 + horrand * porp * dw)  # append position list
                    objyi.append(abs(verside * (dh - pachi) / 2) + verside * dh / 2 + verrand * porp * dh)
                    angle = math.atan((y - objyi[objcount - 1]) / (x - objxi[objcount - 1]))
                    if x - objxi[objcount - 1] < 0:
                        angle = 3.14159265 + angle
                    angle = int(angle * 180 / 3.1415926535)
                    objdir.append(
                        random.randrange(angle - anglevar, angle + anglevar) * 3.1415926535 / 180)  # create new object

            if (y > objyi[i] and y < objyi[i] + objh) or (y + pachi > objyi[i] and y + pachi < objyi[i] + objh) or (
                    y < objyi[i] and y + pachi > objyi[i] + objh):
                if (x > objxi[i] and x < objxi[i] + objw) or (x + pacwid > objxi[i] and x + pacwid < objxi[i] + objw) or (
                        x < objxi[i] and x + pacwid > objxi[i] + objw):
                    crashed = 1
            # ^^^^^ crash condition
        # observes.append([choice/8, objxi/dw, objyi/dh])
        prevob = []
        prevob.append(objdir[0]/360)
        prevob.append(abs(objxi[0]-x) < enemythresh)
        prevob.append(abs(objyi[0]-y) < enemythresh)
        prevob.append(x < borderthresh)
        prevob.append(y < borderthresh)
        prevob.append(dw-x < borderthresh)
        prevob.append(dh-y < borderthresh)
        prevob.append((objxi[0] - x)/dw)
        prevob.append((objyi[0] - y)/dh)
        prevob.append(x/dw)
        prevob.append(y/dh)
        prevob = np.array(prevob)

        pygame.event.pump()
        if crashed == 1:
            gameduration = duration
            break
        pygame.display.update()  # update screen
        clock.tick(clockspeed)  # clock progress
    if crashed == 1:
        return observes, gameduration
    else:
        return observes, goal_steps


pygame.init()   # initialize pygame

gameDisplay = pygame.display.set_mode((dw, dh)) # setting up the game window
pygame.display.set_caption('testing')
clock = pygame.time.Clock()

userin,userout = gameloopusertrain()
traindata = initpop()
#print(traindata)
model = trainmodel(traindata,userin,userout)



scores = []
choices = []

for eachgame in range(games):      # running good games

    score = 0

    observes, score = gameloopgraphics(model)
    #for thing in observes:
    #    choices.append(thing[0])
    scores.append(score)


print('avg', sum(scores)/len(scores))

max=100
for _ in range (0,max):
    a = random.randrange(0, max)
    b = random.randrange(0, max)
    c = random.randrange(0, max)
    d = random.randrange(0, max)
    e = random.randrange(0, max)
    f = random.randrange(0, max)
    g = random.randrange(0, max)
    h = random.randrange(0, max)
    i = random.randrange(0, max)
    j = random.randrange(0, max)
    k = random.randrange(0, max)

    print(np.array([a, b, c, d, e, f, g, h, i, j, k]).reshape(-1, inputdim, 1)[0])
    print(model.predict(np.array([a, b, c, d, e, f, g, h, i, j, k]).reshape(-1, inputdim, 1))[0])



#print('c1: {}, C2: {}, c3: {}, C4: {}, c5: {}, C6: {}, c7: {}, C8: {}, c9: {}'.format(choices.count(1)/len(choices),choices.count(0)/len(choices)))