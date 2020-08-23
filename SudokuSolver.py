# [NOTE] Rendering is handled by rastering since I want this to be entirely cross platform/terminal compatable

class Sudoku_Cell:
    def __init__(self, default = [1, 2, 3, 4, 5, 6, 7, 8, 9]):
        self.data = default

    def raster(self):
        retVal = ". "

        if len(self.data) == 1:
            retVal = "{} ".format(self.data[0])

        return retVal

    def setValue(self, value): self.data = [int(value)]

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

    def inspect(self):
        for y in range(self.height):
            for x in range(self.width):
                cell = self.getCell(x, y)
                print("\tValues for {}, {} are {}".format(x, y, cell.data))

    def getCell(self, x, y): return self.data[y][x]

    def getValue(self, x, y):
        cell = self.getCell(x, y)
        return cell.data

    def setValue(self, x, y, value):
        if value == "0" or value == ".": return

        cell = self.getCell(x, y)
        cell.setValue(value)

class Sudoku_Board:
    def __init__(self, rows = 3, columns = 3):
        self.rows = rows
        self.columns = columns

        self.data = [[Sudoku_Block() for x in range(self.columns)] for y in range(self.rows)]

        block = self.getBlock(0, 0)
        self.width = self.columns * block.width
        self.height = self.rows * block.height

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

    def inspect(self):
        for y in range(self.columns):
            for x in range(self.rows):
                print("Inspecting block {}, {}".format(x, y))
                block = self.getBlock(x, y)
                block.inspect()

    def getBlock(self, column, row): return self.data[row][column]

    def setValue(self, column, row, blockX, blockY, value):
        block = self.getBlock(column, row)
        block.setValue(blockX, blockY, value)

    def setValueXY(self, x, y, value):
        block = self.getBlock(0, 0)

        # [TODO] Find a more elegant way of doing this below, I'm tired and can't figure out the math right now...
        column = 0
        row = 0

        xCounter = 0
        for n in range(x):
            xCounter += 1
            if xCounter == block.width:
                column += 1
                xCounter = 0

        yCounter = 0
        for n in range(y):
            yCounter += 1
            if yCounter == block.height:
                row += 1
                yCounter = 0

        blockX = x - (column * block.width)
        blockY = y - (row * block.height)
        # [TODO] Find a more elegant way of doing this above, I'm tired and can't figure out the math right now...

        block = self.getBlock(column, row)
        block.setValue(blockX, blockY, value)

    ###
    def getValueXY(self, x, y):
        block = self.getBlock(0, 0)

        # [TODO] Find a more elegant way of doing this below, I'm tired and can't figure out the math right now...
        column = 0
        row = 0

        xCounter = 0
        for n in range(x):
            xCounter += 1
            if xCounter == block.width:
                column += 1
                xCounter = 0

        yCounter = 0
        for n in range(y):
            yCounter += 1
            if yCounter == block.height:
                row += 1
                yCounter = 0

        blockX = x - (column * block.width)
        blockY = y - (row * block.height)
        # [TODO] Find a more elegant way of doing this above, I'm tired and can't figure out the math right now...

        block = self.getBlock(column, row)
        return block.getValue(blockX, blockY)
    ###

    def setPattern(self, pattern):
        block = self.getBlock(0, 0)
        assert len(pattern) == self.width * self.height

        n = self.rows * block.width
        rows = [pattern[i:i+n] for i in range(0, len(pattern), n)]

        for y in range(self.height):
            for x in range(self.width):
                value = rows[y][x]
                self.setValueXY(x, y, value)

    def rotate(self, direction):
        if direction == "cw":
            for y in range(self.columns):
                for x in range(self.rows):
                    block = self.getBlock(x, y)
                    block.data = list(zip(*block.data[::-1]))
            self.data = list(zip(*self.data[::-1]))

        if direction == "ccw":
            for n in range(3): self.rotate("cw")

class Sudoku:
    def __init__(self):
        self.board = Sudoku_Board()

    def solve(self):
        self.purgeRows()

        #rotate cw
        #purgeRows()
        #rotate ccw
        #purge blocks

    """ This will purge non-possible values from each row """
    def purgeRows(self):
        self.purgeRow(0)

    def purgeRow(self, y):
        pass

    """ This will purge non-possible values from each block """
    def purgeBlocks(self):
        pass

game = Sudoku()
game.board.setPattern("003020600900305001001806400008102900700000008006708200002609500800203009005010300")
game.board.render()
game.solve()
#game.board.inspect()
