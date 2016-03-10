import random
from Tkinter import *
from eventBasedAnimationClass import EventBasedAnimationClass

class SameGame(EventBasedAnimationClass):
    def __init__(self,rows,cols,numColors):
        margin = 100
        cellSize = 30
        self.canvasWidth = 2*margin + cols*cellSize
        self.canvasHeight = 2*margin + rows*cellSize
        super(SameGame,self).__init__(self.canvasWidth,self.canvasHeight)
        self.margin = margin
        self.cellSize = cellSize
        self.rows = rows
        self.cols = cols
        self.numColors = numColors
        self.colors = ["red","blue","green","yellow","dark violet","orange",
                       "deep pink","brown","sienna","cyan","white"]
        self.score = 0
        self.increment = 0
        self.timer = 5
        self.highscore = self.score
        self.highlight = False

    def onKeyPressed(self,event):
        if (event.char == "r"):
            self.score = 0
            self.timer = 5
            self.increment = 0
            self.highlight = False
            self.loadBoard()

    def onMousePressed(self,event):
        board = self.board
        rows = self.rows
        cols = self.cols
        margin = self.margin
        cellSize = self.cellSize
        if (event.x<cols*cellSize+margin and event.x>margin and event.y>margin
            and event.y<rows*cellSize+margin):
            (self.mouseX,self.mouseY) = (event.x,event.y)
            self.adjacentList = []
            clickedRow = (event.y-margin)/cellSize
            clickedCol = (event.x-margin)/cellSize
            clickedColor = board[clickedRow][clickedCol]
            self.findBlocks(clickedRow,clickedCol,clickedColor)
            self.removeBlocks()
            if (clickedColor != "" and not(len(self.adjacentList)==1)):
                self.timer = 5
                self.increment = 0
        self.highlight = False

    def mouseMotion(self,event):
        board = self.board
        rows = self.rows
        cols = self.cols
        margin = self.margin
        cellSize = self.cellSize
        if (event.x<cols*cellSize+margin and event.x>margin and event.y>margin
            and event.y<rows*cellSize+margin):
            (self.hoverX,self.hoverY) = (event.x,event.y)
            self.hoverList = []
            hoverRow = (event.y-margin)/cellSize
            hoverCol = (event.x-margin)/cellSize
            hoverColor = board[hoverRow][hoverCol]
            self.hoverBlocks(hoverRow,hoverCol,hoverColor)
            self.highlightBlocks(hoverColor)
        else:
            self.highlight = False

    def onTimerFired(self):
        if (not self.isGameOver):
            self.timerDelay = 500
            check = 2
            delay = 10
            self.increment += 1
            if (self.increment%check == 0 and self.increment>0 and self.timer>0):
                self.timer -= 1
            if (self.increment == delay):
                self.increment = 0
            if (self.timer == 0):
                self.timeOver()
            
    def timeOver(self):
        if (self.score >= 20):
            self.score -= 20
        self.timer = 5
        self.increment = 0

    def hoverBlocks(self,row,col,color):
        board = self.board
        rows = self.rows
        cols = self.cols
        if ((row >= 0) and (row < rows) and (col >= 0) and (col < cols) and
            (board[row][col] == color) and board[row][col] != ""):
            self.hoverList += [(row,col)]
            if ((row-1,col) not in self.hoverList):
                self.hoverBlocks(row-1,col,color)
            if ((row+1,col) not in self.hoverList):
                self.hoverBlocks(row+1,col,color)
            if ((row,col-1) not in self.hoverList):
                self.hoverBlocks(row,col-1,color)
            if ((row,col+1) not in self.hoverList):
                self.hoverBlocks(row,col+1,color)
        else:
            self.highlight = False

    def highlightBlocks(self,color):
        board = self.board
        hoverList = self.hoverList
        rows = self.rows
        cols = self.cols
        if (not(len(hoverList)==1)):
            for i in xrange(len(hoverList)):
                (row,col) = hoverList[i]
                self.highlight = True
                self.highlightColor = color
        else:
            self.highlight = False
        
    def findBlocks(self,row,col,color):
        board = self.board
        rows = self.rows
        cols = self.cols
        if ((row >= 0) and (row < rows) and (col >= 0) and (col < cols) and
            (board[row][col] == color) and board[row][col] != ""):
            self.adjacentList += [(row,col)]
            if ((row-1,col) not in self.adjacentList):
                self.findBlocks(row-1,col,color)
            if ((row+1,col) not in self.adjacentList):
                self.findBlocks(row+1,col,color)
            if ((row,col-1) not in self.adjacentList):
                self.findBlocks(row,col-1,color)
            if ((row,col+1) not in self.adjacentList):
                self.findBlocks(row,col+1,color)

    def removeBlocks(self):
        board = self.board
        adjacentList = self.adjacentList
        rows = self.rows
        cols = self.cols
        newBoard = [ ]
        if (not(len(adjacentList)==1)):
            self.score += (len(adjacentList)**2)
            for i in xrange(len(adjacentList)):
                (row, col) = adjacentList[i]
                board[row][col] = ""
        self.moveBlocks()

    def moveBlocks(self):
        rows = self.rows
        cols = self.cols
        for col in xrange(cols):
            for row in xrange(rows-1,0,-1):
                if (self.board[row][col] == ""):
                    for rest in xrange(row-1,-1,-1):
                        if (self.board[rest][col] != ""):
                            temp = self.board[row][col]
                            self.board[row][col] = self.board[rest][col]
                            self.board[rest][col] = temp
                            break
        if ("" in self.board[rows-1]):
            count = self.board[rows-1].count("")
            for i in xrange(count):
                index = self.board[rows-1].index("")
                for row in xrange(rows):
                    for col in xrange(index,cols-1):
                        self.board[row][col] = self.board[row][col+1]
                    self.board[row][cols-1] = ""

    def checkGameOver(self):
        board = self.board
        rows = self.rows
        cols = self.cols
        for row in xrange(rows):
            for col in xrange(cols):
                if (board[row][col] != ""):
                    self.gameOverList = []
                    self.checkBoard(row,col,board[row][col])
                    if (len(self.gameOverList) != 1):
                        return False
        return True

    def checkBoard(self,row,col,color):
        board = self.board
        rows = self.rows
        cols = self.cols
        if ((row >= 0) and (row < rows) and (col >= 0) and (col < cols) and
            (board[row][col] == color) and board[row][col] != ""):
            self.gameOverList += [(row,col)]
            if ((row-1,col) not in self.gameOverList):
                self.checkBoard(row-1,col,color)
            if ((row+1,col) not in self.gameOverList):
                self.checkBoard(row+1,col,color)
            if ((row,col-1) not in self.gameOverList):
                self.checkBoard(row,col-1,color)
            if ((row,col+1) not in self.gameOverList):
                self.checkBoard(row,col+1,color)
                

    def genColors(self):
        board = self.board
        colors = self.colors
        rows = self.rows
        cols = self.cols
        numColors = self.numColors
        for row in xrange(rows):
            for col in xrange(cols):
                colorIndex = random.randint(0,numColors-1)
                board[row][col] = colors[colorIndex]
        self.board = board

    def loadBoard(self):
        rows = self.rows
        cols = self.cols
        board = [ ]
        for row in xrange(rows): board += [[0] * cols]
        self.board = board
        self.genColors()

    def drawGame(self):
        self.canvas.create_rectangle(0,0,self.canvasWidth,self.canvasHeight,
                                     fill="black")
        self.drawBoard()
        

    def drawBoard(self):
        board = self.board
        rows = len(board)
        cols = len(board[0])
        for row in xrange(rows):
            for col in xrange(cols):
                self.drawCell(row, col,board[row][col])

    def drawCell(self, row, col, color):
        margin = self.margin
        cellSize = self.cellSize
        left = margin + col * cellSize
        right = left + cellSize
        top = margin + row * cellSize
        bottom = top + cellSize
        self.canvas.create_rectangle(left, top, right, bottom, fill=color,
                                      width=3)

    def drawOutline(self,row,col,color):
        margin = self.margin
        cellSize = self.cellSize
        left = margin + col * cellSize
        right = left + cellSize
        top = margin + row * cellSize
        bottom = top + cellSize
        self.canvas.create_rectangle(left, top, right, bottom, fill=color,
                                      width=10)

    def drawScore(self):
        margin = self.margin
        scoreDisplay = "Score: %d" % (self.score)
        self.canvas.create_text(self.canvasWidth-margin,margin/2,
                                text=scoreDisplay,font="Arial 20",fill="white")

    def drawHighscore(self):
        margin = self.margin
        scoreDisplay = "Highscore: %d" % (self.score)
        self.canvas.create_text(self.canvasWidth/2,margin/2,
                                text=scoreDisplay,font="Arial 20",fill="white")

    def drawTimer(self):
        margin = self.margin
        timeDisplay = "Time Left: %d" % (self.timer)
        self.canvas.create_text(margin,margin/2,text=self.timer,
                                font="Arial 20",fill="white")

    def gameOverScreen(self):
        score = "Score = %d" % (self.score)
        self.canvas.create_rectangle(0,0,self.canvasWidth,self.canvasHeight,
                                fill="red")
        self.canvas.create_text(self.canvasWidth/2,self.canvasHeight/2,
                                text=score,font="Arial 20")
        
    def redrawAll(self):
        self.canvas.delete(ALL)
        self.gameOverList = []
        self.isGameOver = self.checkGameOver()
        self.drawGame()
        if (self.highlight):
            for i in xrange(len(self.hoverList)):
                (row,col) = self.hoverList[i]
                self.drawOutline(row,col,self.highlightColor)
        self.drawScore()
        self.drawHighscore()
        self.drawTimer()
        if (self.isGameOver):
            self.gameOverScreen()

    def initAnimation(self):
        self.loadBoard()
        self.isGameOver = False
        
playSameGame = SameGame(rows=10, cols=15, numColors=3)

playSameGame.run()
