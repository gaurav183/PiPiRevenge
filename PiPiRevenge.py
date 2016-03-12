from Tkinter import *
from eventBasedAnimationClass import EventBasedAnimationClass
import random
import math

def distance(self,x0,y0,x1,y1):
  return ((x0-x1)**2+(y0-y1)**2)**0.5
    
def almostEqual(a,b,epsilon = 10*10**-6):
  return abs(a - b) < epsilon
   
def inCircle(x,y,cx,cy,r):
  return UnderTheSea.almostEqual(float(((x-cx)**2+(y-cy)**2)**0.5),
          float(r))

class PiPiRevenge(EventBasedAnimationClass):
    def __init__(self):
        super(PiPiRevenge, self).__init__(600,800)
        
    def initAnimation(self):
        self.isMainScreen = True 
        self.isSplashScreen = False 
        self.isHelpScreen = False
        self.timerDelay = 50
        self.startButtonX0,self.startButtonY0 = self.width/2-80,self.height/2.5
        self.startButtonX1 = self.width/2+80
        self.startButtonY1 = self.startButtonY0 + 70
        self.initPositions()
    
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
        self.randSpeed1 = random.randint(5,30)
        self.randSpeed2 = random.randint(5,30)
        self.randSpeed3 = random.randint(5,30)
        self.redPlanet = PhotoImage(file = "images/redplanet.gif")
        self.goldPlanet = PhotoImage(file = "images/goldplanet.gif")
        self.bluePlanet = PhotoImage(file = "images/blueplanet.gif")
         
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
        self.canvas.create_image(self.width/2, self.height/2, image = self.background)
        self.canvas.create_image((self.width/4), (7*self.height/8), image = self.redPlanet)
        self.canvas.create_image((2*self.width/4), (7*self.height/8), image = self.goldPlanet)
        self.canvas.create_image((3*self.width/4), (7*self.height/8), image = self.bluePlanet)
        self.drawAsteroids()
    
    def onTimerFired(self): 
        self.redPlanet = PhotoImage(file = "images/redplanet.gif")
        self.goldPlanet = PhotoImage(file = "images/goldplanet.gif")
        self.bluePlanet = PhotoImage(file = "images/blueplanet.gif")
        self.asteroid1Y += self.randSpeed1
        self.asteroid2Y += self.randSpeed2
        self.asteroid3Y += self.randSpeed3
        if (self.asteroid1Y >= (7*self.height/8)):
          self.asteroid1Y = self.height/12
          self.randSpeed1 = random.randint(5,30)
          self.redPlanet = PhotoImage(file = "images/redplanethighlight.gif")
        if (self.asteroid2Y >= (7*self.height/8)):
          self.asteroid2Y = self.height/12
          self.goldPlanet = PhotoImage(file = "images/goldplanethighlight.gif")
          self.randSpeed2 = random.randint(5,30)
        if (self.asteroid3Y >= (7*self.height/8)):
          self.asteroid3Y = self.height/12
          self.randSpeed3 = random.randint(5,30)
          self.bluePlanet = PhotoImage(file = "images/blueplanethighlight.gif")

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
  
    def redPlanetCollision(self):
        x = self.redPlanetX
        y = self.redPlanetY
        r = self.redPlanetR
        cx = self.asteroid1X
        cy = self.asteroid1Y
        cr = self.asteroidR
        if ((cx-x)**2+(cy-y)**2)**0.5 <= (cr + r):
           self.canvas.create_text(self.width/2, self.height/2, "red planet")

    def bluePlanetCollision(self):
        x = self.bluePlanetX
        y = self.bluePlanetY
        r = self.bluePlanetR
        cx = self.asteroid2X
        cy = self.asteroid2Y
        cr = self.asteroidR
        if ((cx-x)**2+(cy-y)**2)**0.5 <= (cr + r):
            self.canvas.create_text(self.width/2, self.height/2, "blue planet")
    
    def goldPlanetCollision(self):
        x = self.goldPlanetX
        y = self.goldPlanetY
        r = self.goldPlanetR
        cx = self.asteroid3X
        cy = self.asteroid3Y
        cr = self.asteroidR
        if ((cx-x)**2+(cy-y)**2)**0.5 <= (cr + r):
            self.canvas.create_text(self.width/2, self.height/2, "gold planet")

    def redrawAll(self):
        self.canvas.delete(ALL)
        if self.isSplashScreen:
          self.drawSplashScreen()
        elif self.isMainScreen:
           self.drawMainScreen()

pipirevenge = PiPiRevenge()
pipirevenge.run()
