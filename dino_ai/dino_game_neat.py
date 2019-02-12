import pygame
import random
import numpy as np
import time
import neat
goal_steps = 1000
pygame.init()
d_width = 600
d_height = 400


black = (0, 0, 0)
white = (255, 255, 255)
red = (255, 0, 0)

#trex = pygame.image.load('trex.png')


class trex(pygame.sprite.Sprite):

    def __init__(self,x_pos,y_pos):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load('trex.png')
        self.x = x_pos
        self.y = y_pos
        self.vel = 0
        self.onGround = True
    def update(self):
        self.y+=self.vel
        if self.onGround==False:
            self.vel+=9.8*dt
class tree_obs(pygame.sprite.Sprite):
    def __init__(self,x,y,speed):
        self.x = x
        self.y = y
        self.vel = speed
        self.image = pygame.image.load('tree.png')
    def update(self):
        self.x+=self.vel

class bird_enemies(pygame.sprite.Sprite):
    def __init__(self,x,y,speed):
        self.x = x
        self.y = y
        self.vel = speed
        self.image = pygame.image.load('bird.png')
    def update(self):
        self.x +=self.vel

class clouds(pygame.sprite.Sprite):
    def __init__(self,x,y,speed):
        self.x = x
        self.y = y
        self.vel = speed
        self.image = pygame.image.load('cloud.png')
    def update(self):
        self.x+=self.vel

class ground(pygame.sprite.Sprite):
    def __init__(self,x,y,speed):
        self.x = x
        self.y = y
        self.vel = speed
        self.image = pygame.image.load('ground.png')
    def update(self):
        self.x+=self.vel


def game_step(crashed):
    for event in pygame.event.get():
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP and dino.onGround == True:
                dino.onGround = False
                dino.vel = -15
            if event.key == pygame.K_DOWN and dino.onGround==True:
                dino.image = pygame.image.load('down_t-rex.png')
        if event.type == pygame.KEYUP:
            dino.image = pygame.image.load('trex.png')
        if event.type == pygame.MOUSEBUTTONUP:
            crashed = True
    return crashed
def ai_game_step(action,trees,trees2,bird,bird2,g_disp,cloud):
    if (dino.y >= d_height * .82 and not dino.onGround):
        dino.onGround=True
        dino.vel=0
        dino.y = d_height*.82
    if action==1 and dino.onGround==True:
        dino.onGround = False
        dino.vel = -15

    dino.update()
    bird.update()
    bird2.update()
    for tree in trees:
        tree.update()
    for tree in trees2:
        tree.update()
    for i in cloud:
        i.update()

    return game_over(trees,trees2,bird,bird2,g_disp)


def game_over(trees,trees2,bird,bird2,g_disp):
    if trees[0].y!=10000:
        for i in range(len(trees)):
            if dino.x - trees[i].x >= -40 and dino.x - trees[i].x <= 20 and abs(dino.y - trees[i].y) <= 20:
                #print(dino.x-trees[0].x)
                return True
    if trees2[0].y!=10000:
        for i in range(len(trees)):
            if dino.x - trees2[i].x >= -40 and dino.x - trees2[i].x <= 20 and abs(dino.y - trees2[i].y) <= 20:
                #print(dino.x - trees2[0].x)
                return True
    if bird.y!=10000:
        if abs(dino.x+50-bird.x-375)<=35 and abs(dino.y+30-bird.y-60)<=35:
            return True
    if bird2.y!=10000:
        if abs(dino.x+50-bird2.x-375)<=35 and abs(dino.y+30-bird2.y-60)<=35:
            return True
    return False




dt = 0.1
x = d_width*.1
y = d_height*.82
dino = trex(x,y)

#trees = [tree_obs(x=10000,y=10000,speed=0),tree_obs(x=10000,y=10000,speed=0),tree_obs(x=10000,y=10000,speed=0)]


new_obs = True
time_i = 0




def init_trees():
    trees = [tree_obs(10000,10000,0),tree_obs(10000,10000,0),tree_obs(10000,10000,0)]
    return trees
