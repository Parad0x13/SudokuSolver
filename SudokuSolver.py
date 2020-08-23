# [NOTE] Rendering is handled by rastering since I want this to be entirely cross platform/terminal compatable

class Sudoku_Cell:
    def __init__(self, default = [1, 2, 3, 4, 5, 6, 7, 8, 9]):
        self.data = default

    def raster(self):
        retVal = ". "

        if len(self.data) == 1:
            retVal = "{} ".format(self.data[0])

        return retVal

    def setValue(self, value): self.data = [value]

class Sudoku_Block:
    def __init__(self, width = 3, height = 3):
        self.width = width
        self.height = height

        self.data = [[Sudoku_Cell() for x in range(self.width)] for y in range(self.height)]

    def raster(self, y):
        retVal = ""
        for x in range(self.width):
            retVal += self.data[y][x].raster()
        return retVal

    def getCell(self, x, y): return self.data[y][x]

    def setValue(self, x, y, value):
        cell = self.getCell(x, y)
        cell.setValue(value)

class Sudoku_Board:
    def __init__(self, rows = 3, columns = 3):
        self.rows = rows
        self.columns = columns

        self.data = [[Sudoku_Block() for x in range(self.columns)] for y in range(self.rows)]

    def raster(self, row, blockY):
        retVal = ""
        retVal += "| "
        for x in range(self.columns):
            part = self.data[row][x].raster(blockY)
            retVal += part
            retVal += "| "
        return retVal

    def raster_rowSeperator(self):
        retVal = ""

        blockWidth = len(self.data[0][0].raster(0))
        for x in range(self.columns):
            retVal += "+-"
            retVal += "-" * blockWidth
        retVal += "+"

        return retVal

    def render(self):
        rowSeperator = self.raster_rowSeperator()
        print(rowSeperator)
        for y in range(self.rows):
            blockHeight = self.data[0][0].height
            for bY in range(blockHeight):
                #line = self.raster(y)
                line = self.raster(y, bY)
                print(line)
            print(rowSeperator)

    def getBlock(self, column, row): return self.data[row][column]

    def setValue(self, column, row, blockX, blockY, value):
        block = self.getBlock(column, row)
        block.setValue(blockX, blockY, value)

class Sudoku:
    def __init__(self):
        self.board = Sudoku_Board()

game = Sudoku()
game.board.setValue(0, 0, 0, 0, 4)
game.board.render()
