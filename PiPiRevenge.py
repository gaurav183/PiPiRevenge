from Tkinter import *
from eventBasedAnimationClass import EventBasedAnimationClass
import random
import math


class PiPiRevenge(EventBasedAnimationClass):
    def __init__(self):
        super(PiPiRevenge, self).__init__(600,800)
        
    def initAnimation(self):
        self.isMainScreen = True 
        self.isSplashScreen = False 
        self.isHelpScreen = False
        self.timerDelay = 75
        self.startButtonX0,self.startButtonY0 = self.width/2-80,self.height/2.5
        self.startButtonX1 = self.width/2+80
        self.startButtonY1 = self.startButtonY0 + 70
        self.initPositions()


    # all objects are treated as circles for collision detection
    def initPositions(self):
        self.redPlanetX = self.width/4
        self.redPlanetY = 7*self.height/8
        self.redPlanetR = 50
        self.bluePlanetX = self.width/2
        self.bluePlanetY = 7*self.height/8
        self.bluePlanetR = 50
        self.goldPlanetX = 3*self.width/4
        self.goldPlanetY = 7*self.height/4
        self.goldPlanetR = 50
        self.asteroid1X = self.width/4
        self.asteroid1Y = self.height/12
        self.asteroid2X = self.width/2
        self.asteroid2Y = self.height/12
        self.asteroid3X = 3*self.width/4
        self.asteroid3Y = self.height/12
        self.asteroidR = 30
        
    def drawSplashScreen(self):
        self.background = PhotoImage(file = "images/splashScreen.gif")
        self.canvas.create_image(self.width/2, self.height/2, image = self.background)
        self.canvas.create_text(self.width/2, self.height/4, text="Pi Pi Revenge", font="Lato 76", fill="white")
        self.drawSplashScreenButtons()

    def drawSplashScreenButtons(self):
        self.drawStartButton()
        #self.drawHelpButton()
    
    def drawMainScreen(self):
        self.background = PhotoImage(file = "images/splashScreen.gif")
        self.redPlanet = PhotoImage(file = "images/redplanet.gif")
        self.goldPlanet = PhotoImage(file = "images/goldplanet.gif")
        self.bluePlanet = PhotoImage(file = "images/blueplanet.gif")
        self.canvas.create_image(self.width/2, self.height/2, image = self.background)
        self.canvas.create_image((self.width/4), (7*self.height/8), image = self.redPlanet)
        self.canvas.create_image((2*self.width/4), (7*self.height/8), image = self.goldPlanet)
        self.canvas.create_image((3*self.width/4), (7*self.height/8), image = self.bluePlanet)
        self.drawAsteroids()
    
    def onTimerFired(self):
        self.asteroid1Y += random.randint(0,65)
        self.asteroid2Y += random.randint(0,65)
        self.asteroid3Y += random.randint(0,65)
        if (self.asteroid1Y >= (7*self.height/8)):
          self.asteroid1Y = self.height/12
        if (self.asteroid2Y >= (7*self.height/8)):
          self.asteroid2Y = self.height/12
        if (self.asteroid3Y >= (7*self.height/8)):
          self.asteroid3Y = self.height/12

    def drawAsteroids(self):
        self.asteroid = PhotoImage(file = "images/asteroid.gif")
        self.canvas.create_image(self.asteroid1X, self.asteroid1Y, image = self.asteroid)
        self.canvas.create_image(self.asteroid2X, self.asteroid2Y, image = self.asteroid)
        self.canvas.create_image(self.asteroid3X, self.asteroid3Y, image = self.asteroid)

    def drawStartButton(self):
        x0,y0 = self.startButtonX0,self.startButtonY0
        x1,y1 = self.startButtonX1,self.startButtonY1
        midX,midY = (x0+x1)/2,(y0+y1)/2
        self.canvas.create_rectangle(x0,y0,x1,y1,
            fill = "midnight blue",width = 3)
        self.canvas.create_text(midX,midY,
            font = "Lato 24",text = "Start",fill = "white")

    def redrawAll(self):
        self.canvas.delete(ALL)
        if self.isSplashScreen:
          self.drawSplashScreen()
        elif self.isMainScreen:
           self.drawMainScreen()

pipirevenge = PiPiRevenge()
pipirevenge.run()
