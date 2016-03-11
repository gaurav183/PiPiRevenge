from Tkinter import *
from eventBasedAnimationClass import EventBasedAnimationClass
import random
import math

# clams that seb must avoid
class Clam(object):
    def __init__(self,x,y):
        self.x = x
        self.y = y
        # taken from 
        # http://www.disneyclips.com/imagesnewb4/imageslwrakr01/clipclam.gif
        self.clam = PhotoImage(file = "clipclam.gif")
        self.clam = self.clam.subsample(4,4)
        self.r = self.clam.width()/2 

    def draw(self,canvas):
        cx = self.x
        cy = self.y
        canvas.create_image(cx,cy,image = self.clam)

# the scorpion that sebastian shoots
class Scorpion(object):
    def __init__(self,x,y):
        self.x = x
        self.y = y
        # taken from 
        # http://www.disneyclips.com/imagesnewb4/imageslwrakr01/clipfish2123.gif
        self.scorpion = PhotoImage(file = "clipfish2123.gif")
        self.scorpion = self.scorpion.subsample(6,6)
        self.r = self.scorpion.width()/2

    def draw(self,canvas):
        x = self.x
        y = self.y
        canvas.create_image(x,y,image = self.scorpion)

# pixels to be drawn in the draw screen
class Pixel(object):
    def __init__(self,x,y):
        self.x = x
        self.y = y
        self.r = 3

    def draw(self,canvas):
        cx,cy = self.x,self.y
        r = self.r
        canvas.create_rectangle(cx-r,cy-r,cx+r,cy+r,fill = "cyan",
            outline = "cyan")

class UnderTheSea(EventBasedAnimationClass):
    def __init__(self):
        super(UnderTheSea,self).__init__(800,800)

    def initAnimation(self):
        self.gameOver = False
        scaleFactor = 0.9
        self.screenScaleFactor = 0.35
        self.currentScore = 500
        # initializes sebastian's position to the bottom center
        self.SebastianX = self.width/4
        self.SebastianY = scaleFactor * self.height
        # based on the image of sebastian
        # divide by 5 because image is subsample
        self.SebastianR = (375/2)/5
        self.timerDelay = 75
        # sets the number of clams on the screen
        self.numOfclams = 5
        # based on the clam image
        # divide by 4 because image is subsample
        self.clamR = (168/2)/4
        self.clamList = self.makeclamList()
        # B1-Motion and B1-ButtonRelease allow for drawing
        self.root.bind("<B1-Motion>", 
            lambda event: self.leftMousePressed(event))
        self.root.bind("<B1-ButtonRelease>", 
            lambda event: self.leftMouseReleased(event))
        self.root.bind("<Motion>", lambda event: self.onMouseMotion(event))
        self.clickX,self.clickY = None,None
        self.mouseX,self.mouseY = None,None
        self.deltaX,self.deltaY = None,None
        self.speedFactor = 10
        # randomly places Ursula on the screen initially
        # ursulaR based on the dimensions of picture
        self.ursulaR = 195/2
        self.ursulaX = random.randint(0+self.ursulaR,
            self.width/2-self.ursulaR)
        self.ursulaY = self.ursulaR
        # randomly places flounder on screen initially
        # flounderR based on dimensions of picture
        self.flounderR = 300/2
        self.flounderX = random.randint(0+self.flounderR,
            self.width/2-self.flounderR)
        self.flounderY = random.randint(0+self.flounderR,3*self.height/4)
        self.pixelXList,self.pixelYList = [],[]
        self.pixelList,self.pixelCoordList = [],[]
        self.isCircle = False
        self.sebastian = None
        # turns on the splash screen when first run the game
        self.splashScreen = True
        # sets the values for all the buttons so they don't change
        self.startButtonX0,self.startButtonY0 = self.width/2-80,self.height/2.5
        self.startButtonX1 = self.width/2+80
        self.startButtonY1 = self.startButtonY0 + 70
        self.helpButtonX0 = self.width/2-80
        self.helpButtonY0 = self.startButtonY1 + 30
        self.helpButtonX1 = self.width/2+80
        self.helpButtonY1 = self.helpButtonY0 + 70
        self.highSButtonX0 = self.width/2-80
        self.highSButtonY0 = self.helpButtonY1 + 35
        self.highSButtonX1 = self.width/2+80
        self.highSButtonY1 = self.highSButtonY0 + 70
        self.restartX0 = self.width/4- 80
        self.restartY0 = 5 * self.height/8
        self.restartX1 = self.width/4 + 80
        self.restartY1 = self.restartY0 + 70
        self.backX0 = self.width/2 - 80
        self.backY0 = 5 * self.height / 6
        self.backX1 = self.width/2 + 80
        self.backY1 = self.backY0 + 70
        # initializes all the text color to black
        self.backColor,self.restartColor = "black","black"
        self.startColor,self.helpColor = "black","black",
        self.highScoreColor = "black"
        # makes sure only splash screen is on
        self.helpScreen = False
        self.scorpionList = []
        # displays high score from file
        # taken from my own hw10 line 55
        self.highScore = self.highScoreFromFile()
        self.scorpX,self.scorpY = None,None
        # variables to separate sebastian and ursula movement
        self.dontMoveUrsula = False
        self.ursulaDies = False
        self.flounderCaught = False
        # determines why sebastian is at the bottom of the screen --> moving
        # to new path or because user drew him going down
        self.newPath = False

