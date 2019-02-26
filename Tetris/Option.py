import Game

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
        for row in range(Game.gridHeight):
            isEmpty = True
            for col in range(Game.gridWidth):
                if self.grid[row][col]:
                    self.numFilled += 1
                    isEmpty = False

                    if col > 0 and not self.grid[row][col - 1]:
                        self.perimeter += 1
                    if row < Game.gridHeight - 1 and not self.grid[row + 1][col]:
                        self.perimeter += 1
                    if col < Game.gridWidth - 1 and not self.grid[row][col + 1]:
                        self.perimeter += 1
                    if row > 0 and not self.grid[row - 1][col]:
                        self.perimeter += 1
            if isEmpty:
                self.height = row
                return #(self.numFilled, self.perimeter, self.height)