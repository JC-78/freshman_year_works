import pygame,math,random,time,os
from random import randrange

pygame.display.init()

WHITE=(255,255,255)
BLACK=(0,0,0)

class Bullet(pygame.sprite.Sprite): #player bullet
    def __init__(self,pos,angle):
        pygame.sprite.Sprite.__init__(self)
        bullet_image=pygame.image.load("ammo/player_bullet.png").convert_alpha() #Citation: https://www.shutterstock.com/video/clip-12261347-abstract-fractal-disco-ball-animated-on-black
        bullet_image=pygame.transform.scale(bullet_image,(20,20))
        self.image=bullet_image
        self.rect = self.image.get_rect() 
        self.pos=pos
        self.angle=angle
        
    def update(self): #updating bullet direction depending on the player's direction
        self.pos=(self.pos[0]+10*math.cos(math.radians(self.angle)),self.pos[1]-10*math.sin(math.radians(self.angle)))
        self.rect.x+=(10*math.cos(math.radians(self.angle)))
        self.rect.y-=(10*math.sin(math.radians(self.angle)))

    def display(self,screen,x,y):
        screen.blit(self.image,(x,y))

class EnemyBullet(Bullet): #Normal enemy bullet
    def __init__(self,bulletGoDown):
        pygame.sprite.Sprite.__init__(self)
        bullet_image=pygame.image.load("ammo/red_beam.png").convert_alpha() #Citation:https://www.shutterstock.com/video/clip-33970345-animation-laser-beam-on-black-background-alpha
        bullet_image=pygame.transform.scale(bullet_image,(20,20))
        self.image=bullet_image
        self.image.set_colorkey(BLACK)
        self.rect = self.image.get_rect()
        self.bulletGoDown=bulletGoDown
        
    def update(self):
        self.rect.y+=(10*self.bulletGoDown)

class fractalBullet(Bullet):
    def __init__(self,xc,yc,level):
        pygame.sprite.Sprite.__init__(self)
        bullet_image=pygame.image.load("ammo/fractalBullet.png").convert_alpha() #citation:http://tuscriaturas.blogia.com/2019/junio.php
        self.x=20
        self.y=20
        bullet_image=pygame.transform.scale(bullet_image,(self.x,self.y))
        self.image=bullet_image
        self.image.set_colorkey(BLACK)
        self.rect = self.image.get_rect()
        self.xc=xc
        self.yc=yc
        self.rect.x=xc
        self.rect.y=yc
        self.level=level
        
    def update(self): 
        if self.x<=110 and self.y<=110 and self.level>0:
            self.x+=4
            self.y+=4
            bullet_image=pygame.transform.scale(self.image,(self.x,self.y))
            self.image=bullet_image
            self.image.set_colorkey(BLACK)
            self.rect.x+=6
            self.rect.y+=6
            self.rect.width+=6
        self.rect.y+=3
         
    def display(self,screen,x,y):
        screen.blit(self.image,(x,y))

class BulletSphere(Bullet): 
    def __init__(self,sx,sy,angle,px,py):
        pygame.sprite.Sprite.__init__(self)
        bullet_image=pygame.image.load("ammo/red_beam.png").convert_alpha() #Citation:https://www.shutterstock.com/video/clip-33970345-animation-laser-beam-on-black-background-alpha
        bullet_image=pygame.transform.scale(bullet_image,(20,20))
        self.image=bullet_image
        self.image.set_colorkey(BLACK)
        self.rect = self.image.get_rect()
        self.angle=angle
        self.speedX = 5 * math.cos(math.radians(self.angle)) 
        self.speedY = 5 * math.sin(math.radians(self.angle))
        self.enemyX=sx
        self.enemyY=sy
        self.playerX=px
        self.playerY=py
        self.bulletGoDown= (-1)
        
    def update(self):
        self.posX = self.rect.x
        self.posY = self.rect.y
        self.posX += self.speedX
        self.posY += self.speedY
        self.rect.center = (self.posX, self.posY)

class Tracer(Bullet):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        bullet_image=pygame.image.load("ammo/tracer.png").convert_alpha() #Citation:https://www.amazon.com/NieR-Automata-Halloween-Cosplay-Helmet/dp/B07D3TBF41/ref=sr_1_5?dchild=1&keywords=nier&qid=1574743951&s=apparel&sr=1-5
        bullet_image=pygame.transform.scale(bullet_image,(20,20))
        self.image=bullet_image
        self.image.set_colorkey(BLACK)
        self.rect = self.image.get_rect()
        self.speed=5
    
    def pos_towards_player(self, player_rect):
        c = math.sqrt((player_rect.x - self.rect.x) ** 2 + (player_rect.y - self.rect.y) ** 2) #distance formula
        try:
            x = (player_rect.x - self.rect.x) / c
            y = (player_rect.y - self.rect.y) / c
        except: #ZeroDivisionError
            return False
        return (x,y)
        
    def update(self,player_rect):#tracer moves towards player
        new_pos = self.pos_towards_player(player_rect)
        if new_pos: #if not ZeroDivisonError
            self.rect.x, self.rect.y = (self.rect.x + new_pos[0]*self.speed, self.rect.y + new_pos[1]*self.speed)

class predictingBullet(Tracer):
    def __init__(self,playerDirectionX,playerDirectionY):
        pygame.sprite.Sprite.__init__(self)
        bullet_image=pygame.image.load("ammo/predictor.png").convert_alpha() #Citation:https://www.scirra.com/store/effects-for-games/bullet-effects-3986
        bullet_image=pygame.transform.scale(bullet_image,(20,20))
        self.image=bullet_image
        self.image.set_colorkey(BLACK)
        self.rect = self.image.get_rect()
        self.speed=5
        self.playerDirectionX=playerDirectionX
        self.playerDirectionY=playerDirectionY
    
    def pos_towards_player(self, player_rect): #Similar but different from tracer. Moves further ahead, predicting player's position based on its movement
        c = math.sqrt((player_rect.x - self.rect.x) ** 2 + (player_rect.y - self.rect.y) ** 2)
        try:
            x = ((player_rect.x+15*self.playerDirectionX) - self.rect.x) / c
            y = ((player_rect.y+15*self.playerDirectionY) - self.rect.y) / c
        except:
            return False
        return (x,y)