# DRAWING INITIAL CHARACTERS

    def makeclamList(self):
        clamList = []
        for clam in xrange(self.numOfclams):
            # randomizes the coordinates of the clams
            clamX = random.randint(0,(self.width/2-self.clamR))
            clamY = random.randint(0,3 * self.height/4)
            clamList.append(Clam(clamX,clamY))
        return clamList

    def drawSebastian(self):
        # taken from 
        # http://www.disneyclips.com/imagesnewb4/imageslwrakr01/apl1523.gif
        self.sebastian = PhotoImage(file = "sebastian.gif")
        self.sebastian = self.sebastian.subsample(5,5)
        self.canvas.create_image(self.SebastianX,self.SebastianY,
            image = self.sebastian)
        self.SebastianR = min(self.sebastian.width(),self.sebastian.height())/2
        # determines if the shape drawn is a circle
        if self.isCircle:
            # makes sebastian go forward if circle is drawn
            self.deltaX = 0
            self.deltaY = -1
            # creates a new scorpion based on seb's position
            self.scorpX = self.SebastianX
            self.scorpY = self.SebastianY
            newScorp = Scorpion(self.scorpX,self.scorpY)
            self.scorpionList.append(newScorp)
            self.isCircle = False

    def shoot(self):
        for scorp in self.scorpionList:
            scorp.draw(self.canvas)
            # determines if scorp touches clam
            self.checkScorpClamCollision(scorp.x,scorp.y,scorp.r)

    def drawUrsula(self):
        # taken from 
        # http://www.disneyclips.com/imagesnewb4/imageslwrakr01/clipursula.gif
        self.ursula = PhotoImage(file = "clipursula.gif")
        self.ursula = self.ursula.subsample(3,3)
        self.canvas.create_image(self.ursulaX,self.ursulaY,
            image = self.ursula)
        self.ursulaR = min(self.ursula.width(),self.ursula.height())/2
        # checks if ursula hits sebastian every time she's drawn
        self.checkSebastianCollision(self.ursulaX,self.ursulaY,self.ursulaR)
        for scorp in self.scorpionList:
            # checks if scorp collision everytime she's drawn
            if self.checkUrsScorpCollision(scorp.x,scorp.y,scorp.r):
                self.ursulaDies = True

    def drawclams(self):
        for clam in self.clamList:
            clam.draw(self.canvas)
            # checks if seb has collided every time drawn
            self.checkSebastianCollision(clam.x,clam.y,clam.r)

    def drawFlounder(self):
        # taken from 
        # http://www.disneyclips.com/imagesnewb4/imageslwrakr01/jan1018.gif
        self.flounder = PhotoImage(file = "flounder.gif")
        self.flounder = self.flounder.subsample(4,4)
        self.canvas.create_image(self.flounderX,self.flounderY,
            image = self.flounder)
        self.flounderR = min(self.flounder.width(),self.flounder.height())/2
        # checks if sebastian has caught flounder every time flounder drawn
        if self.checkSebFlounderCollision(self.flounderX,
            self.flounderY,self.flounderR):
            self.flounderCaught = True
            # increases the score if flounder is caught
            self.currentScore += 30
        
    # randomizes a new position for ursula on the screen
    def drawRandomUrsula(self):
        # makes sure she doesn't go off the screen
        self.ursulaX = random.randint(0+self.ursulaR,
            self.width/2-self.ursulaR)
        # starts her at the top of the screen
        self.ursulaY = self.ursulaR
        self.ursula = PhotoImage(file = "clipursula.gif")
        self.ursula = self.ursula.subsample(3,3)
        self.canvas.create_image(self.ursulaX,self.ursulaY,
            image = self.ursula)
        self.ursulaR = min(self.ursula.width(),self.ursula.height())/2

    # randomizes a new pos for flounder on screen
    def drawRandomFlounder(self):
        # makes sure flounder doesn't go off screen
        self.flounderX = random.randint(0+self.flounderR,
            self.width/2-self.flounderR)
        self.flounderY = random.randint(0+self.flounderR,3*self.height/4)
        self.flounder = PhotoImage(file = "clipursula.gif")
        self.flounder = self.ursula.subsample(3,3)
        self.canvas.create_image(self.flounderX,self.flounderY,
            image = self.flounder)
        self.flounderR = min(self.flounder.width(),self.flounder.height())/2

