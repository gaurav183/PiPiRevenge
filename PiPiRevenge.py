from Tkinter import *
from eventBasedAnimationClass import EventBasedAnimationClass
import random
import math


class PiPiRevenge(EventBasedAnimationClass):
    def __init__(self):
        super(PiPiRevenge, self).__init__(600,800)
        
    def initAnimation(self):
        self.isBackground = False
        self.isSplashScreen = True
        self.isHelpScreen = False
        self.timerDelay = 75
    
    def drawSplashScreen(self):
        self.background = PhotoImage(file = "images/splashScreen.gif")
        self.canvas.create_image(self.width/2, self.height/2, image = self.background)
        
    def redrawAll(self):
        self.canvas.delete(ALL)
        if self.isSplashScreen:
          self.drawSplashScreen()

pipirevenge = PiPiRevenge()
pipirevenge.run()
