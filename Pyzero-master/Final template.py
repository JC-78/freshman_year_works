import pygame,math,random,time,os
from os import path
from random import randrange
from asteroid import *
from bullet import *
from enemy import *

pygame.display.init()

WHITE=(255,255,255)
BLACK=(0,0,0)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
YELLOW = (255, 255, 0)
NAVY_BLUE=(0,0,128)

window_width=570
window_height=750
angle=0
HS_FILE="high_score.txt"

class Player(pygame.sprite.Sprite):
    def __init__(self,width,height):
        pygame.sprite.Sprite.__init__(self)
        self.width=width
        self.height=height
        self.health=800
        self.initial_health=self.health
        player_image = pygame.image.load("sprite_collection/player.png").convert_alpha() #Citation:https://www.kissclipart.com/spaceship-sprite-png-clipart-sprite-spacecraft-w66twe/
        player_image = pygame.transform.scale(player_image,(self.width,self.height))
        shield_image = pygame.image.load("shield.png").convert_alpha()
        shield_image = pygame.transform.scale(shield_image,(self.width+60,self.height+60))
        self.image=player_image
        self.image1=shield_image
        self.drawShield= False
        self.shield=50
        self.initial_shield=self.shield
        self.shieldLife=True
        self.rect=self.image.get_rect()
        self.angle =90
        self.direction=0
        self.angle+=self.direction
        self.xCoordinate=0
        self.yCoordinate=0

    def update(self): 
        rotated_image=pygame.transform.rotate(self.image,self.direction)
        new_rect=rotated_image.get_rect(center=(self.xCoordinate,self.yCoordinate))
        self.image=rotated_image
        
    def shoot(self,x,y): 
        angle=self.angle%360
        bullet = Bullet(self.rect.center,angle)
        bullet.rect.x = x+40
        bullet.rect.y = y+40
        return bullet
            
    def display(self,screen,x,y):
        screen.blit(self.image,(x,y))
    
class Explosion(pygame.sprite.Sprite):
    def __init__(self, center, size,explosion_animation):
        pygame.sprite.Sprite.__init__(self)
        self.size = size
        self.image = explosion_animation[self.size][0]
        self.rect = self.image.get_rect()
        self.rect.center = center
        self.frame = 0
        self.last_update = pygame.time.get_ticks()
        self.frame_rate = 50

    def update(self,explosion_animation):
        now = pygame.time.get_ticks()
        if now - self.last_update > self.frame_rate:
            self.last_update = now
            self.frame += 1
            if self.frame == len(explosion_animation[self.size]):
                self.kill()
            else:
                center = self.rect.center
                self.image = explosion_animation[self.size][self.frame]
                self.rect = self.image.get_rect()
                self.rect.center = center

    def display(self,screen,x,y):
        screen.blit(self.image,(x,y))

