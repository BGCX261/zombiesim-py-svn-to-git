#! /usr/bin/env python
import random,pygame,sys
from pygame.locals import *

#Objects
class GameObject():
    def __init__(self,x,y,w,h):
        objects.append(self)
        self.rect = pygame.rect.Rect(x,y,w,h)
        
    def move(self,dx,dy):
        if dx != 0:
            self.moveAxis(dx,0)
        if dy != 0:
            self.moveAxis(0,dy)

    def draw(self,surface):
        pygame.draw.rect(surface,self.color,self.rect)

    def moveAxis(self,dx,dy):
        self.rect.left = self.rect.left + dx
        self.rect.top = self.rect.top + dy
        for wall in walls:
            if self.rect.colliderect(wall.rect):
                if dx > 0:
                    self.rect.right = wall.rect.left
                if dx < 0:
                    self.rect.left = wall.rect.right
                if dy > 0:
                    self.rect.bottom = wall.rect.top
                if dy < 0:
                    self.rect.top = wall.rect.bottom
        if self.rect.right > screenWidth:
            self.rect.right = self.rect.right - self.speed
        if self.rect.left < 0:
            self.rect.left = self.rect.left + self.speed
        if self.rect.top > (screenHeight + 44):             ## <-- 50 is text box size
            self.rect.top = self.rect.top - self.speed
        if self.rect.top < 50:                              ## lazy coding alert
            self.rect.top = self.rect.top + self.speed
            
    
class Baby(GameObject):
    def __init__(self,x,y):
        GameObject.__init__(self,x,y,6,6)
        babies.append(self)
        
        self.color = (255,117,231)
        self.age = 0
        self.speed = 1
        
    def agecount(self):
        self.age += 1
        if self.age == 720:
            Human(self.rect.left,self.rect.top)
            self.die()
    
    def die(self):
        babies.remove(self)
        objects.remove(self)
                    

class ZombieHunter(GameObject):

    def __init__(self,x,y):
        GameObject.__init__(self,x,y,6,6)
        hunters.append(self)
        
        self.color = (72,136,250)
        self.speed = 2
        self.checker = 50
    
    def AI(self):
        for zombie in zombies:
            xdis = abs(zombie.rect.left - self.rect.left)
            ydis = abs(zombie.rect.top - self.rect.top)
            if xdis < 2 and ydis < 2:
                zombie.die()
            if xdis < self.checker and ydis < self.checker:
                self.checker = 50
                if zombie.rect.left < self.rect.left:
                    self.move(-self.speed,0)
                else:
                    self.move(self.speed,0)
                if zombie.rect.top < self.rect.top:
                    self.move(0,-self.speed)
                else:
                    self.move(0,self.speed)
                break
            else:
                self.checker += 1
                
    def die(self):
        hunters.remove(self)
        objects.remove(self)

class ZombieShooter(GameObject):

    def __init__(self,x,y):
        GameObject.__init__(self,x,y,6,6)
        self.color = (255,0,0)
        shooter.append(self)
        self.checker = 50
        self.speed = 1
        for wall in walls:
            if self.rect.colliderect(wall.rect):
                self.die()
    
    def AI(self):
       for zombie in zombies:
            xdis = abs(zombie.rect.left - self.rect.left)
            ydis = abs(zombie.rect.top - self.rect.top)
            if xdis < 20 and ydis < 20:
                zombie.die()
            if xdis < self.checker and ydis < self.checker:
                self.checker = 50
                if zombie.rect.left < self.rect.left:
                    self.move(-self.speed,0)
                else:
                    self.move(self.speed,0)
                if zombie.rect.top < self.rect.top:
                    self.move(0,-self.speed)
                else:
                    self.move(0,self.speed)
                break
            else:
                self.checker += 1
                
    def die(self):
        shooter.remove(self)
        objects.remove(self) 
        ZombieShooter(random.randint(0,screenWidth),random.randint(0,screenHeight-50))
        
    
class Human(GameObject):

    def __init__(self,x,y):
        GameObject.__init__(self,x,y,6,6)
        humans.append(self)
        self.color = (255,255,255)
        self.speed = 1
        self.state = "calm"
        self.hadkids = 0
        
    def AI(self):
        
        if self.hadkids:
            self.hadkids -= 1
        if self.state == "calm":
            self.color = (255,255,255)
            self.speed = 1
        else:
            self.color = (255,160,160)
            self.speed = 2
        for zombie in zombies:
            xdis = abs(zombie.rect.left - self.rect.left)
            ydis = abs(zombie.rect.top - self.rect.top)
            if xdis < 75 and ydis < 75:
                self.state = "panic"
                self.hadkids = 300
                if zombie.rect.left > self.rect.left:
                    self.move(-self.speed,0)
                else:
                    self.move(self.speed,0)
                if zombie.rect.top > self.rect.top:
                    self.move(0,-self.speed)
                else:
                    self.move(0,self.speed)
                break
            else:
                self.state = "calm"
                    
        if random.randint(0,150) == 0 and self.state == "calm" and not self.hadkids:
            for human in humans:
                xdis = abs(human.rect.left - self.rect.left)
                ydis = abs(human.rect.top - self.rect.top)
                if not xdis == ydis:
                    if xdis < 2 and ydis < 2:
                        Baby(human.rect.left,human.rect.top)
                        self.hadkids = 720
                        break
                        
        if random.randint(0,60) == 0 and self.state == "calm":
            for human in humans:
                    xdis = abs(human.rect.left - self.rect.left)
                    ydis = abs(human.rect.top - self.rect.top)
                    if xdis < 50 and ydis < 50:
                        if human.rect.left > self.rect.left:
                            self.move(self.speed,0)
                        else:
                            self.move(-self.speed,0)
                        if human.rect.top > self.rect.top:
                            self.move(0,self.speed)
                        else:
                            self.move(0,-self.speed)
                        break
                                

    def die(self):
        humans.remove(self)
        objects.remove(self)
        
