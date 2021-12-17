import pygame,math,random,time,os
from random import randrange
pygame.display.init()

WHITE=(255,255,255)
BLACK=(0,0,0)

window_width=570
window_height=750

class Asteroid(pygame.sprite.Sprite):
    def __init__(self,):
        pygame.sprite.Sprite.__init__(self)
        asteroid_image = pygame.image.load("asteroid1.png").convert_alpha() #Citation:https://commons.wikimedia.org/wiki/File:H%C3%BAsafell_Stone.png
        randomX=random.randint(40,60)
        randomY=randomX
        self.original_image = pygame.transform.scale(asteroid_image,(randomX,randomY))
        self.original_image.set_colorkey(BLACK)
        self.image = self.original_image.copy()
        self.image.set_colorkey(WHITE)
        self.rect = self.image.get_rect()
        self.radius = int(self.rect.width * 0.85 / 2)
        self.rect.x = random.randrange(window_width - self.rect.width)
        self.rect.y = random.randrange(-100, -50)
        self.speedx = random.randrange(-3, 3)
        self.speedy = random.randrange(1, 8)
        self.rotation = 0
        self.rot_speed = random.randrange(-8, 8)
        self.last_update = pygame.time.get_ticks()

    def rotate(self):
        now = pygame.time.get_ticks()
        if now - self.last_update > 40:
            self.last_update = now
            self.rotation = (self.rotation + self.rot_speed) % 360
            new_image = pygame.transform.rotate(self.original_image, self.rotation).convert_alpha()
            old_center = self.rect.center
            self.image = new_image
            self.rect = self.image.get_rect()
            self.rect.center = old_center

    def update(self):
        self.rotate()
        self.rect.x += self.speedx
        self.rect.y += self.speedy
        if self.rect.top > window_height + 10 or self.rect.left < -50 or self.rect.right > window_height + 50:
            self.rect.x = random.randrange(window_width - self.rect.width)
            self.rect.y = random.randrange(-100, -50)
            self.speedy = random.randrange(1, 8)
            
    def display(self,screen,x,y):
        screen.blit(self.image,(x,y))