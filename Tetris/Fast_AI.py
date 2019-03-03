import sys
import Game
import Option
import pygame

class FastPlayer(object):
    def playGame(self):
        game = Game.Game(isRendered=True)
        while game.isAlive():
            allOptions = self.allOptions(game)

            bestOption = self.bestOption(allOptions)

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

    def allOptions(self, game):  # could this just be one big list comprehension?
        allOptions = []
        for oriCurrent in range(game.currentPiece.numOrientations()):
            for posCurrent in range(Game.gridWidth - game.currentPiece.width(oriCurrent) + 1):
                myGame = Game.Game(clone=game)
                myGame.currentPiece.ori = oriCurrent
                myGame.currentPiece.col = posCurrent
                rowAddedAt = myGame.dropPiece()  # this automatically sets up pieces which is kind of wasteful and makes the following line complex
                allOptions.append(Option.Option(myGame.grid, oriCurrent, posCurrent, 0, 0, myGame.numLinesCleared, rowAddedAt))
        return allOptions

    def bestOption(self, options):  # using lines cleared calculated in dropPiece would be more efficient
        # reimplement the filtering efficiently to do one pass procedurally?

        # filter for max lines cleared
        options = [option for option in options if option.numLinesCleared == max([opt.numLinesCleared for opt in options])]

        # filter for smallest height that the first piece was added at
        options = [option for option in options if option.rowAddedAt == min([opt.rowAddedAt for opt in options])]
        # replace height with something like average height of added pieces (or just use the height of the added peice...)

        # get perimeters
        for option in options:
            option.generateStats()
        # filter for smallest perimeter
        options = [option for option in options if option.perimeter == min([opt.perimeter for opt in options])]

        # arbitrarily pick first in remaining options
        return options[0]
