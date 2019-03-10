import pygame, sys
from pygame.locals import *
from random import randint
import copy
import math
import numpy as np

# defining the window size and other different specifications of the window
FPS = 5
WINDOWWIDTH = 640
WINDOWHEIGHT = 640
boxsize = min(WINDOWWIDTH, WINDOWHEIGHT) // 4
margin = 5
thickness = 0
# defining the RGB for various colours used
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
DARKGREEN = (0, 155, 0)
DARKGRAY = (40, 40, 40)
LIGHTSALMON = (255, 160, 122)
ORANGE = (221, 118, 7)
LIGHTORANGE = (227, 155, 78)
CORAL = (255, 127, 80)
BLUE = (0, 0, 255)
LIGHTBLUE = (0, 0, 150)
colorback = (189, 174, 158)
colorblank = (205, 193, 180)
colorlight = (249, 246, 242)
colordark = (119, 110, 101)

fontSize = [100, 85, 70, 55, 40]

dictcolor1 = {
    0: colorblank,
    2: (238, 228, 218),
    4: (237, 224, 200),
    8: (242, 177, 121),
    16: (245, 149, 99),
    32: (246, 124, 95),
    64: (246, 95, 59),
    128: (237, 207, 114),
    256: (237, 204, 97),
    512: (237, 200, 80),
    1024: (237, 197, 63),
    2048: (237, 194, 46),
    4096: (237, 190, 30),
    8192: (239, 180, 25)}

dictcolor2 = {
    2: colordark,
    4: colordark,
    8: colorlight,
    16: colorlight,
    32: colorlight,
    64: colorlight,
    128: colorlight,
    256: colorlight,
    512: colorlight,
    1024: colorlight,
    2048: colorlight,
    4096: colorlight,
    8192: colorlight}
BGCOLOR = LIGHTORANGE
UP = 'up'
DOWN = 'down'
LEFT = 'left'
RIGHT = 'right'

TABLE = [[0, 0, 0, 0], [0, 0, 0, 0], [0, 0, 0, 0], [0, 0, 0, 0]]

global FPSCLOCK, screen, BASICFONT
pygame.init()
FPSCLOCK = pygame.time.Clock()
screen = pygame.display.set_mode((WINDOWWIDTH, WINDOWHEIGHT))
BASICFONT = pygame.font.Font('freesansbold.ttf', 18)
pygame.display.set_caption('2048')

def second_largest(ar):
    ind = np.argmax(ar)
    #ar = np.array(ar[0])
    index= 0
    max = 0
    for i in range(len(ar)):
        if ar[i]>max and i!=ind:
            max = ar[i]
            index = i
    return index
def third_largest(ar):
    i1 = np.argmax(ar)
    i2 = second_largest(ar)
    #ar = np.array(ar[0])
    index = 0
    max = 0
    for i in range(len(ar)):
        if ar[i]>max and i!=i1 and i!=i2:
            max = ar[i]
            index = i
    return index