def init_clouds():
    cloud = [clouds(10000,10000,-6),clouds(10000,10000,-6)]
    for i in range(2):
        cloud[i] = clouds(d_width * (1 + 0.7 * i), d_height * .15, -6)
    return cloud
def init_bird():
    bird = bird_enemies(10000,10000,-6)
    return bird

dictobject = {
    0: "tree",
    1: "bird"}
dictheight = {
    0: 210,
    1: 250,
    2: 300
}

def eval_genomes(genomes,config):
    g_disp = pygame.display.set_mode((d_width, d_height))
    g_disp.fill(white)
    clock = pygame.time.Clock()
    trees = init_trees()
    trees2 = init_trees()
    bird = init_bird()
    bird2 = init_bird()
    for genome_id,genome in genomes:
        time_c=0
        mult=80
        speed = -6
        net = neat.nn.RecurrentNetwork.create(genome, config)
        current_max_fitness = 0
        fitness_current = 0
        done = False
        tree_count = 0
        bird_count = 0
        cloud = init_clouds()
        floor = ground(0, d_height * .9, speed)
        floor2 = ground(10000, 10000, speed)
        while not done:
            time_c+=1
            pygame.display.update()
            if fitness_current%mult==0:
                obj_type = dictobject[0]
                if fitness_current>=300:
                    obj_type = dictobject[random.randrange(0,2)]
                if obj_type=="tree":
                    if tree_count==2:
                        tree_count=0
                    num_objs = random.randrange(2, 4)
                    if tree_count==0:
                        for i in range(num_objs):
                            trees[i] = tree_obs(d_width * (1 + .03 * i), d_height * .82, speed)
                    else:
                        for i in range(num_objs):
                            trees2[i] = tree_obs(d_width * (1 + .03 * i), d_height * .82, speed)
                    tree_count += 1

                elif obj_type=="bird":
                    if bird_count==2:
                        bird_count=0
                    height = dictheight[random.randrange(0,3)]
                    if bird_count == 0:
                        bird = bird_enemies(d_width*.5,height,speed)
                    elif bird_count ==1:
                        bird2 = bird_enemies(d_width*.5,height,speed)
                    bird_count+=1
            #print(bird_count,tree_count)

            g_disp.fill((0, 255, 255))

            g_disp.blit(bird.image,(bird.x,bird.y))

            g_disp.blit(bird2.image,(bird2.x,bird2.y))
            g_disp.blit(dino.image, (dino.x, dino.y))


            for i in range(len(trees)):
                g_disp.blit(trees[i].image, (trees[i].x, trees[i].y))
            for i in range(len(trees2)):
                g_disp.blit(trees2[i].image, (trees2[i].x, trees2[i].y))
            for i in range(2):
                g_disp.blit(cloud[i].image, (cloud[i].x, cloud[i].y))

            g_disp.blit(floor.image,(floor.x,floor.y))
            g_disp.blit(floor2.image,(floor2.x,floor2.y))

            for _ in pygame.event.get():
                pass
            useB2 = False
            useB1 = False
            useT1 = False
            useT2 = False


            if bird2.y!=10000 and bird2.x+295-dino.x>=-20:
                useB2=True
            if bird.y!=10000 and bird.x+295-dino.x>=-20:
                useB1=True
            if trees[0].y!=10000 and trees[0].x-dino.x-30>=-20:
                useT1 = True
            if trees2[0].y!=10000 and trees2[0].x-dino.x-30>=-20:
                useT2 = True
            action = 0





            if useT1 and not useT2 and not useB1 and not useB2:
                action = np.argmax(net.activate([trees[0].x-dino.x-30, 0]))
            if useT2 and not useT1 and not useB1 and not useB2:
                action = np.argmax(net.activate([trees2[0].x-dino.x-30, 0]))
            if useB1 and not useT1 and not useT2 and not useB2:
                action = np.argmax(net.activate([bird.x+295-dino.x, dino.y-bird.y-30]))
            if useB2 and not useT1 and not useT2 and not useB1:
                action = np.argmax(net.activate([bird2.x+295-dino.x, dino.y-bird2.y-30]))

            if useT1 and useT2:
                if trees[0].x<=trees[1].x:
                    action = np.argmax(net.activate([trees[0].x-dino.x-30,0]))
                else:
                    action = np.argmax(net.activate([trees2[0].x-dino.x-30, 0]))
            elif useT1 and useB1:
                if trees[0].x<=bird.x+340:
                    action = np.argmax(net.activate([trees[0].x-dino.x-30,0]))
                else:
                    action = np.argmax(net.activate([bird.x+295-dino.x, dino.y - bird.y-30]))
            elif useT1 and useB2:
                if trees[0].x<=bird2.x+340:
                    action = np.argmax(net.activate([trees[0].x-dino.x-30,0]))
                else:
                    action = np.argmax(net.activate([bird2.x+295-dino.x, dino.y - bird2.y-30]))
            elif useT2 and useB1:
                if trees2[0].x<=bird.x+340:
                    action = np.argmax(net.activate([trees2[0].x-dino.x-30,0]))
                else:
                    action = np.argmax(net.activate([bird.x+295-dino.x, dino.y - bird.y-30]))
            elif useT2 and useB2:
                if trees2[0].x<=bird2.x+340:
                    action = np.argmax(net.activate([trees2[0].x-dino.x-30,0]))
                else:
                    action = np.argmax(net.activate([bird2.x+295-dino.x, dino.y - bird2.y-30]))
            elif useB1 and useB2:
                if bird.x<=bird2.x:
                    action = np.argmax(net.activate([bird.x+295-dino.x,dino.y-bird.y-30]))
                else:
                    action = np.argmax(net.activate([bird2.x+295-dino.x, dino.y - bird2.y-30]))




            #clock.tick(120)
            if floor.y!=10000:
                floor.update()
                if floor.x<=-650:
                    floor.__init__(10000,10000,speed)
                    floor2.__init__(0,d_height*.9,speed)
            if floor2.y!=10000:
                floor2.update()
                if floor2.x<=-650:
                    floor2.__init__(10000,10000,speed)
                    floor.__init__(0,d_height*.9,speed)
            #print("Tree ",i,": (",trees[i].x,",",trees[i].y,")")
            done = ai_game_step(action,trees=trees,trees2=trees2,bird=bird,bird2=bird2,g_disp=g_disp,cloud=cloud)

            fitness_current+=1
            if bird.x<=-500:
                bird = init_bird()
            if trees[len(trees)-1].x<=0:
                trees = init_trees()
            if bird2.x<=-500:
                bird2 = init_bird()
            for i in range(len(cloud)):
                if cloud[i].x<=-100:
                    cloud[i].__init__(d_width*1.1,d_height*0.15,speed)
            if trees2[len(trees)-1].x<=0:
                trees2 = init_trees()
            if time_c>500:
                time_c=0
                speed-=1
                mult-=3
                if trees[0].y!=10000:
                    for i in range(len(trees)):
                        trees[i].vel-=1
                if trees2[0].y!=10000:
                    for i in range(len(trees2)):
                        trees2[i].vel-=1
                if bird.y!=10000:
                    bird.vel-=1
                if bird2.y!=10000:
                    bird2.vel-=1
                for i in cloud:
                    i.vel-=1
            #if (fitness_current>=500):
            #    speed-=1
            #print(dino.x,dino.y)
        fitness_current-=80
        if fitness_current>current_max_fitness:
            current_max_fitness = fitness_current
        genome.fitness = fitness_current
        time.sleep(0.2)

        dino.y = d_height*.82
        trees = init_trees()
        bird = init_bird()
        bird2 = init_bird()
        trees2 = init_trees()
        print("ID: ",genome_id,"fitness: ",genome.fitness)


def evolutionary_driver():
    config = neat.Config(neat.DefaultGenome, neat.DefaultReproduction,
                         neat.DefaultSpeciesSet, neat.DefaultStagnation,
                         'config_dino')
    p = neat.Population(config)
    p.add_reporter(neat.StdOutReporter(False))
    p.add_reporter(neat.Checkpointer(10))
    p.run(eval_genomes)

evolutionary_driver()