class Zombie(GameObject):
    def __init__(self,x,y):
        GameObject.__init__(self,x,y,6,6)
        zombies.append(self)
        self.color = (50,255,50)
        self.speed = 2
        self.checker = 50
        self.findbaby = 0
    def AI(self):
        for baby in babies:
                xdis = abs(baby.rect.left - self.rect.left)
                ydis = abs(baby.rect.top - self.rect.top)
                if xdis < 2 and ydis < 2:
                    Zombie(baby.rect.left,baby.rect.top)
                    baby.die()
                if xdis < 50 and ydis < 50:
                    self.findbaby=1
                    if baby.rect.left < self.rect.left:
                        self.move(-self.speed,0)
                    else:
                        self.move(self.speed,0)
                    if baby.rect.top < self.rect.top:
                        self.move(0,-self.speed)
                    else:
                        self.move(0,self.speed)
                    break
                else:
                    self.findbaby=0
        if not babies:
            self.findbaby=0
        if not self.findbaby:
            for human in humans:
                xdis = abs(human.rect.left - self.rect.left)
                ydis = abs(human.rect.top - self.rect.top)
                if xdis < 2 and ydis < 2:
                    Zombie(human.rect.left,human.rect.top)
                    human.die()
                if xdis < self.checker and ydis < self.checker:
                    self.checker = 50
                    if human.rect.left < self.rect.left:
                        self.move(-self.speed,0)
                    else:
                        self.move(self.speed,0)
                    if human.rect.top < self.rect.top:
                        self.move(0,-self.speed)
                    else:
                        self.move(0,self.speed)
                    break
                else:
                    self.checker+=1
                    
    def die(self):
        zombies.remove(self)
        objects.remove(self)

class Wall(GameObject):
    def __init__(self,x,y):
        GameObject.__init__(self,x,y,random.randint(25,200),random.randint(25,200))
        walls.append(self)
        
        self.color = (200,200,200)

    def die(self):
        zombies.remove(self)
        objects.remove(self)

#class GUI

#Initiate Variables
screenWidth = 940
screenHeight = 680
humanNum = 60
zombieNum = 1
hunterNum = 2
wallNum = 25
shooterNum = 0

objects = []
humans = []
zombies = []
walls = []
hunters = []
babies = []
shooter = []
shoothunter = []

huntercount = 0
created = 0 
size_textbox = 50
        
#Initiate Level
for i in range(0,humanNum):
    Human(random.randint(0, screenWidth),random.randint(size_textbox, screenHeight))
for i in range(0,zombieNum):
    Zombie(random.randint(0, screenWidth),random.randint(size_textbox, screenHeight))
for i in range(0,wallNum):
    Wall(random.randint(0, screenWidth),random.randint(size_textbox, screenHeight))

#Initiate Pygame
pygame.init()
pygame.display.set_caption('ZombieSim')
screen = pygame.display.set_mode((screenWidth,screenHeight + size_textbox))
MyGui = pygame.Surface((screenWidth,50))
clock = pygame.time.Clock()
font = pygame.font.SysFont("Hetvalitca",22)

#MainLoop
def eventHandle():
    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            sys.exit()

def update():
    screen.fill((0,0,0))
    for human in humans:
        human.move(random.randint(-1 * human.speed, human.speed),random.randint(-1 * human.speed, human.speed))
        human.AI()
        human.draw(screen)
    for zombie in zombies:
        zombie.move(random.randint(-1 * zombie.speed, zombie.speed),random.randint(-1 * zombie.speed, zombie.speed))
        zombie.AI()
        zombie.draw(screen)
    for hunter in hunters:
        hunter.move(random.randint(-1 * hunter.speed, hunter.speed),random.randint(-1 * hunter.speed, hunter.speed))
        hunter.AI()
        hunter.draw(screen)
    for baby in babies:
        baby.move(random.randint(-1 * baby.speed, baby.speed),random.randint(-1 * baby.speed, baby.speed))
        baby.agecount()
        baby.draw(screen)
    for shooters in shooter:
        shooters.AI()
        shooters.draw(screen)
    for wall in walls:
        wall.draw(screen)
    #pygame.draw.rect(screen, [100, 100, 100], (0,550,800,50))
    MyGui.fill((255,255,255))
    screen.blit(MyGui, (0,0))
    screen.blit(ZombieText, (10,10))
    screen.blit(HumanText, (10,25))
    pygame.display.flip()

while 1:
    if not created:
        huntercount+=1
        if huntercount==800:
            for i in range(0,hunterNum):
                ZombieHunter(random.randint(0,screenWidth),random.randint(size_textbox,screenHeight))
            for i in range(0,shooterNum):
                ZombieShooter(random.randint(0,screenWidth),random.randint(size_textbox,screenHeight))
            created=1
    ZombieText = font.render("Zombies: %s" % len(zombies),1,(0,0,0))
    HumanText = font.render("Humans: %s" % (len(humans)+len(babies)),1,(0,0,0))
    clock.tick(60)
    # print (clock.get_fps())
    eventHandle()
    update()