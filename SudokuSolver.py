# [NOTE] Rendering is handled by rastering since I want this to be entirely cross platform/terminal compatable

class Sudoku_Cell:
    def __init__(self, default = [1, 2, 3, 4, 5, 6, 7, 8, 9]):
        self.data = default

    def raster(self):
        retVal = ". "

        if len(self.data) == 1:
            retVal = "{} ".format(self.data[0])

        return retVal

    def setValue(self, value):
        if type(value) == list: self.data = value    # In the event that we pass a new list of integers
        else: self.data = [int(value)]    # In the event that we pass a single integer

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

    def getPattern(self):
        retVal = ""

        for y in range(self.width):
            for x in range(self.height):
                value = self.getValueXY(x, y)
                if len(value) == 1: retVal += "{}".format(value[0])
                else: retVal += "0"

        return retVal

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

    def iterate(self):
        self.purgeRows()
        self.board.rotate("cw")
        self.purgeRows()
        self.board.rotate("ccw")

        self.purgeBlocks()

        self.checkBlocksStragglers()

    # In the event master cannot solve the game
    def spawnGames(self):
        pattern = self.board.getPattern()

        for y in range(self.board.height):
            for x in range(self.board.width):
                value = self.board.getValueXY(x, y)
                if len(value) == 1: continue    # No need to try another game if the value is already known
                for item in value:
                    game = Sudoku()
                    game.board.setPattern(pattern)
                    game.board.setValueXY(x, y, item)
                    game.solve(isMaster = False)

    def solve(self, isMaster = True):
        # Do this a bunch of times to ensure equilibrium is achieved
        for n in range(100): self.iterate()

        if self.isSolved():
            print("Yay it's solved!")
            self.board.render()
            print(self.board.getPattern())
            exit()

        # If there is no solution we iterate through all values until a solution is generated, hopefully
        # We only want the master to generate new boards, otherwise we'll end up in an endless loop
        if isMaster: self.spawnGames()

    def isSolved(self):
        for y in range(self.board.height):
            for x in range(self.board.width):
                value = self.board.getValueXY(x, y)
                if len(value) > 1: return False
        return True

    """ This will purge non-possible values from each row """
    def purgeRows(self):
        for y in range(self.board.height):
            self.purgeRow(y)

    def purgeRow(self, y):
        # First we go through and check all values that are known
        seen = []
        for x in range(self.board.width):
            value = self.board.getValueXY(x, y)
            if len(value) == 1: seen.append(value[0])

        # Then we go through and purge those values from any cell that is not known
        for x in range(self.board.width):
            value = self.board.getValueXY(x, y)
            if len(value) != 1:
                value = [i for i in value if i not in seen]
                self.board.setValueXY(x, y, value)

    """ This will purge non-possible values from each block """
    def purgeBlocks(self):
        for y in range(self.board.columns):
            for x in range(self.board.rows):
                self.purgeBlock(x, y)

    def purgeBlock(self, x, y):
        block = self.board.getBlock(x, y)

        # First we go through and check all values that are known
        seen = []
        for y in range(block.height):
            for x in range(block.width):
                value = block.getValue(x, y)
                if len(value) == 1: seen.append(value[0])

        # Then we go through and purge those values from any cell that is not known
        for y in range(block.height):
            for x in range(block.width):
                value = block.getValue(x, y)
                if len(value) != 1:
                    value = [i for i in value if i not in seen]
                    block.setValue(x, y, value)

    """ This will check for values that can only be in a single block and no others """
    def checkBlocksStragglers(self):
        for y in range(self.board.columns):
            for x in range(self.board.rows):
                self.checkBlockStragglers(x, y)

    def checkBlockStragglers(self, x, y):
        block = self.board.getBlock(x, y)

        # First we count how often each possible value can be seen
        counts = {}
        for y in range(block.height):
            for x in range(block.width):
                value = block.getValue(x, y)
                for item in value:
                    if item in counts: counts[item] += 1
                    else: counts[item] = 1

        # Then we create a list of values that we are certain are unique
        uniques = []
        for key in counts:
            if counts[key] == 1:
                uniques.append(key)

        # Then we iterate through and purge all other values from cells that contain only unique values
        for y in range(block.height):
            for x in range(block.width):
                value = block.getValue(x, y)
                possible = set(value) & set(uniques)
                if len(possible) > 0:
                    block.setValue(x, y, list(possible))

examples = [
"003020600900305001001806400008102900700000008006708200002609500800203009005010300",
"200080300060070084030500209000105408000000000402706000301007040720040060004010003",
"000000907000420180000705026100904000050000040000507009920108000034059000507000000",
"030050040008010500460000012070502080000603000040109030250000098001020600080060020"
]
game = Sudoku()
game.board.setPattern(examples[2])
game.board.render()
game.solve()