def fill_num(TABLE,num):
    flatTABLE = sum(TABLE, [])
    if 0 not in flatTABLE:
        return TABLE
    empty = False
    w = 0
    while not empty:
        w = randint(0, 15)
        if TABLE[w // 4][w % 4] == 0:
            empty = True
        TABLE[w // 4][w % 4] = num
    return TABLE
def randomfill(TABLE):
    # search for zero in the game table and randomly fill the places
    flatTABLE = sum(TABLE, [])
    if 0 not in flatTABLE:
        return TABLE
    empty = False
    w = 0
    while not empty:
        w = randint(0, 15)
        if TABLE[w // 4][w % 4] == 0:
            empty = True
    z = randint(1, 10)
    if z == 10:
        TABLE[w // 4][w % 4] = 4
    else:
        TABLE[w // 4][w % 4] = 2
    return TABLE


def gameOver(TABLE):
    # returns False if a box is empty or two boxes can be merged
    x = [-1, 0, 1, 0]
    y = [0, 1, 0, -1]
    for pi in range(4):
        for pj in range(4):
            if TABLE[pi][pj] == 0:
                return False
            for point in range(4):
                if pi + x[point] > -1 and pi + x[point] < 4 and pj + y[point] > -1 and pj + y[point] < 4 and TABLE[pi][
                    pj] == TABLE[pi + x[point]][pj + y[point]]:
                    return False
    return True




def showMainMenu():
    # to display main menu
    pressKeySurf = BASICFONT.render('Press a key for main menu', True, WHITE)
    pressKeyRect = pressKeySurf.get_rect()
    pressKeyRect.topleft = (WINDOWWIDTH - 250, WINDOWHEIGHT - 30)
    screen.blit(pressKeySurf, pressKeyRect)


def checkForKeyPress():
    # checking if a key is pressed or not
    if len(pygame.event.get(QUIT)) > 0:
        terminate()

    keyUpEvents = pygame.event.get(KEYUP)
    if len(keyUpEvents) == 0:
        return None
    if keyUpEvents[0].key == K_ESCAPE:
        terminate()
    return keyUpEvents[0].key


def show(TABLE):
    # showing the table
    screen.fill(colorback)
    myfont = pygame.font.SysFont("Arial", 60, bold=True)
    for i in range(4):
        for j in range(4):
            pygame.draw.rect(screen, dictcolor1[TABLE[i][j]], (j * boxsize + margin,
                                                               i * boxsize + margin,
                                                               boxsize - 2 * margin,
                                                               boxsize - 2 * margin),
                             thickness)
            if TABLE[i][j] != 0:
                order = int(math.log10(TABLE[i][j]))
                myfont = pygame.font.SysFont("Arial", fontSize[order], bold=True)
                label = myfont.render("%4s" % (TABLE[i][j]), 1, dictcolor2[TABLE[i][j]])
                screen.blit(label, (j * boxsize + 2 * margin, i * boxsize + 9 * margin))

    pygame.display.update()

def key(DIRECTION, TABLE):
    if DIRECTION == 'w':
        for pi in range(1, 4):
            for pj in range(4):
                if TABLE[pi][pj] != 0: TABLE = moveup(pi, pj, TABLE)
    elif DIRECTION == 's':
        for pi in range(2, -1, -1):
            for pj in range(4):
                if TABLE[pi][pj] != 0: TABLE = movedown(pi, pj, TABLE)
    elif DIRECTION == 'a':
        for pj in range(1, 4):
            for pi in range(4):
                if TABLE[pi][pj] != 0: TABLE = moveleft(pi, pj, TABLE)
    elif DIRECTION == 'd':
        for pj in range(2, -1, -1):
            for pi in range(4):
                if TABLE[pi][pj] != 0: TABLE = moveright(pi, pj, TABLE)
    return TABLE


def movedown(pi, pj, T):
    justcomb = False
    while pi < 3 and (T[pi + 1][pj] == 0 or (T[pi + 1][pj] == T[pi][pj] and not justcomb)):
        if T[pi + 1][pj] == 0:
            T[pi + 1][pj] = T[pi][pj]
        elif T[pi + 1][pj] == T[pi][pj]:
            T[pi + 1][pj] += T[pi][pj]
            justcomb = True
        T[pi][pj] = 0
        pi += 1
    return T


def moveleft(pi, pj, T):
    justcomb = False
    while pj > 0 and (T[pi][pj - 1] == 0 or (T[pi][pj - 1] == T[pi][pj] and not justcomb)):
        if T[pi][pj - 1] == 0:
            T[pi][pj - 1] = T[pi][pj]
        elif T[pi][pj - 1] == T[pi][pj]:
            T[pi][pj - 1] += T[pi][pj]
            justcomb = True
        T[pi][pj] = 0
        pj -= 1
    return T


def moveright(pi, pj, T):
    justcomb = False
    while pj < 3 and (T[pi][pj + 1] == 0 or (T[pi][pj + 1] == T[pi][pj] and not justcomb)):
        if T[pi][pj + 1] == 0:
            T[pi][pj + 1] = T[pi][pj]
        elif T[pi][pj + 1] == T[pi][pj]:
            T[pi][pj + 1] += T[pi][pj]
            justcomb = True
        T[pi][pj] = 0
        pj += 1
    return T


def moveup(pi, pj, T):
    justcomb = False
    while pi > 0 and (T[pi - 1][pj] == 0 or (T[pi - 1][pj] == T[pi][pj] and not justcomb)):
        if T[pi - 1][pj] == 0:
            T[pi - 1][pj] = T[pi][pj]
        elif T[pi - 1][pj] == T[pi][pj]:
            T[pi - 1][pj] += T[pi][pj]
            justcomb = True
        T[pi][pj] = 0
        pi -= 1
    return T


def leaderboard():
    s = 'to show leaderboard'


def terminate():
    pygame.quit()
    sys.exit()



def init_game():
    TABLE = [[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0]]
    TABLE = randomfill(TABLE)
    TABLE = randomfill(TABLE)
    return TABLE
dictaction = {
    0:"w",
    1:"d",
    2:"a",
    3:"s"}


def adjacent(TABLE):
    adjtiles = []
    for i in range(4):
        for j in range(4):
            if (j<3):
                if TABLE[i][j]==TABLE[i][j+1]!=0:
                    if  [(i,j+1),(i,j)] not in adjtiles:
                        adjtiles.append([(i, j), (i,j+1)])
            if (i<3):
                if TABLE[i][j]==TABLE[i+1][j]!=0:
                    if [(i+1,j), (i, j)] not in adjtiles:
                        adjtiles.append([(i, j), (i+1, j)])
            if j!=0:
                if TABLE[i][j] == TABLE[i][j-1]!=0:
                    if [(i,j-1), (i,j)] not in adjtiles:
                        adjtiles.append([(i,j),(i,j-1)])
            if i!=0:
                if TABLE[i][j] == TABLE[i-1][j]!=0:
                    if [(i-1,j), (i,j)] not in adjtiles:
                        adjtiles.append([(i,j),(i-1,j)])
    return adjtiles


def state_score(TABLE):
    W1 = [[6,5,4,3],[5,4,3,2],[4,3,2,1],[3,2,1,0]]
    W2 = np.rot90(W1,-1)
    #W2 = np.rot90(np.array(W1))
    #W3 = np.rot90(W2)
    #W4 = np.rot90(W3)
    a = TABLE
    penalty = 0
    score1 = 0
    for i in range(4):
        for j in range(4):
            score1+=W1[i][j]*a[i][j]
            score1+=W2[i][j]*a[i][j]
    for i in range(4):
        for j in range(4):
            if a[i][j]!=0:
                if i != 0:
                    penalty += abs(a[i][j] - a[i - 1][j])
                if j != 0:
                    penalty += abs(a[i][j] - a[i][j - 1])
                if i != 3:
                    penalty += abs(a[i][j] - a[i + 1][j])
                if j != 3:
                    penalty += abs(a[i][j] - a[i][j + 1])
    return score1-penalty

def move(TABLE,action):
    new_table = key(dictaction[action],copy.deepcopy(TABLE))
    return new_table
def possible_fills(TABLE):
    lin_tab = np.concatenate(TABLE)
    indices = [i for i, x in enumerate(lin_tab) if x == 0]
    p = []
    tabs = []

    for i in indices:
        lin_tab[i]=2
        tabs.append(np.array(lin_tab).reshape(4,4).tolist())
        p.append(0.9)
        lin_tab[i] = 4
        tabs.append(np.array(lin_tab).reshape(4, 4).tolist())
        p.append(0.1)
    return tabs,p,len(indices)

def score(TABLE,depth,tables,state):
    if depth==0:
        return state_score(TABLE)
    elif state=="board":
        tabs,probs,n = possible_fills(TABLE)
        s = 0
        for i in range(len(tabs)):
            s+=probs[i]*score(tabs[i],depth-1,tables,"player")
        return s/n
    elif state=="player":
        scores = [0,0,0,0]
        for d in range(3):
            new_table = move(TABLE,d)
            if new_table!=TABLE:# and new_table not in tables:

                tables.append(new_table)
                scores[d] = score(new_table,depth-1,tables,"board")
        return np.max(scores)

def get_action_2(TABLE,depth):
    scores = []
    for d in range(3):
        new_table = key(dictaction[d],copy.deepcopy(TABLE))
        if new_table==TABLE:
            scores.append(-1)
        else:
            scores.append(score(move(TABLE, d), depth, [],"board"))
    action = np.argmax(scores)
    return action



def options_menu(ai_play,user_play,deep):
    keep_going = False
    screen.fill(colorback)
    screen.blit(pygame.transform.scale(pygame.image.load("quick_AI.png"),(300,100)), (150,260))
    screen.blit(pygame.transform.scale(pygame.image.load("deep_AI.png"),(300,100)), (150,400))
    screen.blit(pygame.transform.scale(pygame.image.load("userplay.png"),(300,100)), (150,120))

    pygame.display.update()

    for event in pygame.event.get():
        if event.type==pygame.MOUSEBUTTONUP:
            if pygame.mouse.get_pos()[0]>=150 and pygame.mouse.get_pos()[0]<=450 and pygame.mouse.get_pos()[1]>=120 and pygame.mouse.get_pos()[1]<=220:
                user_play = True
                keep_going = True
                ai_play = False
                deep=False
            elif pygame.mouse.get_pos()[0]>=150 and pygame.mouse.get_pos()[0]<=450 and pygame.mouse.get_pos()[1]>=260 and pygame.mouse.get_pos()[1]<=360:
                ai_play = True
                keep_going = True
                user_play = False
                deep=False
            elif pygame.mouse.get_pos()[0]>=150 and pygame.mouse.get_pos()[0]<=450 and pygame.mouse.get_pos()[1]>=400 and pygame.mouse.get_pos()[1]<=500:
                deep=True
                ai_play = True
                keep_going = True
                user_play = False
        if event.type==pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                keep_going=True
                break
    return ai_play,user_play,keep_going,deep

ai_play = False
user_play = False
while not ai_play and not user_play:
    ai_play,user_play,keep_going,deep = options_menu(False,False,False)
TABLE = init_game()
done = False
while not done:
    keep_going = True
    show(TABLE)
    if gameOver(TABLE):
        show(TABLE)
        while True:
            for event in pygame.event.get():
                if event.type == pygame.MOUSEBUTTONUP:
                    done = True
                    break
            if done:
                break
    if ai_play:
        show(TABLE)
        num_zeroes = len([x for x in np.concatenate(TABLE) if x ==0])
        if not deep:
            if np.max(TABLE)<1024 and num_zeroes>7:
                action= get_action_2(copy.deepcopy(TABLE),depth=3)
            else:
                action = get_action_2(copy.deepcopy(TABLE),depth=4)
        else:
            if num_zeroes >7 and np.max(TABLE)<1024:
                action = get_action_2(copy.deepcopy(TABLE), depth=4)
            elif num_zeroes > 5:
                action = get_action_2(copy.deepcopy(TABLE), depth=5)
            else:
                action = get_action_2(copy.deepcopy(TABLE), depth=6)
        new_table = key(dictaction[action], copy.deepcopy(TABLE))
        if new_table == TABLE:
            action = 3
            new_table = key(dictaction[action], copy.deepcopy(TABLE))
        TABLE=randomfill(new_table)
    elif user_play:
        action = ""
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    action = "w"
                if event.key == pygame.K_RIGHT:
                    action = "d"
                if event.key == pygame.K_LEFT:
                    action = "a"
                if event.key == pygame.K_DOWN:
                    action = "s"
                if event.key == pygame.K_SPACE:
                    keep_going = False

        if action != "":
            new_table = key(action, copy.deepcopy(TABLE))
            if new_table!=TABLE:
                TABLE = randomfill(new_table)
    for event in pygame.event.get():
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                keep_going = False

    while not keep_going:
        ai_play, user_play,keep_going,deep = options_menu(ai_play,user_play,deep)