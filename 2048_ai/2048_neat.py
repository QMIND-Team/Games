import random, pygame, sys
from pygame.locals import *
from random import randint
import copy
import math
import numpy as np
import neat

Population = 300
DeltaDisjoint = 2.0
DeltaWeights = 0.4
DeltaThreshold = 1.0

StaleSpecies = 15

MutateConnectionsChance = 0.25
PerturbChance = 0.90
CrossoverChance = 0.75
LinkMutationChance = 2.0
NodeMutationChance = 0.50
BiasMutationChance = 0.40
StepSize = 0.1
DisableMutationChance = 0.4
EnableMutationChance = 0.2

TimeoutConstant = 20


MaxNodes = 1000000


n_epoch = 7
# defining the window size and other different specifications of the window
LR = 5e-4
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
dictkey = {
    "w": 0,
    "d": 1,
    "a": 2,
    "s": 3}
dictaction = {
    0:"w",
    1:"d",
    2:"a",
    3:"s"}
BGCOLOR = LIGHTORANGE
UP = 'up'
DOWN = 'down'
LEFT = 'left'
RIGHT = 'right'

TABLE = [[0, 0, 0, 0], [0, 0, 0, 0], [0, 0, 0, 0], [0, 0, 0, 0]]

def second_largest(ar):
    #print(ar)
    ind = np.argmax(ar)
    #ar = np.array(ar[0])
    index= 0
    max = 0
    for i in range(4):
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
    for i in range(4):
        if ar[i]>max and i!=i1 and i!=i2:
            max = ar[i]
            index = i
    return index
    #showStartScreen()


def eval_genomes(genomes,config):
    gen_score = 0
    gen_tables = []
    for genome_id,genome in genomes:
        net = neat.nn.RecurrentNetwork.create(genome, config)
        current_max_fitness = 0
        fitness_current = 0
        counter = 0
        scores = []
        good_tables = []
        max_score = 0

        for i in range(20):
            TABLE = init_game()
            done = False
            score = 0
            tables = []
            while not done:
                new_table=TABLE
                act_count=0
                nn_Output = net.activate(np.concatenate(TABLE))
                while new_table==TABLE:
                    desired_key = dictaction[np.array(nn_Output).argmax()]
                    if act_count>10:
                        desired_key = dictaction[second_largest(np.array(nn_Output))]
                    if act_count>20:
                        desired_key = dictaction[third_largest(np.array(nn_Output))]
                    if act_count>30:
                        desired_key = dictaction[random.randrange(0,4)]
                    act_count+=1
                    done,new_table,reward = game_step(desired_key,TABLE)
                    if done:
                        break
                TABLE = randomfill(new_table)
                tables.append(TABLE)
            scores.append(calc_score(TABLE))
            score = calc_score(TABLE)
            if score>max_score:
                max_score=score
                good_tables = []
                for tab in tables:
                    good_tables.append(tab)
            if i==19:
                #top_3 = np.array(scores).argsort()[-3:][::-1]
                #fitness_current = np.mean(np.array([scores[top_3[0]],scores[top_3[1]],scores[top_3[2]]]))
                for a in range(len(scores)):
                    scores[a]+=0.0
                fitness_current = np.max(np.array(scores))
                if fitness_current<500: fitness_current=0
                else: fitness_current-=500
                if fitness_current>current_max_fitness:
                    current_max_fitness = fitness_current
                genome.fitness = fitness_current
                score = calc_score(good_tables[-1])
                if score>=gen_score:
                    gen_score = score
                    gen_tables = []
                    for tab in good_tables:
                        gen_tables.append(tab)
                print("ID: ",genome_id,"fitness: ",genome.fitness)
    for a in gen_tables:
        for _ in pygame.event.get():
            pass
        show(a)


def evolutionary_driver(n=50):
    global FPSCLOCK, screen, BASICFONT
    pygame.init()
    FPSCLOCK = pygame.time.Clock()
    screen = pygame.display.set_mode((WINDOWWIDTH, WINDOWHEIGHT))
    BASICFONT = pygame.font.Font('freesansbold.ttf', 18)
    pygame.display.set_caption('2048')
    config = neat.Config(neat.DefaultGenome, neat.DefaultReproduction,
                         neat.DefaultSpeciesSet, neat.DefaultStagnation,
                         'config')
    p = neat.Population(config)
    p.add_reporter(neat.StdOutReporter(False))
    p.add_reporter(neat.Checkpointer(10))

    p.run(eval_genomes)

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
    z = randint(1, 5)
    if z == 5:
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
def init_game():
    TABLE = [[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0]]
    TABLE = randomfill(TABLE)
    TABLE = randomfill(TABLE)
    return TABLE

def game_step(desired_key,TABLE):
    new_table = key(desired_key, copy.deepcopy(TABLE))
    reward = calc_score(new_table)- calc_score(TABLE)
    if gameOver(new_table):
        return True,new_table,reward
    return False,new_table,reward

def calc_score(TABLE):
    ar = np.concatenate(TABLE)
    a = ar.argsort()[-3:][::-1]
    return ar[a[0]]+ar[a[1]]+ar[a[2]]


def initial_population(initial_games = 100):
    actions = []
    obs = []
    scores = []
    for game in range(initial_games):
        over = False
        TABLE = init_game()
        while(not over):
            action = random.randrange(0,4)
            if action==0:
                desired_key = "w"
            elif action==1:
                desired_key = "d"
            elif action == 2:
                desired_key = "a"
            else:
                desired_key = "s"
            over,new_table,reward = game_step(desired_key,TABLE)
            if new_table!=TABLE:
                a = [0,0,0,0]
                a[action] = 1
                actions.append(a)
                obs.append(np.concatenate(TABLE))
                scores.append(calc_score(TABLE))
                TABLE = randomfill(new_table)
    return obs,actions

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

evolutionary_driver()