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

    def drawSplashScreen(self):
        self.background = PhotoImage(file = "images/splashScreen.gif")
        self.canvas.create_image(self.width/2, self.height/2, image = self.background)
        self.canvas.create_text(self.width/2, self.height/4, text="Pi Pi Revenge", font="BritannicBold 76", fill="white")
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
    def drawStartButton(self):
        x0,y0 = self.startButtonX0,self.startButtonY0
        x1,y1 = self.startButtonX1,self.startButtonY1
        midX,midY = (x0+x1)/2,(y0+y1)/2
        self.canvas.create_rectangle(x0,y0,x1,y1,
            fill = "midnight blue",width = 3)
        self.canvas.create_text(midX,midY,
            font = "BritannicBold 24",text = "Start",fill = "white")

    def redrawAll(self):
        self.canvas.delete(ALL)
        if self.isSplashScreen:
          self.drawSplashScreen()
        elif self.isMainScreen:
           self.drawMainScreen()

pipirevenge = PiPiRevenge()
pipirevenge.run()
