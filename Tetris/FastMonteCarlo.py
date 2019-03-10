import sys
import Game
import Option
import pygame
import random

numTestGames = 200
numMoves = 3

class MCTSPlayer(object):
    def playGame(self):
        game = Game.Game(isRendered=True)
        while game.isAlive():
            bestOption = Option.Option(None, 0, 0, None, None, None, None)
            bestNumLinesCleared = 0
            for oriCurrent in range(game.currentPiece.numOrientations()):
                for posCurrent in range(Game.gridWidth - game.currentPiece.width(oriCurrent) + 1):
                    myGame = Game.Game(clone=game)
                    myGame.currentPiece.ori = oriCurrent
                    myGame.currentPiece.col = posCurrent
                    myGame.dropPiece()

                    # Monte Carlo this game state
                    averageNumLinesCleared = 0
                    for i in range(numTestGames):
                        testGame = Game.Game(clone=myGame)
                        for moves in range(numMoves):
                            testGame.currentPiece.ori = random.randint(0, testGame.currentPiece.numOrientations() - 1)
                            testGame.currentPiece.col = random.randint(0, Game.gridWidth - testGame.currentPiece.width(testGame.currentPiece.ori))
                            testGame.dropPiece()
                        averageNumLinesCleared += testGame.numLinesCleared - game.numLinesCleared
                    averageNumLinesCleared /= numTestGames

                    if averageNumLinesCleared > bestNumLinesCleared:
                        bestOption = Option.Option(None, oriCurrent, posCurrent, None, None, None, None)
                        bestNumLinesCleared = averageNumLinesCleared

            game.currentPiece.ori = bestOption.oriCurrent
            game.currentPiece.col = bestOption.posCurrent

            game.dropPiece()

            game.render()
            print("here")
        game.render()
        print("Score: " + str(game.numLinesCleared))
        #game.screen.blit(Game.font.render("Score: " + str(game.numLinesCleared), True, (0, 0, 255)), (10, 100))
        pygame.display.update()
        keyPressed = False
        while not keyPressed:
            pygame.time.wait(100)
            for event in pygame.event.get():
                keyPressed = event.type
        pygame.quit()
        #sys.exit()

MCTSPlayer().playGame()