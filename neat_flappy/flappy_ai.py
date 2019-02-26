#QMIND Gaming Team Version
#Contributions by Andrew Simonds

import neat
import os
import sys
from FlapPyBird.flappy import FlappyBirdApp

def eval_genomes(genomes, config):

    # Play game and get results
    idx,genomes = zip(*genomes)

    MyNeatFlappy = FlappyBirdApp(genomes, config)
    MyNeatFlappy.play()
    results = MyNeatFlappy.crash_info
    
    # Calculate fitness and top score
    top_score = 0
    for result, genomes in results:

        score = result['score']
        distance = result['distance']
        energy = result['energy']

        fitness = score*3000 + 0.2*distance - energy*1.5
        genomes.fitness = -1 if fitness == 0 else fitness
        if top_score < score:
            top_score = score

    #print score
    print('The top score was:', top_score)


def run (config_file):
    # Load configuration.
    config = neat.Config(neat.DefaultGenome, neat.DefaultReproduction,
                         neat.DefaultSpeciesSet, neat.DefaultStagnation,
                         config_file)
    
    # Create the population, which is the top-level object for a NEAT run.
    p = neat.Population(config)

    # Add a stdout reporter to show progress in the terminal.
    p.add_reporter(neat.StdOutReporter(False))

    # Run until we achive n.
    winner = p.run(eval_genomes, 50)

def main():
    if len(sys.argv)>1:
        run(int(sys.argv[1]))
    else:
        run()

if __name__ == "__main__":
    # Fix working directory
    local_dir = os.path.dirname(__file__)
    config_path = os.path.join(local_dir, 'config-flappy')
    run(config_path)
