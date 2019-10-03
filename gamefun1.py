import pgzrun
from random import randint
import math
import time
import datetime
WIDTH = 1280
HEIGHT = 720
Time = 0

Game_Over = False
DIFFICULTY = 1
player = Actor("player", (400, 550)) # Load in the player Actor image
   
def draw():
    screen.fill((100,200,200))
    if StatusGame == 0:
        message = "Are you ready, press Enter key to play."
        screen.draw.text(message,center=(640,360),fontsize=90,color='blue')
    elif StatusGame == 1:
        screen.blit('background', (0, 0))
        player.image = player.images[math.floor(player.status/6)]
        player.draw()
        drawLasers()
        drawAliens()
        drawBases()
        screen.draw.text(str(score), topright=(1180, 10), owidth=0.5, ocolor=(255,255,255), color=(0,64,255), fontsize=60)
        screen.draw.text(str(Time), topleft=(100, 10), owidth=0.5, ocolor=(255,255,255), color=(0,64,255), fontsize=60)
    if  player.status >= 30:
        screen.draw.text("GAME OVER\nPress Enter to play again : " + str(Time), center=(640, 360), owidth=0.5, ocolor=(255,255,255), color=(255,64,0), fontsize=60)
        screen.draw.text("\n\n\ncore : " + str(score), center=(640, 360), owidth=0.5, ocolor=(255,255,255), color=(255,64,0), fontsize=60)
    if  len(aliens) == 0 :
        screen.draw.text("YOU WON!\nPress Enter to play again : " + str(Time) +str(score), center=(640, 360), owidth=0.5, ocolor=(255,255,255), color=(255,64,0) , fontsize=60)
    
    elif StatusGame == 3:
        screen.fill((200,100,200))
        message = "Game over, your score : " + str(score)
        screen.draw.text(message,topleft=(20,270),fontsize=50,color='cyan')
        message = "Play again,press Enter key ."
        screen.draw.text(message,topleft=(20,350),fontsize=50,color='cyan')
    if Game_Over :
        screen.fill('red')
        msg = "Time out, final score : " +str(score)
        screen.draw.text(msg, center=(640,360), fontsize = 50)

def on_key_down(key):
    global StatusGame,Score,Time
    if StatusGame == 0:
        if key == keys.RETURN:
            start_game()
    elif StatusGame == 3 :
        if key == keys.RETURN:
            start_game()

def update(): # Pygame Zero update function
    global moveCounter,player,Game_Over
    if player.status < 30 and len(aliens) > 0:
        checkKeys()
        updateLasers()
        moveCounter += 1
        if moveCounter == moveDelay:
            moveCounter = 0
            updateAliens() 
        if player.status > 0: player.status += 1
    else:
        if keyboard.RETURN: init()

    global StatusGame,MaxFruits
    if StatusGame == 1:
        for n in range(MaxFruits):
            fruits[n].top += speeds[n]
            fruits[n].right += speeds[n]
            if(fruits[n].top > HEIGHT+100):
                fruits[n].bottom = -100
            if(fruits[n].right > WIDTH+100):
                fruits[n].left = -100

    if StatusGame == 1:
        for fruit in fruits:
            if fruit.colliderect(ship):
                fruits.remove(fruit)
                a = randint(0,2)
                fruits.append(Actor('apple'))
                speeds.append(randint(1,4))
                fruits[2].pos = POS[a]

    
def drawAliens():
    for a in range(len(aliens)): aliens[a].draw()

def drawBases():
    for b in range(len(bases)):
        bases[b].drawClipped()

def drawLasers():
    for l in range(len(lasers)): lasers[l].draw()

def checkKeys():
    global player, lasers
    if keyboard.left:
        if player.x > 40: player.x -= 5
    if keyboard.right:
        if player.x < 760: player.x += 5
    if keyboard.J:
        player.x = player.x - 5
    if keyboard.L:
        player.x = player.x + 5
    if keyboard.I:
        player.y = player.y - 5
    if keyboard.K:
        player.y = player.y + 5
    if keyboard.space:
        if player.laserActive == 1:
            player.laserActive = 0
            clock.schedule(makeLaserActive, 1.0)
            l = len(lasers)
            lasers.append(Actor("laser2", (player.x,player.y-32)))
            lasers[l].status = 0
            lasers[l].type = 1

def makeLaserActive():
    global player
    player.laserActive = 1
            
def checkBases():
    for b in range(len(bases)):
        if l < len(bases):
            if bases[b].height < 5:
                del bases[b]