#COLLISION CHECKS
    # for all collisions,checks if distance between two centers of circles
    # is less than the sum of the radii

    # scorpion x,y,r values passed in
    def checkScorpClamCollision(self,cx,cy,cr):
        for clam in self.clamList:
            x = clam.x
            y = clam.y
            r = clam.r
            # gets rid of clam that scorp comes in contact with
            if ((cx-x)**2+(cy-y)**2)**0.5 <= (cr + r):
                self.clamList.remove(clam)

    # scorpion x,y,r values passed in
    def checkUrsScorpCollision(self,cx,cy,cr):
        x = self.ursulaX
        y = self.ursulaY
        r = self.ursulaR
        if (((cx-x)**2+(cy-x)**2)**0.5 <= (cr + r)
            or UnderTheSea.almostEqual(((cx-x)**2+(cy-y)**2)**0.5,
                cr+r)):
                return True
        return False

    def checkSebastianCollision(self,cx,cy,r):
        if (((((cx-self.SebastianX)**2+(cy-self.SebastianY)**2)**0.5) <= 
            (self.SebastianR + r))
            # also checks if the radius is the same
            or (UnderTheSea.almostEqual(
                ((cx-self.SebastianX)**2+(cy-self.SebastianY)**2)**0.5,
                self.SebastianR+r))):
            self.gameOver = True

    def checkSebFlounderCollision(self,cx,cy,r):
        if (((((cx-self.SebastianX)**2+(cy-self.SebastianY)**2)**0.5) <= 
            (self.SebastianR + r))
            # also checks if the radius is the same
            or (UnderTheSea.almostEqual(
                ((cx-self.SebastianX)**2+(cy-self.SebastianY)**2)**0.5,
                self.SebastianR+r))):
            return True
        return False


