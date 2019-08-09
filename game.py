import random
from graphics import *
win = GraphWin(width = 1000, height = 1000)
win.setCoords(0, 0, win.width, win.height)

cellSize = 25
gapSize = 2
cells = []
# List of cells to toggle so they can all be done at once after checking everything
cellsToUpdate = []

class Cell:
    alive = False
    def __init__(self, i, j):
        self.i = i
        self.j = j
        x = i * cellSize
        y = j * cellSize
        self.rect = Rectangle(Point(x + gapSize, y + gapSize), Point(x + cellSize - gapSize, y + cellSize - gapSize))
        self.rect.setFill("white")
        self.needsCheck = False
    
    def toggle(self):
        #toggles state and changes fill color
        if(self.alive):
            self.alive = False
            self.rect.setFill("white")
        else:
            self.alive = True
            self.rect.setFill("black")
        self.rect.draw
        
    def check(self):
        # Counts the surrounding cells that are alive
        numAlive = 0
        
        if(self.i > 0 and self.j > 0):
            if(cells[self.i-1][self.j-1].alive):
                numAlive += 1
            elif(self.alive):
                # If self is alive and other cell is not, mark it for check on second pass
                cells[self.i-1][self.j-1].needsCheck = True
        
        if(self.i > 0):
            if(cells[self.i-1][self.j].alive):
                numAlive += 1
            elif(self.alive):
                cells[self.i-1][self.j].needsCheck = True
        
        if(self.i > 0 and self.j < len(cells[0]) - 1):
            if(cells[self.i-1][self.j+1].alive):
                numAlive += 1
            elif(self.alive):
                cells[self.i-1][self.j+1].needsCheck = True
        
        if(self.j < len(cells[0]) - 1):
            if(cells[self.i][self.j+1].alive):
                numAlive += 1
            elif(self.alive):
                cells[self.i][self.j+1].needsCheck = True
        
        if(self.i < len(cells) - 1 and self.j < len(cells[0]) - 1):
            if(cells[self.i+1][self.j+1].alive):
                numAlive += 1
            elif(self.alive):
                cells[self.i+1][self.j+1].needsCheck = True
        
        if(self.i < len(cells) - 1):
            if(cells[self.i+1][self.j].alive):
                numAlive += 1
            elif(self.alive):
                cells[self.i+1][self.j].needsCheck = True
        
        if(self.i < len(cells) - 1 and self.j > 0):
            if(cells[self.i+1][self.j-1].alive):
                numAlive += 1
            elif(self.alive):
                cells[self.i+1][self.j-1].needsCheck = True
        
        if(self.j > 0):
            if(cells[self.i][self.j-1].alive):
                numAlive += 1
            elif(self.alive):
                cells[self.i][self.j-1].needsCheck = True
        
        if(self.alive):
            if(numAlive <= 1 or numAlive >= 4):
                cellsToUpdate.append(self)
        
        if(not self.alive):
            if(numAlive == 3):
                cellsToUpdate.append(self)
        
        self.needsCheck = False


for i in range(int(win.height / cellSize)):
    row = []
    
    for j in range(int(win.width / cellSize)):
        newCell = Cell(i, j)
        newCell.rect.draw(win)
        row.append(newCell)
    
    cells.append(row)

print("Welcome to Heath's Game of Life simulator!")
print("Instructions:")
print("\'k\' to close the game")
print("\'n\' to advance a step")
print("\'c\' to clear the board")
print("\'r\' to randomize each cell")

lastKey = ""
# K closes the window by reaching the end of the file
while(lastKey != "k"):
    clickPoint = win.checkMouse()
    if(clickPoint):
        cellX = int(clickPoint.getX() / cellSize)
        cellY = int(clickPoint.getY() / cellSize)
        cells[cellX][cellY].toggle()
    
    lastKey = win.checkKey()
    if(lastKey == "n"):
        
        # First pass, check cells that are alive
        for row in cells:
            for cell in row:
                if(cell.alive):
                    cell.check()
                    
        # Second pass, check cells adjacent to live cells
        for row in cells:
            for cell in row:
                if(cell.needsCheck):
                    cell.check()
                    
        #Toggle all cells in cellsToUpdate
        for cell in cellsToUpdate:
            cell.toggle()

            
        cellsToUpdate = []
        
    # C clears the board
    elif(lastKey == "c"):
        for row in cells:
            for cell in row:
                if(cell.alive):
                    cell.toggle()
                    
    # R randomizes the cells
    elif(lastKey == "r"):
        for row in cells:
            for cell in row:
                if(random.choice([True, False])):
                    cell.toggle()