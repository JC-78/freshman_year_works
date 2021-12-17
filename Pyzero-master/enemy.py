import pygame,math,random,time,os
from random import randrange
from asteroid import *
from bullet import *

pygame.display.init()

WHITE=(255,255,255)

window_height=750

class Enemy(pygame.sprite.Sprite):  #Normal enemy that flies downward while shooting bullets
    def __init__(self, width, height):
        pygame.sprite.Sprite.__init__(self)
        enemy_image = pygame.image.load("sprite_collection/enemy1.png").convert_alpha() #Citation:https://www.pngocean.com/gratis-png-clipart-zvlub
        enemy_image = pygame.transform.scale(enemy_image,(50,50))
        enemy_image.set_colorkey(WHITE)
        self.width=width
        self.height=height
        self.image=enemy_image
        self.rect=self.image.get_rect()

    def update(self):
        self.rect.y+=5
        if(self.rect.y>=window_height):
            self.rect.y=10
    
    def display(self,screen,x,y):
        screen.blit(self.image,(x,y))

    def shoot(self,x,y):
        bullet = EnemyBullet(1)
        bullet.rect.x = x-40
        bullet.rect.y = y-40
        return bullet

class Rainer(Enemy):  #Enemy that moves left right while shooting bullets
    def __init__(self,width,height):
        pygame.sprite.Sprite.__init__(self)
        super().__init__(width,height)
        enemy_image = pygame.image.load("sprite_collection/Rainer.png").convert_alpha() #Citation:https://www.pinterest.com/pin/546765211005668669/?lp=true
        enemy_image = pygame.transform.scale(enemy_image,(70,70))
        enemy_image.set_colorkey(WHITE)
        self.image=enemy_image
        self.rect=self.image.get_rect()
        self.sign=1

    def update(self):
        self.rect.x+=(15*self.sign)
        if(self.rect.x>=570):
            self.sign*=-1
        if (self.rect.x<=0):
            self.sign*=-1

class Kamikaze(Enemy): #Enemy that flies downward while creating lines of bullets at its sides
    def __init__(self,width,height):
        pygame.sprite.Sprite.__init__(self)
        super().__init__(width,height)
        enemy_image = pygame.image.load("sprite_collection/kamikaze.png").convert_alpha() #Citation:https://www.pngfly.com/png-sw1mwd/
        enemy_image = pygame.transform.scale(enemy_image,(30,30))
        enemy_image.set_colorkey(WHITE)
        self.image=enemy_image
        self.rect=self.image.get_rect()
        self.speed=5

    def update(self):
        self.rect.y+=20
        if(self.rect.y>=window_height):
            self.rect.y=10
       
class Midboss(Enemy):
    def __init__(self,width,height,level):
        pygame.sprite.Sprite.__init__(self)
        super().__init__(width,height)
        enemy_image = pygame.image.load("sprite_collection/midboss.png").convert_alpha() #Citation:https://www.pngkit.com/view/u2e6a9i1w7a9o0y3_image-starship-sprites-starship-sprites/
        enemy_image = pygame.transform.scale(enemy_image,(80,80))
        enemy_image.set_colorkey(WHITE)
        self.image=enemy_image
        self.rect=self.image.get_rect()
        self.signX=1
        self.signY=1
        self.health=450+50*level
        self.value=self.health

    def update(self): #bounce around
        self.rect.x+=(15*self.signX)
        self.rect.y+=(20*self.signY)
        if(self.rect.x>=570):
            self.signX*=-1
        if (self.rect.x<=0):
            self.signX*=-1
        if (self.rect.y>=750):
            self.signY*=-1
        if (self.rect.y<=0):
            self.signY*=-1
            
    def shoot(self,x,y):
        bullet = Tracer()
        bullet.rect.x = x-40
        bullet.rect.y = y-40
        return bullet

class Boss(Enemy):
    def __init__(self,width,height,level):
        pygame.sprite.Sprite.__init__(self)
        super().__init__(width,height)
        enemy_image = pygame.image.load("sprite_collection/boss.png").convert_alpha() #Citation:https://www.realpng.com/fundo-transparente-png-clipart-lhcys
        enemy_image = pygame.transform.scale(enemy_image,(150,150))
        enemy_image.set_colorkey(WHITE)
        self.image=enemy_image
        self.rect=self.image.get_rect()
        self.health=2000+100*level
        self.value=self.health
        self.signX=1
        self.signY=1
        self.bulletGoDown=1
        
    def update(self): 
        if ((0.8*self.value)<=self.health<=self.value): #Move left right
            self.rect.x+=(15*self.signX)
            if(self.rect.x>=570):
                self.signX*=-1
            if (self.rect.x<=0):
                self.signX*=-1
        elif ((0.45*self.value)<=self.health<=(0.8*self.value)): #Float around
            self.rect.x+=(10*self.signX)
            self.rect.y+=(15*self.signY)
            if(self.rect.x>=570):
                self.signX*=-1
            if (self.rect.x<=0):
                self.signX*=-1
            if (self.rect.y>=750):
                self.signY*=-1
                self.bulletGoDown=-1
            if (self.rect.y<=0):
                self.signY*=-1
                self.bulletGoDown=1

        elif ((0.25*self.value)<=self.health<=(0.45*self.value)): #Combine three movement patterns to create teleportation effect
            rand=random.randint(1,3)
            if rand==1:   #moving vertically down and restationing at top
                self.rect.y+=40
                if(self.rect.y>=window_height):
                    self.rect.y=10
                    self.rect.x=random.randrange(50,570-50)
            elif rand==2: #moving left to right from random height and restationing at top
                self.rect.x-=50
                self.rect.y=random.randrange(50,750-20)
                while self.rect.x<=570:
                    self.rect.x+=50
                self.rect.y=10
                self.rect.x=random.randrange(50,570-50)
            elif rand==3: #moving left to right from random height and restationing at top
                self.rect.x=620
                self.rect.y=random.randrange(50,750-20)
                while self.rect.x>=(-10):
                    self.rect.x-=50
                self.rect.y=10
                self.rect.x=random.randrange(50,570-50)
        
        elif (0<self.health<(0.25*self.value)): #move left to right at top, and right to left at bottom
            self.rect.x+=(20*self.signX)
            if(self.rect.x>=570):
                self.signX*=-1
                self.rect.y=700
                self.bulletGoDown=-1
            if (self.rect.x<=0):
                self.signX*=-1
                self.rect.y=30
                self.bulletGoDown=1

    
    def shootN(self,sx,sy):  #shoot normal bullet
        bullet = EnemyBullet(self.bulletGoDown)
        bullet.rect.x = sx-40
        bullet.rect.y = sy-40
        return bullet
        
    def shootT(self,sx,sy): #shoot tracer bullet
        bullet = Tracer()
        bullet.rect.x = sx
        bullet.rect.y = sy
        return bullet    
    
    def shootC(self,sx,sy,angle,px,py): #shoot the bullet-sphere. The sphere of 12 red bullets
        bullet=BulletSphere(sx,sy,angle,px,py)
        bullet.rect.x=sx
        bullet.rect.y=sy
        return bullet

    def shootF(self,sx,sy): #shoot fractal bullet
        bullet=fractalBullet(sx,sy,2) #can control fractal level here through the third argument
        return bullet

    def shootP(self,sx,sy,playerDirectionX,playerDirectionY):  #shoot predicting Bullet
        bullet = predictingBullet(playerDirectionX,playerDirectionY)
        bullet.rect.x = sx-40
        bullet.rect.y = sy-40
        return bullet    