# IDENTIFYING DRAWINGS
    
    @staticmethod
    # used for the circle drawings because lack of precision
    def kindaAlmostEqual(a,b,epsilon = 15):
        return abs(a-b) < epsilon

    def distance(self,x0,y0,x1,y1):
        return ((x0-x1)**2+(y0-y1)**2)**0.5

    @staticmethod
    def almostEqual(a,b,epsilon = 10*10**-6):
        return abs(a - b) < epsilon

    @staticmethod
    def inCircle(x,y,cx,cy,r):
        return UnderTheSea.almostEqual(float(((x-cx)**2+(y-cy)**2)**0.5),
            float(r))

    # using the list of pixel objs, creates lists of sep coordinates
    # this makes it easier to analyze in "checkInCircle" fcn
    def createPixelLists(self):
        self.pixelXList = []
        self.pixelYList = []
        self.pixelCoordList = []
        for pixel in self.pixelList:
            self.pixelXList.append(pixel.x)
            self.pixelYList.append(pixel.y)
            self.pixelCoordList.append((pixel.x,pixel.y))

    # uses the first and last pixels to create unit vector
    def calculateDeltaMovement(self):
        self.dontMoveUrsula = False
        if len(self.pixelList) > 0:
            # x and y coords of first pixel
            x0 = self.pixelList[0].x
            y0 = self.pixelList[0].y
            length = len(self.pixelList)
            # x and y coords of last pixel
            x1 = self.pixelList[length-1].x
            y1 = self.pixelList[length-1].y
            # finds the magnitude of vector formed by first and last pt
            distance = ((x0-x1)**2+(y0-y1)**2)**0.5
            if distance != 0:
                # creates x and y components of unit vector
                self.deltaX = (x1-x0)/distance
                self.deltaY = (y1-y0)/distance
            # if the distance is zero, avoid division by zero
            else:
                self.deltaX,self.deltaY = 0,0
        self.pixelList = []

    def checkInCircle(self):
        # makes sure didn't just draw a short line
        if len(self.pixelCoordList) > 10:
            # makes sure that first and last points are around the same
            if ((UnderTheSea.kindaAlmostEqual(self.pixelXList[0],
                self.pixelXList[len(self.pixelXList)-1]))
                and (UnderTheSea.kindaAlmostEqual(self.pixelYList[0],
                    self.pixelYList[len(self.pixelYList)-1]))):
                # finds the min/max X coords and min/max Y coords
                minX = min(self.pixelXList)
                minXY = self.pixelYList[self.pixelXList.index(minX)]
                maxX = max(self.pixelXList)
                maxXY = self.pixelYList[self.pixelXList.index(maxX)]
                minY = min(self.pixelYList)
                minYX = self.pixelXList[self.pixelYList.index(minY)]
                maxY = max(self.pixelYList)
                maxYX = self.pixelXList[self.pixelYList.index(maxY)]
                if self.checkSameCenterPoint(minX,maxX,minY,maxY,minXY,maxXY,
                    minYX,maxYX):
                    # if the center point is the same, calculates the radius
                    radius = self.distance(minX,minXY,maxX,maxXY)/2
                    # and the center
                    cx = (minX+maxX)/2
                    cy = (minY+maxY)/2
                    # checks if the distance to the center is around the 
                    # same for all the points on the circle
                    for x,y in self.pixelCoordList:
                        return UnderTheSea.kindaAlmostEqual(
                            (self.distance(cx,cy,x,y)),(radius))
        else: return False

    # determines if the midpoint of the min/max Y points and midpt of 
    # min/max X points are around the same
    def checkSameCenterPoint(self,minX,maxX,minY,maxY,minXY,maxXY,minYX,maxYX):
        return ((UnderTheSea.kindaAlmostEqual((minX+maxX)/2,
            (maxYX+minYX)/2))and 
            (UnderTheSea.kindaAlmostEqual(((minY+maxY)/2),
                (maxXY+minXY)/2)))

    # draws the pixels on the black screen 
    def drawOnBlackScreen(self):
        for pixel in self.pixelList:
            pixel.draw(self.canvas)