def updateLasers():
    global lasers, aliens
    for l in range(len(lasers)):
        if lasers[l].type == 0:
            lasers[l].y += (2*DIFFICULTY)
            checkLaserHit(l)
            if lasers[l].y > 600:
                lasers[l].status = 1
        if lasers[l].type == 1:
            lasers[l].y -= 5
            checkPlayerLaserHit(l)
            if lasers[l].y < 10:
                lasers[l].status = 1
    lasers = listCleanup(lasers)
    aliens = listCleanup(aliens)

def listCleanup(l):
    newList = []
    for i in range(len(l)):
        if l[i].status == 0: newList.append(l[i])
    return newList
    
def checkLaserHit(l):
    global player
    if player.collidepoint((lasers[l].x, lasers[l].y)):
        player.status = 1
        lasers[l].status = 1
    for b in range(len(bases)):
        if bases[b].collideLaser(lasers[l]):
            bases[b].height -= 10
            lasers[l].status = 1

def checkPlayerLaserHit(l):
    global score
    for b in range(len(bases)):
        if bases[b].collideLaser(lasers[l]):
            lasers[l].status = 1
    for a in range(len(aliens)):
        if aliens[a].collidepoint((lasers[l].x, lasers[l].y)):
            lasers[l].status = 1
            aliens[a].status = 1
            score += 1000
            
def updateAliens():
    global moveSequence, lasers, moveDelay
    movex = movey = 0
    if moveSequence < 10 or moveSequence > 30:
        movex = -15
    if moveSequence == 10 or moveSequence == 30:
        movey = 50 + (10 * DIFFICULTY)
        moveDelay -= 1
    if moveSequence >10 and moveSequence < 30:
        movex = 15
    for a in range(len(aliens)):
        animate(aliens[a], pos=(aliens[a].x + movex, aliens[a].y + movey), duration=0.5, tween='linear')
        if randint(0, 1) == 0:
            aliens[a].image = "alien1"
    
        else:
            aliens[a].image = "alien1b"
            if randint(0, 5) == 0:
                lasers.append(Actor("laser1", (aliens[a].x,aliens[a].y)))
                lasers[len(lasers)-1].status = 0
                lasers[len(lasers)-1].type = 0
        if aliens[a].y > 500 and player.status == 0:
            player.status = 1
    moveSequence +=1
    if moveSequence == 40: moveSequence = 0

def init():
    global lasers, score, player, moveSequence, moveCounter, moveDelay
    initAliens()
    initBases()
    moveCounter = moveSequence = player.status = score = player.laserCountdown = 0
    lasers = []
    moveDelay = 30
    player.images = ["player","explosion1","explosion2", "explosion3","explosion4","explosion5"]
    player.laserActive = 1

def initAliens():
    global aliens
    aliens = []
    for a in range(20):
        aliens.append(Actor("alien1", (210+(a % 6)*80,100+(int(a/6)*64))))
        aliens[a].status = 0

def drawClipped(self):
    screen.surface.blit(self._surf, (self.x-32, self.y-self.height+30),(0,0,64,self.height))

def collideLaser(self, other):
    return (
        self.x-20 < other.x+5 and
        self.y-self.height+30 < other.y and
        self.x+32 > other.x+5 and
        self.y-self.height+30 + self.height > other.y
    )

def initBases():
    global bases
    bases = []
    bc = 0
    for b in range(4):
        for p in range(4):
            bases.append(Actor("base1", midbottom=(150+(b*300)+(p*40),520)))
            bases[bc].drawClipped = drawClipped.__get__(bases[bc])
            bases[bc].collideLaser = collideLaser.__get__(bases[bc])
            bases[bc].height = 60
            bc +=1

def start_game():
    global StatusGame,Time,score,MaxFruits,fruits,speed

    StatusGame = 1
    Time = 0
    score = 0
    MaxFruits = 3
    for n in range(MaxFruits) :
        fruits.append(Actor('apple'))
        speeds.append(randint(1,4))
        fruits[n].pos = POS[n]

def time_count():
    global Time
    Time += 1

def time_out():
    global Game_Over
    Game_Over = True

POS = [(150,0),(320,0),(560,0)]
score = 0
Time = 60
MaxFruits = 3
StatusGame = 0
fruits = Actor('apple')
fruits.pos = (1,4)      
ship = Actor('player')
ship.pos = (WIDTH/2,HEIGHT-40)
alienx = Actor('alien1')
alienx.pos = (400,175)
alienz = Actor('alien1b')
alienz.pos = (500,185)
fruits = []
speeds = []
clock.schedule_interval(time_count, 1.0)
clock.schedule(time_out,120.0)
init()
pgzrun.go()
