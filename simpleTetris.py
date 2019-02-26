import copy
import random
import pygame
import sys
from enum import Enum


class BitMaps(Enum):
    I = [[[True], [True], [True], [True]], [[True, True, True, True]]]
    O = [[[True, True], [True, True]]]
    T = [[[False, True, False], [True, True, True]], [[False, True], [True, True], [False, True]], [[True, True, True], [False, True, False]], [[True, False], [True, True], [True, False]]]
    S = [[[True, False], [True, True], [False, True]], [[True, True, False], [False, True, True]]]
    Z = [[[True, False], [True, True], [False, True]], [[False, True, True], [True, True, False]]]
    J = [[[True, True], [False, True], [False, True]], [[True, True, True], [True, False, False]], [[True, False], [True, False], [True, True]], [[False, False, True], [True, True, True]]]
    L = [[[True, True], [True, False], [True, False]], [[True, False, False], [True, True, True]], [[False, True], [False, True], [True, True]], [[True, True, True], [False, False, True]]]


intToBitMaps = [BitMaps.I, BitMaps.O, BitMaps.T, BitMaps.S, BitMaps.Z, BitMaps.Z, BitMaps.J, BitMaps.L]

black = (0, 0, 0)
white = (255, 255, 255)
pygame.font.init()
font = pygame.font.Font(None, 36)

gridWidth = 10
gridHeight = 40
squareLength = 10  # pixels


class Piece(object):
    def __init__(self, bitMaps):
        self.bitMaps = bitMaps  # rename to something like "type" or "Tetrominoe"
        self.ori = 0
        self.col = 3
        self.row = 36

    def getBitMap(self, ori=None):
        if ori is None:
            ori = self.ori
        return self.bitMaps.value[ori]

    def width(self, ori=None):
        if ori is not None:
            return len(self.bitMaps.value[ori][0])
        else:
            return len(self.getBitMap()[0])

    def height(self, ori=None):
        if ori is not None:
            return len(self.getBitMap(ori=ori))
        else:
            return len(self.getBitMap())

    def numOrientations(self):
        return len(self.bitMaps.value)


class Option(object):  # what is this doing and should I add getPerimeter() etc here
    def __init__(self, grid, oriCurrent, posCurrent, oriNext, posNext, numLinesCleared, rowAddedAt):
        self.grid = grid
        self.oriCurrent = oriCurrent
        self.posCurrent = posCurrent
        self.oriNext = oriNext
        self.posNext = posNext
        self.numFilled = None
        self.perimeter = None
        self.height = None
        self.numLinesCleared = numLinesCleared  # total lines cleared
        self.rowAddedAt = rowAddedAt

    def generateStats(self):
        self.numFilled = 0
        self.perimeter = 0  # should perimeter include the walls? (I am not going to currently...)
        for row in range(gridHeight):
            isEmpty = True
            for col in range(gridWidth):
                if self.grid[row][col]:
                    self.numFilled += 1
                    isEmpty = False

                    if col > 0 and not self.grid[row][col - 1]:
                        self.perimeter += 1
                    if row < gridHeight - 1 and not self.grid[row + 1][col]:
                        self.perimeter += 1
                    if col < gridWidth - 1 and not self.grid[row][col + 1]:
                        self.perimeter += 1
                    if row > 0 and not self.grid[row - 1][col]:
                        self.perimeter += 1
            if isEmpty:
                self.height = row
                return #(self.numFilled, self.perimeter, self.height)