# MOVE SEBASTIAN AND URSULA    

    def moveUrsula(self):
        if not self.gameOver:
            if self.deltaX != None and self.deltaY != None:
                # self.speedFactor = len(self.pixelCoordList)
                # checks that ursula is within the left screen constraints
                if ((self.ursulaX + self.ursulaR - 5 * self.deltaX >= 0) and 
                    (self.ursulaX - self.ursulaR - 5 * self.deltaX)
                     <= (self.width/2)): 
                    # ursula moves in same y direction if seb is going down 
                    if self.deltaY > 0 and self.ursulaY < self.SebastianY:
                        uDY = self.deltaY
                    # if ursula goes past seb, reverses her dir to follow seb
                    elif self.deltaY > 0 and self.ursulaY > self.SebastianY:
                        uDY = self.deltaY * -1
                    # if sebastian is going in reverse direction,
                    # reverses ursula's y dir to follow seb
                    elif self.deltaY < 0 and self.ursulaY < self.SebastianY:
                        uDY = self.deltaY * -1
                    # if ursula goes past seb, and seb is going up
                    # they move in the same direction
                    else:
                        uDY = self.deltaY
                    # if seb is going right, ursula moves in same dir
                    if self.deltaX > 0 and self.ursulaX < self.SebastianX:
                        uDX = self.deltaX
                    # if ursula passes seb, reverses dir to follow him
                    elif self.deltaX > 0 and self.ursulaX > self.SebastianX:
                        uDX = self.deltaX * -1
                    # if seb is going left, ursula moves in same dir
                    elif self.deltaX < 0 and self.ursulaX < self.SebastianX:
                        uDX = self.deltaX * -1
                    # if ursula passes seb(going left), reverses dir to follow
                    else:
                        uDX = self.deltaX
                    # moves ursulas x and y pos based on vector movement
                    # ursula moves slower than sebastian
                    ursulaSpeedFactor = self.speedFactor / 2
                    self.ursulaX += ursulaSpeedFactor * uDX
                    self.ursulaY += ursulaSpeedFactor * uDY
                # makes ursula bounce against the edges of screen
                else:
                    ursulaSpeedFactor = self.speedFactor/2
                    uDX = -1 * self.deltaX
                    uDY = self.deltaY
                    self.ursulaX += ursulaSpeedFactor * uDX
                    self.ursulaY += ursulaSpeedFactor * uDY

    def moveSebastian(self):
        if not self.gameOver:
            if self.deltaX != None and self.deltaY != None:
                # if sebastian is within the left screen, moves by the vector
                if ((self.SebastianX - self.SebastianR + 10 * self.deltaX >= 0) 
                    and ((self.SebastianX + self.SebastianR + 10 * self.deltaX)
                     <= (self.width/2))):
                    self.SebastianX += self.speedFactor * self.deltaX
                    self.SebastianY += self.speedFactor * self.deltaY
                else:
                    # makes sebastian bounce against the walls
                    self.deltaX *= -1
                    self.SebastianX += self.speedFactor * self.deltaX
                    self.SebastianY += self.speedFactor * self.deltaY

    def onTimerFired(self):
            self.moveUrsula()
            self.moveSebastian()
            if not self.gameOver:
                if self.deltaY != None:
                    # score increases when seb moves forward
                    self.currentScore -= self.deltaY
                    if self.currentScore < 0:
                        self.currentScore = 0
                # makes the scorpions shoot up
                for scorp in self.scorpionList:
                    scorp.y -= 30
            # once the Sebastian reaches the end of the screen, wraps around
            if self.SebastianY + 2 * self.SebastianR <= 0:
                # distinguishes between moving to new path and moving down bc
                # of a vector pointing down
                self.newPath = True
                self.SebastianY = self.height
                self.clamList = self.makeclamList()
                # draws a new flounder on the new screen if he has been caught
                if self.flounderCaught:
                    self.drawRandomFlounder()
                    self.flounderCaught = False
            # if seb is not going on new path and reaches end of screen
            # makes sure he doesn't go farther down
            if ((self.SebastianY+self.SebastianR >= self.height) and 
                (not self.newPath)):
                self.SebastianY = self.height-self.SebastianR
            # makes sure ursula stays on screen
            if ((self.ursulaY+self.ursulaR >= self.height) or 
                (self.ursulaY-self.ursulaR <= 0)):
                if self.deltaX != None and self.deltaY != None:
                    uDy = self.deltaY * -1
                    self.ursulaY += self.speedFactor * uDy
            # increases number of clams as score increases
            self.numOfclams = 5 + int(self.currentScore / 50)
            self.newPath = False

# EVENT HANDLERS

    # determines if a location has been clicked
    def isClicked(self,clickx,clicky,x0,y0,x1,y1):
        if clickx > x0 and clickx < x1:
                if clicky > y0 and clicky < y1:
                    return True
        return False

    def onKeyPressed(self,event):
        if event.keysym == "Left":
            # makes sure the Sebastian stays on the screen
            if self.SebastianX - 1.5 *self.SebastianR > 0:
                self.SebastianX -= 20
        elif event.keysym == "Right":
            # so Sebastian stays on screen
            if self.SebastianX + 1.5 * self.SebastianR < self.width/2:
                self.SebastianX += 20
        # restart game
        elif event.keysym == "r":
            self.initAnimation()
        # start the game
        elif event.keysym == "s":
            self.splashScreen = False

    def onMouseMotion(self,event):
        # changes the text color of buttons if moused over
        self.startColor,self.helpColor = "black","black"
        self.backColor,self.restartColor = "black","black"
        self.motionX,self.motionY = event.x,event.y
        if self.isClicked(self.motionX,self.motionY,
            self.startButtonX0,self.startButtonY0,
            self.startButtonX1,self.startButtonY1):
            self.startColor = "white"
        elif self.isClicked(self.motionX, self.motionY,
            self.helpButtonX0,self.helpButtonY0,
            self.helpButtonX1,self.helpButtonY1):
            self.helpColor = "white"
        elif self.isClicked(self.motionX,self.motionY,
            self.backX0,self.backY0,self.backX1,
            self.backY1):
            self.backColor = "white"
        elif self.isClicked(self.motionX,self.motionY,
            self.restartX0,self.restartY0,
            self.restartX1,self.restartY1):
            self.restartColor = "white"

    # B1-Motion event handler
    # deals with mouse dragging
    def leftMousePressed(self,event):
        self.mouseX,self.mouseY = event.x,event.y
        # adds all the pixels that mouse dragged over
        if self.mouseX != None and self.mouseY != None:
            if self.inBlackScreen(self.mouseX,self.mouseY):
                    p = Pixel(self.mouseX,self.mouseY)
                    self.pixelList.append(p)


    def leftMouseReleased(self,event):
        self.mouseRX,self.mouseRY = event.x,event.y
        self.createPixelLists()
        # checks if circle drawn after released
        if self.checkInCircle():
            self.isCircle = True
        self.calculateDeltaMovement()


    def onMousePressed(self,event):
        self.clickX,self.clickY = event.x,event.y
        self.clickonButtons()
    