#Game from here
class Game:
    explosion_animation = {}
    explosion_animation['vgg'] = []
    explosion_animation['gg'] = []
    explosion_animation['lg'] = []
    explosion_animation['sm'] = []

    def __init__(self, num_waste, max_depth,level=1):
        pygame.init()
        self.screenWidth=570
        self.screenHeight=750
        self.screen = pygame.display.set_mode((self.screenWidth, self.screenHeight))
        pygame.display.set_caption("PyZero")
        self.level=level

        for i in range(9):
            filename = 'regularExplosion0{}.png'.format(i)
            img=pygame.image.load(f"Explosions_collection/{filename}").convert() #Citation:http://kidscancode.org/blog/2016/09/pygame_shmup_part_10/
            img.set_colorkey(BLACK)
            img_lg = pygame.transform.scale(img, (300, 300))
            Game.explosion_animation['vgg'].append(img_lg)
            img_lg = pygame.transform.scale(img, (150, 150))
            Game.explosion_animation['gg'].append(img_lg)
            img_lg = pygame.transform.scale(img, (75, 75))
            Game.explosion_animation['lg'].append(img_lg)
            img_sm = pygame.transform.scale(img, (32, 32))
            Game.explosion_animation['sm'].append(img_sm)
        
        self.timer=0
        self.clock_tick_rate=20        
        self.clock = pygame.time.Clock()
        self.start_time = time.time()
        self.clock = pygame.time.Clock()

        (self.bg_width,self.bg_height)=(1080,900)

        self.laser_sound = pygame.mixer.Sound('music/LASER-SHOT- SOUND.wav') #Citation:https://www.youtube.com/watch?v=sFcGLBoE72k
        self.explosion_sound = pygame.mixer.Sound('music/Explosion- Sound.wav') #Citation:https://www.youtube.com/watch?v=XjOtGgxaX5g
        
        self.num_waste = num_waste
        self.max_depth = max_depth

        self.score=0
        self.totalEnemies=5*self.level # Total number of enemies to draw
        self.enemyList=['Enemy','Rainer','Kamikaze']
        self.midboss=True
        self.midbossIdentity=0
        self.boss=True
        self.bossIdentity=0
        self.enemyKilled=0
        self.enemyCreated=0
        self.wastePerEnemy=self.num_waste/self.totalEnemies
        self.sign=1
        
        self.playerSprite = Player(40, 40)
        self.playerSprite.rect.y = window_height-20
        
        self.multiplayer=False
        self.player2=Player(40,40)
        self.playerSprite.rect.y = window_height-20

        self.directionX=1
        self.directionY=1
        self.dead=False

        self.player_list=pygame.sprite.Group()
        self.player_list.add(self.playerSprite)
        self.player_list.add(self.player2) 
        self.all_enemy_list=pygame.sprite.Group()
        self.bullet_list=pygame.sprite.Group()
        self.enemy_bullet_list=pygame.sprite.Group()
        self.midboss_bullet_list=pygame.sprite.Group()
        self.enemy_tracer_list=pygame.sprite.Group()
        self.enemy_fractalBullet_list=pygame.sprite.Group()
        self.asteroid_list=pygame.sprite.Group()
        self.explosion_list=pygame.sprite.Group()
        self.bulletCount=0
        
        pygame.mixer.music.load("music/Bipolar Nightmare (Vocals).mp3")  #Citation:https://www.youtube.com/watch?v=rQuHwqMcN8w
        pygame.mixer.music.play(-1)
        self.load_data()
        self.init_waste()

    def load_data(self): #load your highest level reached till now 
        self.dir = path.dirname(__file__)
        with open(path.join(self.dir, HS_FILE), 'r') as f:
            try:
                self.highscore = int(f.read())
                return self.highscore
            except:
                self.highscore = 0

    def init_waste(self):# Create the wastes that appear in background
        self.waste = []
        for i in range(self.num_waste):
            waste = [randrange(-50,50), randrange(-50,50), randrange(1, self.max_depth)]
            self.waste.append(waste)

    def moveAndDrawWaste(self): #Move and draw the wastes in the background
        origin_x = self.screenWidth / 2
        origin_y = self.screenHeight / 2

        for waste in self.waste:
            waste[2] -= 0.20
            if waste[2] <= 0:
                waste[0] = randrange(-50,50)
                waste[1] = randrange(-50,50)
                waste[2] = self.max_depth   

            #Convert the 3D coordinates to 2D using perspective projection.
            k = 64 /waste[2]
            x = int(waste[0] * k + origin_x)
            y = int(waste[1] * k + origin_y)
 
            if 0 <= x < self.screenWidth and 0 <= y < self.screenHeight:
                size = (1 - float(waste[2]) / self.max_depth) * 10
                shade = (1 - float(waste[2]) / self.max_depth) * 240
                self.screen.fill((shade,shade,shade),(x,y,size,size))

    def drawShield(self,px,py,player_num): 
        if player_num==1:
            if self.playerSprite.drawShield:
                self.screen.blit(self.playerSprite.image1,(px-30,py-30))
                self.playerSprite.drawShield=False
        if player_num==2:
            if self.multiplayer and self.player2.drawShield:
                self.screen.blit(self.player2.image1,(px-30,py-30))
                self.player2.drawShield=False
    
    def draw(self,lst): #helper function for drawing enemies and other objects in game
        for item in lst:
            item.update()
            item.display(self.screen,item.rect.x,item.rect.y)

    def collision(self,player,object_list,condition): #helper function for player collision and small expl
        hit_list=pygame.sprite.spritecollide(player, object_list, condition)
        for hit in hit_list:
            expl = Explosion(hit.rect.center, 'sm',Game.explosion_animation)
            self.explosion_list.add(expl)
            player.health-=(4*self.level) 
            player.drawShield=True
            if self.multiplayer:
                if player==self.playerSprite:
                    self.player2.drawShield=True
                else:
                    self.playerSprite.drawShield=True
            if object_list==self.asteroid_list:
                asteroid=Asteroid()
                self.asteroid_list.add(asteroid)

    def collision1(self,player,object_list,condition): #helper function for player collision and large expl
        hit_list=pygame.sprite.spritecollide(player, object_list, condition)
        for hit in hit_list:
            expl = Explosion(hit.rect.center, 'lg',Game.explosion_animation)
            self.explosion_list.add(expl)
            player.health-=(4*self.level) 
            player.drawShield=True
            if object_list==self.asteroid_list:
                asteroid=Asteroid()
                self.asteroid_list.add(asteroid)
        
    def run2(self): #For multiplayer
        self.multiplayer=True
        self.run()

    def run(self): #Main loop
        self.timer+=1
        self._keys={}
        self._keys[pygame.K_SPACE]=False
        self._keys[pygame.K_DOWN]=False
        self._keys[pygame.K_UP]=False
        self._keys[pygame.K_RIGHT]=False
        self._keys[pygame.K_LEFT]=False
        
        while (self.dead==False) and self.boss==True:  
            self.timer+=1
            self.clock.tick(70) # Lock the framerate at 70 FPS.
            # Handle events(movement and shooting)
            if self._keys[pygame.K_SPACE]:
                if not self.multiplayer:
                    if len(self.bullet_list)<=20:
                        bullet=self.playerSprite.shoot(self.playerSprite.rect.x,self.playerSprite.rect.y)
                        self.bullet_list.add(bullet)
                        self.bulletCount+=1
                        self.laser_sound.play()
                else:
                    if len(self.bullet_list)<=40:
                        bullet=self.playerSprite.shoot(self.playerSprite.rect.x,self.playerSprite.rect.y)
                        self.bullet_list.add(bullet)
                        self.bulletCount+=1
                        self.laser_sound.play()
            if self._keys[pygame.K_DOWN]:
                self.player2.rect.y+=10
            if self._keys[pygame.K_UP]:
                self.player2.rect.y-=10
            if self._keys[pygame.K_RIGHT]:
                self.player2.rect.x+=10
            if self._keys[pygame.K_LEFT]:
                self.player2.rect.x-=10
            
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    os._exit(0)
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_SPACE:
                        self._keys[event.key]=True                      
                    if event.key == pygame.K_DOWN:
                        self._keys[event.key]=True
                    if event.key == pygame.K_UP:
                        self._keys[event.key]=True
                    if event.key == pygame.K_RIGHT:
                        self._keys[event.key]=True
                    if event.key == pygame.K_LEFT:
                        self._keys[event.key]=True
                    if event.key ==pygame.K_a: 
                        self.playerSprite.direction = 90
                        self.playerSprite.angle+=90
                        self.playerSprite.update()
                    if event.key == pygame.K_d:
                        self.playerSprite.direction = -90
                        self.playerSprite.angle-=90
                        self.playerSprite.update()
                    if event.key == pygame.K_COMMA:
                        self.player2.direction = 90
                        self.player2.angle+=90
                        self.player2.update()
                    if event.key == pygame.K_PERIOD:
                        self.player2.direction = -90
                        self.player2.angle-=90
                        self.player2.update()
                    if event.key == pygame.K_SLASH:
                        bullet=self.player2.shoot(self.player2.rect.x,self.player2.rect.y)
                        self.bullet_list.add(bullet)
                        self.bulletCount+=1
                        self.laser_sound.play()
                if event.type == pygame.KEYUP:
                    self._keys[event.key]=False
        
            self.screen.fill(WHITE)    
            #drawing background for odd number game level and controlling zoom in/out during boss fight
            if self.level%2==1:
                background=pygame.image.load("picture/background.jpg")
                background=pygame.transform.scale(background,(self.bg_width,self.bg_height))  #citation:http://kreatif.com.ua/index.php?newsid=789&news_page=2
                rect=background.get_rect()
                self.screen.blit(background,rect) 
                if self.midboss==False:
                    self.bg_width -= 3* self.sign
                    self.bg_height-= 3* self.sign
                    if self.bg_width<=940:
                        self.sign*=-1
                    if self.bg_width>=1080:
                        self.sign*=-1
            #drawing background for even number game level and controlling zoom in/out during boss fight
            if self.level%2==0:  
                background=pygame.image.load("picture/background2.jpg") #citation:https://www.computerworld.com/article/3427955/cloud-computing-trends-for-2019.html
                background=pygame.transform.scale(background,(self.bg_width,self.bg_height))  
                rect=background.get_rect()
                self.screen.blit(background,rect) 
                if self.midboss==False:
                    self.bg_width -= 3* self.sign
                    self.bg_height-= 3* self.sign
                    if self.bg_width<=940:
                        self.sign*=-1
                    if self.bg_width>=1080:
                        self.sign*=-1
            #draw level at bottom right
            self.message_display(f'Level:{self.level}',self.screenWidth*(0.9),self.screenHeight*(0.9),BLACK)
                    
            #player's position is same as the cursor's
            pos = pygame.mouse.get_pos()
            self.playerSprite.rect.x = pos[0]
            self.playerSprite.rect.y=pos[1]

            #needed for enemies' bullets that predict player's future location
            if self.playerSprite.rect.x>self.playerSprite.xCoordinate:
                self.directionX=1
            else:
                self.directionX=-1

            if self.playerSprite.rect.y>self.playerSprite.yCoordinate:
                self.directionY=1
            else:
                self.directionY=-1

            #for rotation
            self.playerSprite.xCoordinate= self.playerSprite.rect.x
            self.playerSprite.yCoordinate= self.playerSprite.rect.y
            if self.multiplayer:
                self.player2.xCoordinate= self.player2.rect.x
                self.player2.yCoordinate= self.player2.rect.y

            #Ensure player is within the screen. For single-player and multiplayer
            if self.playerSprite.rect.x+self.playerSprite.width>=self.screenWidth:
                self.playerSprite.rect.x=self.screenWidth-self.playerSprite.width
            if self.playerSprite.rect.y+self.playerSprite.height>=self.screenHeight:
                self.playerSprite.rect.y=self.screenHeight-self.playerSprite.height
            if self.multiplayer:
                if self.player2.rect.x+self.player2.width>=self.screenWidth:
                    self.player2.rect.x=self.screenWidth-self.player2.width
                if self.player2.rect.x<=0:
                    self.player2.rect.x=0
                if self.player2.rect.y+self.player2.height>=self.screenHeight:
                    self.player2.rect.y=self.screenHeight-self.player2.height
                if self.player2.rect.y<=0:
                    self.player2.rect.y=0

            #draw player and its health bar #If multiplayer, update and draw player 2 position
            self.playerSprite.display(self.screen,self.playerSprite.rect.x,self.playerSprite.rect.y)
            if self.multiplayer:
                self.player2.display(self.screen,self.player2.rect.x,self.player2.rect.y)
            if self.multiplayer:
                self.draw_health_bar(5,730,self.playerSprite.health+self.player2.health,self.playerSprite.initial_health+self.player2.initial_health)
                self.draw_health_bar(5,710,self.playerSprite.shield+self.player2.shield,self.playerSprite.initial_shield+self.player2.initial_shield) 
            if not self.multiplayer:
                self.draw_health_bar(5,730,self.playerSprite.health,self.playerSprite.initial_health)
                self.draw_health_bar(5,710,self.playerSprite.shield,self.playerSprite.initial_shield) 

            #dead conditions for single and multiplayer     
            if self.multiplayer and (self.playerSprite.health+self.player2.health)<=0:
                self.dead=True
            if not self.multiplayer and self.playerSprite.health<=0:
                self.dead=True

            #adding enemies
            if self.enemyCreated<self.totalEnemies:
                if self.timer%20==0:
                    choice=random.randint(0,2)
                    if choice==0:
                        enemy=Enemy(20, 20)
                    elif choice==1:
                        enemy=Rainer(20, 20)
                    else:
                        enemy=Kamikaze(20,20)
                    enemy.rect.x = random.randrange(30,self.screenWidth-30)
                    enemy.rect.y = random.randrange(0,self.screenHeight/2)
                    self.all_enemy_list.add(enemy)
                    self.enemyCreated+=1
            
            #draw small explosion if player collides against enemies and asteroids.
            self.collision(self.playerSprite,self.all_enemy_list,False)
            self.collision(self.playerSprite,self.asteroid_list,True)
            if self.multiplayer:
                self.collision(self.player2,self.all_enemy_list,False)
                self.collision(self.player2,self.asteroid_list,True)

            #enemy shooting.
            for enemy in self.all_enemy_list:
                if (type(enemy)==Enemy):
                    if self.timer%10==0:
                        bullet=enemy.shoot(enemy.rect.x+60,enemy.rect.y+40)
                        self.enemy_bullet_list.add(bullet)
                elif (type(enemy)==Kamikaze):
                    if self.timer%6==0:
                        bullet=enemy.shoot(enemy.rect.x+20,enemy.rect.y+40)
                        self.enemy_bullet_list.add(bullet)
                        bulletOne=enemy.shoot(enemy.rect.x+70,enemy.rect.y+40)
                        self.enemy_bullet_list.add(bulletOne)
                elif (type(enemy)==Rainer):
                    if self.timer%6==0:
                        bullet=enemy.shoot(enemy.rect.x+60,enemy.rect.y+40)
                        self.enemy_bullet_list.add(bullet)
                elif (type(enemy)==Midboss):
                    self.draw_health_bar(5,5,enemy.health,enemy.value)
                    if self.timer%12==0:
                        tracer=enemy.shoot(enemy.rect.x,enemy.rect.y)
                        self.enemy_tracer_list.add(tracer)
                #boss shooting pattern
                elif (type(enemy)==Boss):
                    self.draw_health_bar(5,5,enemy.health,enemy.value)
                    distance=((enemy.rect.x-self.playerSprite.rect.x)**2+(enemy.rect.y-self.playerSprite.rect.y)**2)**0.5
                    if (self.timer%45==0):
                        bullet=enemy.shootF(enemy.rect.x,enemy.rect.y)
                        self.enemy_fractalBullet_list.add(bullet)

                    if (self.timer%15==0):
                        if (0.8*enemy.value)<=enemy.health<=(enemy.value):
                            for i in range(0,int(enemy.width),int(enemy.width/4)):
                                if distance<=300:
                                    bullet=enemy.shootN(enemy.rect.x+i,enemy.rect.y+130)
                                    self.enemy_bullet_list.add(bullet)
                                else:
                                    if len(self.enemy_tracer_list)<=24:
                                        bullet=enemy.shootT(enemy.rect.x+i,enemy.rect.y+20)
                                        self.enemy_tracer_list.add(bullet)
                        elif ((0.45*enemy.value)<=enemy.health<=(0.8*enemy.value)):#bounce around
                            if distance<=300:
                                angle=0 
                                for x in range(12): 
                                    bullet=enemy.shootC(enemy.rect.x,enemy.rect.y,angle,self.playerSprite.xCoordinate,self.playerSprite.yCoordinate)
                                    self.enemy_bullet_list.add(bullet)
                                    angle+=30
                                angle=0
                            else:
                                if len(self.enemy_tracer_list)<=24:
                                    bullet=enemy.shootT(enemy.rect.x+i,enemy.rect.y+20)
                                    self.enemy_tracer_list.add(bullet)
                        elif ((0.25*enemy.value)<=enemy.health<=(0.45*enemy.value)): #spasm
                            if distance>=200:
                                if len(self.enemy_tracer_list)<=40:
                                    bullet=enemy.shootP(enemy.rect.x+i,enemy.rect.y+20,self.directionX,self.directionY)
                                    self.enemy_tracer_list.add(bullet)
                                    bullet=enemy.shootT(enemy.rect.x+i,enemy.rect.y+20)
                                    self.enemy_tracer_list.add(bullet)
                            else:
                                for i in range(0,int(enemy.width),int(enemy.width/8)):
                                    bullet=enemy.shootN(enemy.rect.x+i,enemy.rect.y+20)
                                    self.enemy_bullet_list.add(bullet)
                        elif (0<=enemy.health<=(0.25*enemy.value)):
                            if distance<=300:
                                for i in range(0,int(enemy.width),int(enemy.width/4)):
                                    bullet=enemy.shootN(enemy.rect.x+i,enemy.rect.y+20)
                                    self.enemy_bullet_list.add(bullet)
                            else:
                                if len(self.enemy_tracer_list)<30:
                                    bullet=enemy.shootT(enemy.rect.x+i,enemy.rect.y+20)
                                    self.enemy_tracer_list.add(bullet)
            #updating and drawing tracer and predicting bullets
            for tracer in self.enemy_tracer_list:
                if type(tracer)==predictingBullet:
                    (tracer.playerDirectionX,tracer.playerDirectionY)=(self.directionX,self.directionY)                
                tracer.update(self.playerSprite.rect)
                tracer.display(self.screen,tracer.rect.x,tracer.rect.y)

            self.collision1(self.playerSprite,self.enemy_tracer_list,True)
            if self.multiplayer:
                self.collision1(self.player2,self.enemy_tracer_list,True)

            self.draw(self.enemy_fractalBullet_list)
            for fB in self.enemy_fractalBullet_list:
                if (fB.rect.y==self.screenHeight):
                    self.enemy_fractalBullet_list.remove(fB)
                hit_list=pygame.sprite.spritecollide(fB, self.player_list,False)
                for hit in hit_list:
                    expl = Explosion(hit.rect.center, 'lg',Game.explosion_animation)
                    self.explosion_list.add(expl)
                    self.playerSprite.health-=(4*self.level) 
                    self.playerSprite.drawShield=True
                    if self.multiplayer:
                        self.player2.drawShield=True
                        
            self.drawShield(self.playerSprite.xCoordinate,self.playerSprite.yCoordinate,1)
            self.drawShield(self.player2.xCoordinate,self.player2.yCoordinate,2)

            #updating normal enemy bullet and checking if it hits player
            self.draw(self.enemy_bullet_list)
            for enemy_bullet in self.enemy_bullet_list:
                if (enemy_bullet.rect.y==self.screenHeight):
                    self.enemy_bullet_list.remove(enemy_bullet)
                #Bullet deflection
                blocks_hit_list = pygame.sprite.spritecollide(enemy_bullet,self.player_list,False)
                for hit in blocks_hit_list:
                    self.playerSprite.health-=(4*self.level) 
                    self.playerSprite.drawShield=True
                    if self.multiplayer:
                        self.player2.drawShield=True
                    expl = Explosion(hit.rect.center, 'lg',Game.explosion_animation)
                    self.explosion_list.add(expl)
                    if self.playerSprite.shieldLife or self.player2.shieldLife:
                        if pygame.sprite.collide_rect(self.playerSprite,enemy_bullet):
                            if enemy_bullet.bulletGoDown==1: #when enemy bullet is from above
                                bullet = Bullet(enemy_bullet.rect.center,90)
                                bullet.rect.x = self.playerSprite.xCoordinate+40
                                bullet.rect.y = self.playerSprite.yCoordinate+40
                                self.bullet_list.add(bullet) 
                                self.playerSprite.shield-=10
                                self.enemy_bullet_list.remove(enemy_bullet)
                            elif enemy_bullet.bulletGoDown==(-1):#when enemy bullet is from below 
                                bullet = Bullet(enemy_bullet.rect.center,-90)
                                bullet.rect.x = self.playerSprite.xCoordinate+40
                                bullet.rect.y = self.playerSprite.yCoordinate+40
                                self.bullet_list.add(bullet) 
                                self.playerSprite.shield-=10
                                self.enemy_bullet_list.remove(enemy_bullet)
                            else:
                                pass
                        elif self.multiplayer and pygame.sprite.collide_rect(self.player2,enemy_bullet):
                            if enemy_bullet.bulletGoDown==1: 
                                bullet = Bullet(enemy_bullet.rect.center,90)
                                bullet.rect.x = self.player2.xCoordinate+40
                                bullet.rect.y = self.player2.yCoordinate+40
                                self.bullet_list.add(bullet) 
                                self.player2.shield-=10
                                self.enemy_bullet_list.remove(enemy_bullet)
                            elif enemy_bullet.bulletGoDown==(-1):
                                bullet = Bullet(enemy_bullet.rect.center,-90)
                                bullet.rect.x = self.player2.xCoordinate+40
                                bullet.rect.y = self.player2.yCoordinate+40
                                self.bullet_list.add(bullet) 
                                self.player2.shield-=10
                                self.enemy_bullet_list.remove(enemy_bullet)
                            else:
                                pass
            #shield life control
            if self.multiplayer:
                if self.playerSprite.shield+self.player2.shield<=0:
                    self.playerSprite.shieldLife=False
                    self.player2.shieldLife=False
            else:
                if self.playerSprite.shield<=0:
                    self.playerSprite.shieldLife=False
                if self.playerSprite.shieldLife==False:
                    self.playerSprite.shield+=2
                if self.playerSprite.shield>=50:
                    self.playerSprite.shieldLife=True
            #updating and drawing player bullet. Also test collision against fractal bullets
            for tempBullet in self.bullet_list: 
                tempBullet.update()
                tempBullet.display(self.screen,tempBullet.pos[0],tempBullet.pos[1])  
                if(tempBullet.rect.x<=0) or (tempBullet.rect.y<=0) \
                    or (tempBullet.rect.x>=self.screenWidth) or (tempBullet.rect.y>=self.screenHeight):
                    self.bullet_list.remove(tempBullet)
                for fB in self.enemy_fractalBullet_list:
                    if pygame.sprite.collide_circle(tempBullet,fB):
                        if fB.rect.width>=80 and fB.level>0:
                            x=fB.rect.x
                            y=fB.rect.y
                            for i in range(-150,250,100):
                                bullet=fractalBullet(x,y,fB.level-1)
                                bullet.rect.x+=i
                                bullet.rect.y+=10
                                self.enemy_fractalBullet_list.add(bullet)
                            fB.kill()
                        elif fB.rect.width<=80 and fB.level>0:
                            fB.kill()
                        elif fB.level==0:
                            fB.kill()
                #checking if midboss or boss got hit by bullet. 
                if len(self.all_enemy_list)<=1:
                    for enemy in self.all_enemy_list:
                        if type(enemy)==Midboss:
                            blocks_hit_list = pygame.sprite.spritecollide(tempBullet, self.all_enemy_list, False)
                            for hit in blocks_hit_list:
                                if (enemy.health-10)<=0:
                                    expl = Explosion(hit.rect.center, 'gg',Game.explosion_animation)
                                    self.explosion_list.add(expl)
                                    self.all_enemy_list.remove(enemy)
                                    self.midboss=False #midboss die
                                    self.explosion_sound.play()
                                else:
                                    expl = Explosion(hit.rect.center, 'sm',Game.explosion_animation)
                                    self.explosion_list.add(expl)
                                    enemy.health-=10
                        
                        if type(enemy)==Boss:
                            blocks_hit_list = pygame.sprite.spritecollide(tempBullet, self.all_enemy_list,False)
                            for hit in blocks_hit_list:
                                if (enemy.health-10)<=0:
                                    expl = Explosion(hit.rect.center, 'vgg',Game.explosion_animation)
                                    self.explosion_list.add(expl)
                                    self.all_enemy_list.remove(enemy)
                                    self.boss=False #boss die       
                                    self.explosion_sound.play()                             
                                else:
                                    expl = Explosion(hit.rect.center, 'sm',Game.explosion_animation)
                                    self.explosion_list.add(expl)
                                    enemy.health-=10
                                
                #If bullet hit an enemy, it will explode and disappear 
                if self.midbossIdentity not in self.all_enemy_list and self.bossIdentity not in self.all_enemy_list:
                    blocks_hit_list = pygame.sprite.spritecollide(tempBullet, self.all_enemy_list, True)
                    self.enemyKilled+=len(blocks_hit_list)
                    for hit in blocks_hit_list:
                        expl = Explosion(hit.rect.center, 'lg',Game.explosion_animation)
                        self.explosion_list.add(expl)
                        for i in range(int(self.wastePerEnemy)):
                            self.waste.pop()

                #player bullet destroying fractal bullet
                blocks_hit_list = pygame.sprite.spritecollide(tempBullet, self.enemy_fractalBullet_list, True)
                for hit in blocks_hit_list:
                    expl = Explosion(hit.rect.center, 'lg',Game.explosion_animation)
                    self.explosion_list.add(expl)
                
                #player bullet destroying tracer
                blocks_hit_list = pygame.sprite.spritecollide(tempBullet, self.enemy_tracer_list, True)
                for hit in blocks_hit_list:
                    expl = Explosion(hit.rect.center, 'sm',Game.explosion_animation)
                    self.explosion_list.add(expl)
                num=len(blocks_hit_list)
                if(num > 0):
                    self.score+=num
                    self.message_display(f'Remaining Enemies:{len(self.all_enemy_list)}',self.screenWidth/2,self.screenHeight/6,BLACK)
                    self.bullet_list.remove(tempBullet)                    

                #player bullet destroying asteroid
                blocks_hit_list = pygame.sprite.spritecollide(tempBullet, self.asteroid_list, True)
                for hit in blocks_hit_list:
                    expl = Explosion(hit.rect.center, 'lg',Game.explosion_animation)
                    self.explosion_list.add(expl)
                    asteroid=Asteroid()
                    self.asteroid_list.add(asteroid)
            
            self.draw(self.asteroid_list)
            self.draw(self.all_enemy_list)
            
            #adding asteroids and a midboss after all small enemies die 
            if len(self.all_enemy_list)<=0:
                if self.midboss and self.enemyKilled>=self.totalEnemies:
                    midboss=Midboss(20,20,self.level)
                    midboss.rect.x = random.randrange(50,self.screenWidth-50)
                    midboss.rect.y = random.randrange(50,self.screenHeight-20)
                    self.midbossIdentity=midboss
                    self.all_enemy_list.add(midboss)
                        
                    pygame.mixer.music.load("music/midboss_fight.mp3") #Citation:https://www.youtube.com/watch?v=x8YW7INN7Z4
                    pygame.mixer.music.play(-1)
                    for i in range(7):
                        asteroid=Asteroid()
                        self.asteroid_list.add(asteroid)

            #adding boss after all small enemies and midboss die  
            if len(self.all_enemy_list)<=0: 
                if self.midboss==False and self.boss and self.enemyKilled>=self.totalEnemies:
                    boss=Boss(30,30,self.level)
                    boss.rect.x = random.randrange(50,self.screenWidth-50)
                    boss.rect.y=50
                    self.bossIdentity=boss
                    self.all_enemy_list.add(boss)
                    pygame.mixer.music.load("music/boss_fight.mp3") #Citation: https://www.youtube.com/watch?v=T_jgBbCsdeU
                    pygame.mixer.music.play(-1)
                    
            #update and draw explosion
            for explosion in self.explosion_list:
                explosion.update(Game.explosion_animation)
                explosion.display(self.screen,explosion.rect.x,explosion.rect.y)
                
            pygame.display.flip()
            self.clock.tick(self.clock_tick_rate)
            if(self.score >= self.totalEnemies and self.midboss==False and self.boss==False):
                print("You finished game in ", (time.time() - self.start_time), " seconds")
                print("Total bullets used ", self.bulletCount)
                print("Your shooting accuracy ", (self.totalEnemies/self.bulletCount)*100, "%")

            self.moveAndDrawWaste()
            pygame.display.flip() #updates the entire Surface on the display.
        
        #game over when self.dead==True or self.boss==False(die)
        if self.dead:
            self.gameOver_screen()
        else:
            self.transition_screen()

    def transition_screen(self): #Transition after you clear the level
        self.level+=1
        self.message_display("click '0' to proceed to next level ",self.screenWidth/2,self.screenHeight/2,WHITE)
        pygame.display.flip()
        self.wait_for_key()

    def show_start_screen(self): # game splash/start screen     
        intro = True
        while intro:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    intro=False
                    os._exit(0)
                  
            self.screen.fill(WHITE)
            background=pygame.image.load("picture/background1.jpg")
            background=pygame.transform.scale(background,(1080,900))
            rect=background.get_rect()
            self.screen.blit(background,rect)
            self.message_display('PyZero',self.screenWidth/2,self.screenHeight*(1/6),WHITE)
            self.button("PLAY",140,320,260,50,GREEN,NAVY_BLUE,self.run)
            self.button("MULTIPLAYER",140,400,260,50,GREEN,NAVY_BLUE,self.run2)
            self.button("Instruction",140,480,260,50,YELLOW,NAVY_BLUE,self.instruction_screen)
            self.button("Highest Score",140,560,260,50,YELLOW,NAVY_BLUE,self.score_screen)
            pygame.display.flip()

    def score_screen(self):
        background=pygame.image.load("picture/background3.jpg")
        background=pygame.transform.scale(background,(1080,900)) #https://www.jrailpass.com/blog/arashiyama-bamboo-forest
        rect=background.get_rect()
        self.screen.blit(background,rect) 
        result=self.load_data()
        self.message_display(f'Highest Level ever reached is {result}',self.screenWidth/2,self.screenHeight/2,WHITE)
        self.message_display("Press 'r' to return",self.screenWidth/2,self.screenHeight*(9.5/10),WHITE)
        self.wait_for_key()

    def instruction_screen(self):
        background=pygame.image.load("picture/background1.jpg")
        background=pygame.transform.scale(background,(1080,900))
        rect=background.get_rect()
        self.screen.blit(background,rect)
        self.message_display('Use cursor to move',self.screenWidth/2,self.screenHeight*(1/10),WHITE)
        self.message_display('Press SPACE to shoot',self.screenWidth/2,self.screenHeight*(1/7),WHITE)
        self.message_display('Click A and D rotate left,right',self.screenWidth/2,self.screenHeight*(1/4),GREEN)
        self.message_display('Aliens are attacking Earth ',self.screenWidth/2,self.screenHeight*(2/5),WHITE)
        self.message_display('and producing chemical waste ',self.screenWidth/2,self.screenHeight/2,WHITE)
        self.message_display('Shoot down all the enemies',self.screenWidth/2,self.screenHeight*(3/5),WHITE)
        self.message_display('win and make Earth clean again',self.screenWidth/2,self.screenHeight*(0.7),WHITE)
        self.message_display("For multi, 2nd player uses ",self.screenWidth/2,self.screenHeight*(4/5),WHITE)
        self.message_display("',' and '.' to rotate and '/' to shoot",self.screenWidth/2,self.screenHeight*(7/8),WHITE)
        self.message_display("Press 'r' to return",self.screenWidth/2,self.screenHeight*(9.5/10),WHITE)

        pygame.display.flip()
        self.wait_for_key()

    def gameOver_screen(self): # game over/continue
        pygame.mixer.music.load("music/death.mp3") #Citation:https://www.youtube.com/watch?v=CrOUCJay_7U
        pygame.mixer.music.play(-1)
        print("game over screen")
        if self.level > self.highscore:
            self.highscore = self.level
            with open(path.join(self.dir, HS_FILE), 'w') as f:
                f.write(str(self.level))
        if not self.dead:
            return
        self.screen.fill(WHITE)
        if self.dead and self.boss:
            background=pygame.image.load("picture/gameover.jpg")
            background=pygame.transform.scale(background,(self.bg_width,self.bg_height))  #citation:https://www.ethos3.com/2013/11/dont-leave-your-ideas-in-the-graveyard/
            rect=background.get_rect()
            self.screen.blit(background,rect)
            self.message_display('GAME OVER',self.screenWidth/2,self.screenHeight/2,BLACK)
        elif self.dead and self.boss==False:
            self.message_display('GAME CLEAR',self.screenWidth/2,self.screenHeight/2,BLACK)
        self.message_display('Press "r" to restart',self.screenWidth/2,self.screenHeight*(3/4),BLACK)
        pygame.display.flip()
        self.wait_for_key()
    
    def wait_for_key(self):#for start,gameover,instruction and score screen
        waiting = True
        while waiting:
            self.clock.tick(self.clock_tick_rate)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    os._exit(0)
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_r:
                        Game(512, 40,level=1).show_start_screen()
                    elif event.key == pygame.K_0:
                        if self.multiplayer==True:
                            Game(512,40,self.level).run2()
                        else:
                            Game(512,40,self.level).run()
                   
    def text_objects(self, text,font,color=BLACK):     #setting up text
        black=(0,0,0)
        textSurface = font.render(text,True,color)
        return textSurface, textSurface.get_rect()

    def message_display(self,text,locationX,locationY,color): #displaying message
        largeText = pygame.font.Font('freesansbold.ttf',30)
        TextSurf, TextRect = self.text_objects(text, largeText,color)
        TextRect.center = ((locationX),(locationY))
        self.screen.blit(TextSurf, TextRect)
        pygame.display.update()

    def button(self,msg,x,y,w,h,color1,color2,action):  #setting up button
        mouse = pygame.mouse.get_pos()
        click = pygame.mouse.get_pressed()
        if x+w > mouse[0] > x and y+h > mouse[1] > y:
            pygame.draw.rect(self.screen,color2,(x,y,w,h))
            if click[0] == 1 and action != None:
                action()         
        else:
            pygame.draw.rect(self.screen,color1,(x,y,w,h))
        self.message_display(msg,(x+w/2),(y+h/2),BLACK)
    
    def draw_health_bar(self, x, y, health,initial_health): 
        if health < 0:
            health = 0
        bar_length=100
        bar_height=10
        fill = (health / 300) * bar_length
        outline_rect = pygame.Rect(x, y, bar_length, bar_height)
        fill_rect = pygame.Rect(x, y, fill, bar_height)
        if (0.3*initial_health)< health <(0.6*initial_health):
            pygame.draw.rect(self.screen, YELLOW, fill_rect)
        elif 0<= health<=(0.3*initial_health):
            pygame.draw.rect(self.screen, RED, fill_rect)
        else:  
            pygame.draw.rect(self.screen, GREEN, fill_rect)
        
if __name__ == "__main__":  #start of everything
    Game(512, 40,level=1).show_start_screen()