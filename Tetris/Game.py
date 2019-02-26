import Piece
import pygame
import copy
import random

black = (0, 0, 0)
white = (255, 255, 255)
pygame.font.init()
font = pygame.font.Font(None, 36)

gridWidth = 10
gridHeight = 40
squareLength = 10  # pixels

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
        self.currentPiece = Piece.Piece(Piece.intToBitMaps[random.randint(0, 6)])  # there are 7 pieces to choose from
        self.nextPiece = Piece.Piece(Piece.intToBitMaps[random.randint(0, 6)])
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
        self.nextPiece = Piece.Piece(Piece.intToBitMaps[random.randint(0, 6)]) # there are 7 pieces
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