# BUTTONS AND OTHER SCREEN STUFF

    # makes sure drawing is within black screen
    def inBlackScreen(self,x,y):
        if x <= self.width and x >= self.width/2:
            if ((y <= self.height) and 
                (y >= self.height * self.screenScaleFactor)):
                return True
        return False

    # creates initial splash screen
    def drawSplashScreen(self):
        self.background = PhotoImage(file ="background_.gif")
        self.canvas.create_image(self.width/2,self.height/2,
            image = self.background)
        self.canvas.create_text(self.width/2,self.height/4,
            text = "Under the Sea",font = "BritannicBold 76")
        self.canvas.create_text(self.width/2,3*self.height/4,
            text = "Namrita Murali",font = "BritannicBold 24",
            fill = "black")
        self.drawSplashScreenButtons()

    # next 3 functions make splash screen buttons
    def drawStartButton(self): 
        x0,y0 = self.startButtonX0,self.startButtonY0
        x1,y1 = self.startButtonX1,self.startButtonY1
        midX,midY = (x0+x1)/2,(y0+y1)/2
        self.canvas.create_rectangle(x0,y0,x1,y1,
            fill = "turquoise",width = 3)
        self.canvas.create_text(midX,midY,
            font = "BritannicBold 24",text = "Start",
            fill = self.startColor)

    def drawHelpButton(self):
        x0,y0 = self.helpButtonX0,self.helpButtonY0
        x1,y1 = self.helpButtonX1,self.helpButtonY1
        midX,midY = (x0+x1)/2,(y0+y1)/2
        self.canvas.create_rectangle(x0,y0,x1,y1,
            fill = "turquoise",width = 3)
        self.canvas.create_text(midX,midY,
            font = "BritannicBold 24",
            text = "Help",fill = self.helpColor)

    def drawSplashScreenButtons(self):
        self.drawStartButton()
        self.drawHelpButton()

    def clickonButtons(self):
        if self.splashScreen:
            # checks if start button is clicked
            if self.isClicked(self.clickX,self.clickY,
                self.startButtonX0,self.startButtonY0,
                self.startButtonX1,self.startButtonY1):
                self.splashScreen = False
                self.helpScreen = False
            # checks if help button is clicked
            elif self.isClicked(self.clickX, self.clickY,
                self.helpButtonX0,self.helpButtonY0,
                self.helpButtonX1,self.helpButtonY1):
                self.splashScreen = False
                self.helpScreen = True
        elif self.helpScreen:
            # checks if back button is clicked on help screen
            if self.isClicked(self.motionX,self.motionY,
                self.backX0,self.backY0,self.backX1,
                self.backY1):
                self.splashScreen = True
                self.helpScreen = False
        elif self.gameOver:
            # checks if restart buttons is clicked on game over screen
            if self.isClicked(self.motionX,self.motionY,
                self.restartX0,self.restartY0,
                self.restartX1,self.restartY1):
                self.initAnimation()

    
    def divideScreen(self):
        # creates line that divides screen in half
        self.canvas.create_line(self.width/2,0,self.width/2,self.height)
        # makes the right half of the screen black
        self.canvas.create_rectangle(self.width/2,0,self.width,self.height,
            fill = "black")
        # divides the black part in half too
        self.canvas.create_line(self.width/2,self.height*self.screenScaleFactor,
            self.width,self.height*self.screenScaleFactor,fill = "blue")
        # creates drawing part text
        self.drawBoxText()

    # creates background of actual game
    def drawBackground(self):
        self.gameBackground = PhotoImage(file = "game background.gif")
        self.canvas.create_image(self.width/2,self.height/2,
            image = self.gameBackground)

    # creates text for black side of screen
    def drawBoxText(self):
        self.canvas.create_text((self.width/2+self.width)/2,
            self.height*self.screenScaleFactor/2,
            text = "Score: %d" % self.currentScore,
            fill = "white",font = "BritannicBold 24")
        self.canvas.create_text((self.width/2+self.width)/2,
            self.height*self.screenScaleFactor/4,
            text = "High Score: %d" % self.highScore,
            fill = "white",font = "BritannicBold 24")
        self.canvas.create_text((self.width/2+self.width)/2,
            self.height*1.1*self.screenScaleFactor,
            text = "Draw Here:",
            fill = "white",font = "BritannicBold 24")

    # draws restart button in game over screen
    def drawRestartButton(self):
        x0,y0 = self.restartX0,self.restartY0
        x1,y1 = self.restartX1,self.restartY1
        midX,midY = (x0+x1)/2,(y0+y1)/2
        self.canvas.create_rectangle(x0,y0,x1,y1,
            fill = "turquoise",width = 3)
        self.canvas.create_text(midX,midY,
            font = "BritannicBold 24",
            text = "Restart",fill = self.restartColor)


    def drawHelpScreen(self):
        self.canvas.create_image(self.width/2,self.height/2,
            image = self.background)
        self.canvas.create_text(self.width/2,self.height/16, text = 
"""How to Play""",font = "BritannicBold 40 bold")
        self.canvas.create_text(self.width/2,self.height/2, text = 
"""
Help Sebastian save Flounder and avoid Ursula!

Use the drawing pad to direct what Sebastian does. 

If you draw a line, Sebastian will move in the 
direction of that line.

If you draw a circle, Sebastian will shoot.

Scorpions eat clams, so shoot scorpions
at clams to remove them from your path.

If you shoot a scorpion at Ursula, she will get
annoyed and move to another location.

If you hit the clams along the way, Sebastian will die.

If you come in contact with Flounder, you will save him
and win more points.

See how far through the sea you can get!

Have fun!!""", font = "BritannicBold 26", justify = CENTER)
        # draws back button in help screen 
        self.drawBackButton()

    def drawBackButton(self):
        x0,y0 = self.backX0,self.backY0
        x1,y1 = self.backX1,self.backY1
        midX,midY = (x0+x1)/2,(y0+y1)/2
        self.canvas.create_rectangle(x0,y0,x1,y1,
            fill = "turquoise",width = 3)
        self.canvas.create_text(midX,midY,
            font = "BritannicBold 24",
            text = "Back",fill = self.backColor)