class Game(object): # should be able to do everything that you can do in the game
    def __init__(self, isRendered = False, clone=None):
        if clone is not None:
            self.isRendered = clone.isRendered
            self.grid = copy.deepcopy(clone.grid)
            self.currentPiece = copy.deepcopy(clone.currentPiece)
            self.nextPiece = copy.deepcopy(clone.nextPiece)
            self.numLinesCleared = clone.numLinesCleared
            return

        self.isRendered = isRendered
        self.grid = [[False for i in range(gridWidth)] for j in range(gridHeight)]  # [0][0] is bottom-left corner, index row, then col ([x][y] on caresian plane)
        self.currentPiece = Piece(intToBitMaps[random.randint(0, 6)])  # there are 7 pieces to choose from
        self.nextPiece = Piece(intToBitMaps[random.randint(0, 6)])
        self.numLinesCleared = 0  # fitness function

        if self.isRendered:
            # set up a pygame window for this game
            pygame.init()
            self.screen = pygame.display.set_mode((2 + gridWidth * (squareLength+1), 2 + gridHeight * (squareLength+1)))
            self.screen.fill(white)
            pygame.display.update()

    def _notOverlapping(self, pieceRow=None, pieceCol=None, pieceOri=None):
        if pieceRow is None:
            pieceRow = self.currentPiece.row
        if pieceCol is None:
            pieceCol = self.currentPiece.col
        if pieceOri is None:
            pieceOri = self.currentPiece.ori
        if pieceCol < 0 or pieceCol + self.currentPiece.width() > gridWidth or pieceRow < 0 or pieceRow + self.currentPiece.height() > gridHeight:
            return False
        for row in range(self.currentPiece.height()):
            for col in range(self.currentPiece.width()):
                if self.grid[pieceRow + row][pieceCol + col] and self.currentPiece.getBitMap(ori=pieceOri)[row][col]:
                    return False
        return True

    def rotatePiece(self):
        newOri = (self.currentPiece.ori + 1) % self.currentPiece.numOrientations()
        if self._notOverlapping(pieceOri=newOri):
            self.currentPiece.ori = newOri

    def moveLeft(self):
        if self._notOverlapping(pieceCol=self.currentPiece.col-1):
            self.currentPiece.col -= 1

    def moveDown(self):
        # check that there is space
        if self._notOverlapping(pieceRow=self.currentPiece.row-1):
            self.currentPiece.row -= 1
        else:
            self.dropPiece()

    def moveRight(self):
        if self._notOverlapping(pieceCol=self.currentPiece.col+1):
            self.currentPiece.col += 1

    def isAlive(self):
        # we die if any of the top 4 rows aren't empty
        for row in range(gridHeight - 4, gridHeight):
            for col in range(gridWidth):
                if self.grid[row][col]:
                    return False
        return True

    def dropPiece(self):
        # move piece down the grid
        while self._notOverlapping(pieceRow=self.currentPiece.row-1):
            self.currentPiece.row -= 1

        # add piece to the grid
        for row in range(self.currentPiece.height()):
            for col in range(self.currentPiece.width()):
                if self.currentPiece.getBitMap()[row][col]:
                    if self.grid[self.currentPiece.row + row][self.currentPiece.col + col]:
                        print("the bitmap is overlapping on to filled squares")
                    self.grid[self.currentPiece.row + row][self.currentPiece.col + col] = True
        rowAddedAt = self.currentPiece.row

        # take out any complete rows
        for row in range(self.currentPiece.row + self.currentPiece.height() - 1, self.currentPiece.row - 1, -1):  # reversed so that the indexes don't need to be adjusted for shifting the values of the grid
            isComplete = True
            for col in range(10):
                if not self.grid[row][col]:
                    isComplete = False  # continue to for row?  # move on to the next row
                    break
            if isComplete:
                # remove row
                for myRow in range(row, gridHeight - 1):
                    for myCol in range(gridWidth):
                        self.grid[myRow][myCol] = self.grid[myRow + 1][myCol]
                for myCol in range(gridWidth):
                    self.grid[gridHeight-1][myCol] = False  # do last row separately
                self.numLinesCleared += 1

        # load new piece
        self.currentPiece = self.nextPiece
        self.nextPiece = Piece(intToBitMaps[random.randint(0, 6)]) # there are 7 pieces
        # ^ It would be more efficient to just transfer the data from nextPiece to currentPiece and wipe nextPiece

        return rowAddedAt

    def render(self):
        if not self.isRendered:
            return None

        self.screen.fill(white)
        numFilledSquares = 0
        for row in range(gridHeight):
            for col in range(gridWidth):
                if self.grid[row][col]:
                    pygame.draw.rect(self.screen, black, pygame.Rect(1 + col * (squareLength+1), 1 + (gridHeight - row) * (squareLength+1), squareLength, squareLength), 0) # + squareLength is sketch
                    numFilledSquares += 1
        print("numFilled Squares in the grid:", numFilledSquares)
        '''
        # draw the current piece in the top left corner
        for row in range(self.currentPiece.height()):
            for col in range(self.currentPiece.width()):
                if self.currentPiece.getBitMap()[row][col]:
                    pygame.draw.rect(self.screen, black, pygame.Rect(1 + col * (squareLength+1), 1 + (4 - row) * (squareLength+1), squareLength, squareLength), 0)
        '''

        # draw current piece where it is on the grid
        for row in range(self.currentPiece.height()):
            for col in range(self.currentPiece.width()):
                if self.currentPiece.getBitMap()[row][col]:
                    pygame.draw.rect(self.screen, black, pygame.Rect(1 + (self.currentPiece.col + col) * (squareLength+1), 1 + (gridHeight - (self.currentPiece.row + row)) * (squareLength+1), squareLength, squareLength), 0)

        # draw the next piece in the top right corner
        for row in range(self.nextPiece.height()):
            for col in range(self.nextPiece.width()):
                if self.nextPiece.getBitMap()[row][col]:
                    pygame.draw.rect(self.screen, black, pygame.Rect(1 + (col+5) * (squareLength+1), 1 + (4 - row) * (squareLength+1), squareLength, squareLength), 0)

        pygame.display.update()

        # will this flush my key events?
        pygame.event.pump()  # to tell the operating system that pygame is still running


