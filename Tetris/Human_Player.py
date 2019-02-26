import Game
import sys
import pygame
import Slow_AI

class HumanPlayer(object):
    def playGame(self):
        game = Game.Game(isRendered=True)
        time = pygame.time.get_ticks()
        delayTime = 250
        while game.isAlive():
            delayTime /= 1.001
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.display.quit()
                    sys.exit()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_LEFT:
                        game.moveLeft()
                    elif event.key == pygame.K_DOWN:
                        game.moveDown()
                    elif event.key == pygame.K_RIGHT:
                        game.moveRight()
                    elif event.key == pygame.K_SPACE:
                        game.rotatePiece()
                    elif event.key == pygame.K_UP:
                        game.dropPiece()
                    elif event.key == pygame.K_TAB:
                        helper = Slow_AI.SimplePlayer()
                        allOptions = helper.allOptions(game)
                        bestOption = helper.bestOption(allOptions)
                        game.currentPiece.ori = bestOption.oriCurrent
                        game.currentPiece.col = bestOption.posCurrent
                        game.dropPiece()
            game.render()
            oldTime = time
            time = pygame.time.get_ticks()
            if int(delayTime) - (time - oldTime) > 0:
                pygame.time.wait(int(delayTime) - (time - oldTime))

            game.moveDown()
            game.render()
            oldTime = time
            time = pygame.time.get_ticks()
            pygame.time.wait(int(delayTime) - (time - oldTime))

        game.render()
        game.screen.blit(Game.font.render("Score: " + str(game.numLinesCleared), True, (0, 0, 255)), (10, 100))
        pygame.display.update()
        keyPressed = False
        while not keyPressed:
            pygame.time.wait(100)
            for event in pygame.event.get():
                keyPressed = event.type
        pygame.display.quit()
        sys.exit()
