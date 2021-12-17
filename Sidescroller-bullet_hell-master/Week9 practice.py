
from cmu_112_graphics import *
from tkinter import *

# SideScroller1:

from cmu_112_graphics import *
from tkinter import *
import random

class SideScroller1(App):
    def appStarted(self):
        self.scrollX = 0
        self.scrollY = 0
        url = 'post-304010-13437164422024.png'
        spritestrip = self.loadImage(url)
        self.sprites = [ ]
        for i in range(14):
            sprite = spritestrip.crop((20+260*i, 10, 120+260*i, 520))
            self.sprites.append(sprite)
        self.spriteCounter = 0

    def timerFired(self):
        self.spriteCounter = (1 + self.spriteCounter) % len(self.sprites)

    def keyPressed(self, event):
        if (event.key == "Left"):    self.scrollX -= 5
        elif (event.key == "Right"): self.scrollX += 5
        elif (event.key == "Up"): self.scrollY -=5
        elif (event.key == "Down"): self.scrollY +=5

    def redrawAll(self, canvas):
        """
        self.img = ImageTk.PhotoImage(Image.open("ball.126274-nature-landscape\
            -sky-hill-grass-field-clouds-Windows_XP-748x468.png"))     
        self.canvas.create_image(self.width/2,self.height/2,image=self.img)   
        """
        # draw the player fixed to the center of the scrolled canvas
        sprite = self.sprites[self.spriteCounter]
        canvas.create_image(self.scrollX,self.scrollY, \
            image=ImageTk.PhotoImage(sprite))

        x = self.width/2 - self.scrollX # <-- This is where we scroll the axis!
        y = self.height/2 - self.scrollY
        
        # draw the instructions and the current scrollX
        x = self.width/2
        canvas.create_text(x, 20, text='Use arrows to move\
        left,right,up and down')
        canvas.create_text(x, 40, text=f'Distance to the goal\
             = {self.width-self.scrollX}')

SideScroller1(width=1000, height=700)





"""
class player(object):
    def __init__(self):
        self.health=100
        self.power=30
        self.speed=10
        self.question=[]

    def attack(self):

class monster(object):
    def __init__(self,health,strength,power,speed,size)
        self.health=health
        self.strength=strength
        self.power=power
        self.speed=speed
        
    def attacked(self,strength):
        if self.health>0:
            return self.strength

    def lifeLeft(self,damage):
        self.health -= damage

class TA(monster):
    def __init__(self):
        super().__init__(health,strength,power,speed,size)


class Taylor(monster):
    def __init__(self):
        super().__init__(health,strength,power,speed,size)
        self.health*=2
        self.strength*=2
        self.power*=2
        self.speed*=2
        self.size*=2

class Kosbie(monster):
    def __init__(self):
        super().__init__(health,strength,power,speed,size)
        self.health*=10
        self.strength*=10
        self.power*=10
        self.speed*=10
        self.size*=10


class Bullet(object):
    def __init__(self, start_x, start_y, dest_x, dest_y):
        self.start_x=start_x
        self.start_y=start_y
        self.dest_x=dest_x
        self.dest_y=dest_y
        
        # Set up the image for the bullet
        self.image = #Different 

        # Calculation the angle in radians between the start points
        # and end points. This is the angle the bullet will travel.
        x_diff = dest_x - start_x
        y_diff = dest_y - start_y
        angle = math.atan2(y_diff, x_diff);

        # Taking into account the angle, calculate our change_x
        # and change_y. Velocity is how fast the bullet travels.
        velocity = 5
        self.change_x = math.cos(angle) * velocity
        self.change_y = math.sin(angle) * velocity

        self.floating_point_x = start_x
        self.floating_point_y = start_y

        

    def update(self): #move the bullet
        # The floating point x and y hold our more accurate location.
        self.floating_point_y += self.change_y
        self.floating_point_x += self.change_x

        # The rect.x and rect.y are converted to integers.
        self.rect.y = int(self.floating_point_y)
        self.rect.x = int(self.floating_point_x)

        # If the bullet flies of the screen, get rid of it.
        if self.rect.x < 0 or self.rect.x > self.width or self.rect.y < 0 or \
            self.rect.y > self.height:
            #disappears



class SideScroller(App):
"""



"""
class SplashScreenMode(Mode):
    def redrawAll(mode, canvas):
        font = 'Arial 26 bold'
        canvas.create_text(mode.width/2, 150, \
            text='Welcome to 112 survival!',font=font)
        canvas.create_text(mode.width/2, 200, \
            text='Make your way through the monsters and beat the boss at the \
                end of the road to win', font=font)
        canvas.create_text(mode.width/2, 250, \
            text='Press any key for the game!', font=font)

    def keyPressed(mode, event):
        mode.app.setActiveMode(mode.app.gameMode)

class HelpMode(Mode):
    def redrawAll(mode, canvas):
        font = 'Arial 26 bold'
        canvas.create_text(mode.width/2, 150, \
            text='This is the help screen!', font=font)
        canvas.create_text(mode.width/2, 250, \
            text='Use arrow keys to move; click on the monsters to kill them\
                 while dodging their attacks. Get to the end and kill the boss\
                to win. Try not to die before reaching the end of 112. Yeet.\
            ', font=font)
        canvas.create_text(mode.width/2, 350, \
            text='Press any key to return to the game!', font=font)

    def keyPressed(mode, event):
        mode.app.setActiveMode(mode.app.gameMode)

class GameMode(Mode):

class MyModalApp(ModalApp):
    def appStarted(app):
        app.splashScreenMode = SplashScreenMode()
        app.gameMode = GameMode()
        app.helpMode = HelpMode()
        app.setActiveMode(app.splashScreenMode)
        app.timerDelay = 50

app = MyModalApp(width=500, height=500)
"""