# HIGH SCORE
    
    # lines 702-710 taken from week 11 file i/o course notes
    def readFile(self,filename, mode="rt"):
        # rt = "read text"
        with open(filename, mode) as fin:
            return fin.read()

    def writeFile(self,filename, contents, mode="wt"):
        # wt = "write text"
        with open(filename, mode) as fout:
            fout.write(contents)

    # modified from my own hw10 lines 141-147
    def highScoreFromFile(self):
        try: 
            scores = self.readFile("UnderTheSeaHighScore.txt")
            return int(float(scores))
        except: 
            return 0

    def redrawAll(self):
        self.canvas.delete(ALL)
        if self.gameOver == True:
            self.canvas.create_rectangle(0,0,self.width,
                self.height,fill="dodgerblue")
            self.divideScreen()
            self.canvas.create_text(self.width/4,self.height/2,
                text = "GAME OVER",font = "BritannicBold 40",
                fill = "white")
            self.drawRestartButton()
            # modified from my hw10 lines 225-228
            if self.currentScore > self.highScore:
                self.highScore = self.currentScore
                self.writeFile("UnderTheSeaHighScore.txt",str(self.highScore))
        elif self.splashScreen == True:
            self.drawSplashScreen()
        elif self.helpScreen == True:
            self.drawHelpScreen()
        else:
            self.drawBackground()
            self.divideScreen()
            self.drawSebastian()
            self.drawclams()
            self.drawOnBlackScreen()
            # changes ursula's position if she has been hit by scorp
            if not self.ursulaDies:
                self.drawUrsula()
            else:
                self.drawRandomUrsula()
                self.ursulaDies = False
            # only draw flounder if he's not caught
            if not self.flounderCaught:
                self.drawFlounder()
            # only draws scorpions if circle has been drawn
            if len(self.scorpionList) > 0:
                self.shoot()

termproj = UnderTheSea()
termproj.run()