class HumanPlayer(object):
    def playGame(self):
        game = Game(isRendered=True)
        time = pygame.time.get_ticks()
        delayTime = 250
        while game.isAlive():
            delayTime /= 1.001
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.display.quit()
                    #sys.exit()
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
                        helper = SimplePlayer()
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
        game.screen.blit(font.render("Score: " + str(game.numLinesCleared), True, (0, 0, 255)), (10, 100))
        pygame.display.update()
        keyPressed = False
        while not keyPressed:
            pygame.time.wait(100)
            for event in pygame.event.get():
                keyPressed = event.type
        pygame.display.quit()
        #sys.exit()


class SimplePlayer(object):
    def playGame(self):
        game = Game(isRendered=True)
        while game.isAlive():
            allOptions = self.allOptions(game)

            bestOption = self.bestOption(allOptions)

            game.currentPiece.ori = bestOption.oriCurrent
            game.currentPiece.col = bestOption.posCurrent

            game.dropPiece()

            game.render()
            print("here")
        game.render()
        game.screen.blit(font.render("Score: " + str(game.numLinesCleared), True, (0, 0, 255)), (10, 100))
        pygame.display.update()
        keyPressed = False
        while not keyPressed:
            pygame.time.wait(100)
            for event in pygame.event.get():
                keyPressed = event.type
        pygame.display.quit()
        #sys.exit()

    def allOptions(self, game):  # could this just be one big list comprehension?
        allOptions = []
        for oriCurrent in range(game.currentPiece.numOrientations()):
            for posCurrent in range(gridWidth - game.currentPiece.width(oriCurrent) + 1):
                for oriNext in range(game.nextPiece.numOrientations()):
                    for posNext in range(gridWidth - game.nextPiece.width(oriNext) + 1):
                        myGame = Game(clone=game)
                        myGame.currentPiece.ori = oriCurrent
                        myGame.currentPiece.col = posCurrent
                        myGame.nextPiece.ori = oriNext
                        myGame.nextPiece.col = posNext
                        rowAddedAt = myGame.dropPiece()
                        myGame.dropPiece()  # this automatically sets up pieces which is kind of wasteful and makes the following line complex
                        allOptions.append(Option(myGame.grid, oriCurrent, posCurrent, oriNext, posNext, myGame.numLinesCleared, rowAddedAt))
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


class FastPlayer(object):
    def playGame(self):
        game = Game(isRendered=True)
        while game.isAlive():
            allOptions = self.allOptions(game)

            bestOption = self.bestOption(allOptions)

            game.currentPiece.ori = bestOption.oriCurrent
            game.currentPiece.col = bestOption.posCurrent

            game.dropPiece()

            game.render()
            print("here")
        game.render()
        game.screen.blit(font.render("Score: " + str(game.numLinesCleared), True, (0, 0, 255)), (10, 100))
        pygame.display.update()
        keyPressed = False
        while not keyPressed:
            pygame.time.wait(100)
            for event in pygame.event.get():
                keyPressed = event.type
        pygame.display.quit()
        #sys.exit()

    def allOptions(self, game):  # could this just be one big list comprehension?
        allOptions = []
        for oriCurrent in range(game.currentPiece.numOrientations()):
            for posCurrent in range(gridWidth - game.currentPiece.width(oriCurrent) + 1):
                myGame = Game(clone=game)
                myGame.currentPiece.ori = oriCurrent
                myGame.currentPiece.col = posCurrent
                rowAddedAt = myGame.dropPiece()  # this automatically sets up pieces which is kind of wasteful and makes the following line complex
                allOptions.append(Option(myGame.grid, oriCurrent, posCurrent, 0, 0, myGame.numLinesCleared, rowAddedAt))
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


SimplePlayer().playGame()
HumanPlayer().playGame()
pygame.time.wait(500)
FastPlayer().playGame()

x = "don't end debugging"

# eventually I should should make sure that when a human user rotates a piec when pushed against the right side the piece never go off the grid
# ^ it simply doesn't rotate as of now, which I think is okay

# I'm not sure how efficiency works in python, so I have done stuff to try to make it use pointers but I don't what Python is actually doing...
