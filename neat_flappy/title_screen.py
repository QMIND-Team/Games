import pygame
import os
import time
import random
import math
import flappy_ai
from FlapPyBird_User import flappy_user
from FlapPyBird_User import *

pygame.init()

dh = 400
dw = 800
roomwidth = 2500

# color RGB codes
black = (0,0,0)
white = (255,255,255)
red = (255,0,0)
font = pygame.font.Font('freesansbold.ttf', 50)

gameDisplay = pygame.display.set_mode((dw, dh))
pygame.display.set_caption('flappy')

welcome = pygame.image.load('flappy_welcome.png')
welcomewid = 1000
welcomehi = 80
welcomex = dw/2 - (4*welcomewid/10)
welcomey = 0

userPlay = pygame.image.load('userPlay.png')
userPlaywid = 260
userPlayhi = 85
userPlayx = dw/2 - userPlaywid/2 - userPlaywid
userPlayy = dh/2 + userPlayhi/2

aiLearn = pygame.image.load('ailearn.png')
aiLearnwid = 260#600
aiLearnhi = 85#170
aiLearnx = dw/2 + aiLearnwid/2
aiLearny = dh/2 + aiLearnhi/2

flappyIcon = pygame.image.load('Flappy_Bird_icon.png')
flappyIconwid = 175
flappyIconhi = 175
flappyIconx = dw/2 - (flappyIconwid / 2)
flappyIcony = dh/4

def mouseon(mousepos,thingpos,thingsize):  #([mouse x,mouse y],[thing x,thing y],[thingwid,thinghi]).
    if (mousepos[0] > thingpos[0] and mousepos[0]< thingpos[0] + thingsize[0]) and (mousepos[1] > thingpos[1] and mousepos[1]< thingpos[1] + thingsize[1]):
        return 1
    else:
        return 0

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

        if mouseon(mousepos,[userPlayx,userPlayy],[userPlaywid,userPlayhi]) and mousebuttons[0] == 1:
            return 1
        if mouseon(mousepos,[aiLearnx,aiLearny],[aiLearnwid,aiLearnhi]) and mousebuttons[0] == 1:
            return 2
        gameDisplay.fill(white)
        gameDisplay.blit(welcome, (welcomex, welcomey))
        gameDisplay.blit(userPlay, (userPlayx, userPlayy))
        gameDisplay.blit(aiLearn, (aiLearnx, aiLearny))
        gameDisplay.blit(flappyIcon, (flappyIconx, flappyIcony))
        pygame.display.update()

def userLoop():
    while 1 == 1:
        for event in pygame.event.get():

         if event.type == pygame.QUIT:
            pygame.quit()
            quit()

         if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_q:
                 return -1
         os.chdir("C:/Users/Andrew\Desktop/Queen's/2ndYear/QMIND/Games/neat_flappy/FlapPyBird_User")
         flappy_user.main()

def aiLoop():
    while 1 == 1:
        for event in pygame.event.get():

            if event.type == pygame.QUIT:
                pygame.quit()
                quit()

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_q:
                     return -1
            flappy_ai.main()
                
    

while 1==1:
    directive = mainmenu()
    if directive == 1:
        userLoop()
    if directive == 2:
        aiLoop()

pygame.quit()
quit()
