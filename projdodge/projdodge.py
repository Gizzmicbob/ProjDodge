#imports
from sense_hat import SenseHat, ACTION_PRESSED, ACTION_RELEASED
import random
import time
#

## Programmer   : Gizzmicbob and Birdemic
## Last Updeate : 26/04/18
## Description  : This is a small game designed to run on the SenseHat.
##              : As the green blob named Karl, you must dodge projectiles.

#colors
PLAYERCOLOR = (0,200,0)
PROJCOLOR0 = (200,0,0)
PROJCOLOR1 = (200,200,200)
PROJCOLOR2 = (200,200,0)
PROJCOLOR3 = (200,0,200)
PROJCOLOR4 = (0,0,200)
PROJCOLOR5 = (0,200,200)

#speed
#STANDARD - 0.8
#ASYNC/RAND - 0.2
BASESPEED = 0.8 #seconds until projectiles move (initial speed... ~halves by the hardest round)

#screen flipped
FLIP = False #if using the PI upside-down, enable this... needs to be double checked on a PI

#round limits
ROUNDLIMIT = 2
ROUNDLIMIT2 = 4
ROUNDLIMIT3 = 6
ROUNDLIMIT4 = 8
ROUNDLIMIT5 = 10

#death message
SKIP_DMESSAGE = False
DM_SPEED = 0.05

#move mode
ASYNC = False #moves porjectiles one at a time... should be better perf
RAND = False #randomly moves projectiles on at a time.. requires ASYNC to work

#godmode
GODMODE = False #nuf said?

#don't change below unless you know what you're doing
#inital setup
# # # # # #

sense = SenseHat()#just to shorten the SenseHat functions

#arrays
projectiles = []
startPos = [3,3] #the start position of the player

#ints
RANDround = 0
curRound = 0 #current round
stage = 0 #current stage
alongX = 0 #to limit projectiles on x axis
alongY = 0 #to limit projectiles on y axis
curProj = 0
projCount = 4

#bools
started = False
alive = True
moved = False

speed = BASESPEED #speed

startTime = time.time() #time

#flip stuff
up = "up"
down = "down"
left = "left"
right = "right"
if FLIP:
  sense.set_rotation(180)
  up = "down"
  down = "up"
  left = "right"
  right = "left"
  
#clearing the screen to start
sense.clear()

# # # # # #

###reset stuff###
def DeathMessage():
  #message on death
  global alive
  sense.clear() #clears screen from old game
  if not SKIP_DMESSAGE:
    #little and fat Karl death messages
    if not stage > 1:
      sense.show_message("Little Karl died after round "+str(curRound-1)+" :(", DM_SPEED, PLAYERCOLOR)
    else:
      sense.show_message("Fat Karl died after round "+str(curRound-1)+" :(", DM_SPEED, PLAYERCOLOR)
  ClearAll()
  alive = True #sets player to be alive after the death message

def ClearAll():
  #resets everything back to their original state
  #you have to call global to use vars outside of the function
  global curRound
  global stage
  global started
  global alongX
  global alongY
  global speed
  curRound = 0
  stage = 0
  alongX = 0
  alongY = 0
  speed = BASESPEED
  for proj in projectiles:
    proj.active = 0 #deactivates all projectiles
  started = False #sets the game to not started so it runs initial function
#^^reset stuff^^#  

###projectile stuff###
class projectile:
    def __init__(self,x,y,direction,active,name):
        #spawns projectile
        self.x = x
        self.y = y
        self.direction = direction
        self.active = active
        self.name = name
        projectiles.append(self) #adds new projectile to the projectile array
        #spawns projectile initially
        if name == 0:
          sense.set_pixel(x, y, PROJCOLOR0)
        if name == 1:
          sense.set_pixel(x, y, PROJCOLOR1)
        if name == 2:
          sense.set_pixel(x, y, PROJCOLOR2)
        if name == 3:
          sense.set_pixel(x, y, PROJCOLOR3)
        if name == 4:
          sense.set_pixel(x, y, PROJCOLOR4)
        if name == 5:
          sense.set_pixel(x, y, PROJCOLOR5) 
    def move(self):
      #moves projectile depending on its set direction
      global alongX
      global alongY
      if self.active == 1: #only moves active projectiles
        if self.direction == 0:
            self.x-=1
        if self.direction == 1:
            self.y+=1
        if self.direction == 2:
            self.x+=1
        if self.direction == 3:
            self.y-=1
        #deactivates projectile if it hits a wall
        if (self.x > 7 and self.direction == 2) or (self.x < 0 and self.direction == 0) or (self.y < 0 and self.direction == 3) or (self.y > 7 and self.direction == 1):
          if self.name == 0: #to limit the prints to one
            print("That round had "+str(alongX)+" projectiles along the X axis and "+str(alongY)+" along the Y axis")
          self.active = 0
          alongX = 0
          alongY = 0
          print("Projectile "+str(self.name)+" hit a wall at "+str(self.x)+","+str(self.y))
        return True

#initializes projectiles
projPos0 = projectile(1,7,3,0,0)
projPos1 = projectile(1,7,3,0,1)   
projPos2 = projectile(1,7,3,0,2)   
projPos3 = projectile(1,7,3,0,3)
projPos4 = projectile(1,7,3,0,4)
projPos5 = projectile(1,7,3,0,5)   

#^^projectile stuff^^-#

def blit():
  #handles rendering and player impacts
    global alive
    global started
    sense.clear()
    if alive:
      #checks if pixel exists (is on map) and lights it if so
      if not (startPos[0] > 7 and startPos[1] < 0):
        sense.set_pixel(startPos[0], startPos[1], PLAYERCOLOR)
      if stage >= 2:
        #checks if pixel exists (is on map) for stage 2 and lights it if so
        if not (startPos[0] > 6 ):
          sense.set_pixel(startPos[0]+1, startPos[1], PLAYERCOLOR)
        if not (startPos[1] > 6):
          sense.set_pixel(startPos[0], startPos[1]+1, PLAYERCOLOR)
        if not (startPos[0] > 6 or startPos[1] > 6):
          sense.set_pixel(startPos[0]+1, startPos[1]+1, PLAYERCOLOR)
      #lights the projectiles if active
      if projPos0.active:
        sense.set_pixel(projPos0.x, projPos0.y, PROJCOLOR0)
      if projPos1.active:
        sense.set_pixel(projPos1.x, projPos1.y, PROJCOLOR1)
      if projPos2.active:
        sense.set_pixel(projPos2.x, projPos2.y, PROJCOLOR2)
      if projPos3.active:
        sense.set_pixel(projPos3.x, projPos3.y, PROJCOLOR3)
      if projPos4.active:
        sense.set_pixel(projPos4.x, projPos4.y, PROJCOLOR4)
      if projPos5.active:
        sense.set_pixel(projPos5.x, projPos5.y, PROJCOLOR5)  
      for proj in projectiles:
        #checks if any active projectiles are touching the player
        if not GODMODE:
          if proj.active and alive and started: #checks alive and started to fix spawn kill bug
            if proj.x == startPos[0]:
              if proj.y == startPos[1]:
                print("Player died at "+str(proj.x)+","+str(proj.y)+" by projectile #"+str(proj.name)+" on round #"+str(curRound))
                alive = False
                DeathMessage()
                return
            if stage >= 2: #checks impacts for larger model
              if proj.x == startPos[0]+1:
                if proj.y == startPos[1]:
                  print("Player died at "+str(proj.x)+","+str(proj.y)+" by projectile #"+str(proj.name)+" on round #"+str(curRound))
                  alive = False
                  DeathMessage()
                  return
              if proj.x == startPos[0]:
                if proj.y == startPos[1]+1:
                  print("Player died at "+str(proj.x)+","+str(proj.y)+" by projectile #"+str(proj.name)+" on round #"+str(curRound))
                  alive = False
                  DeathMessage()
                  return
              if proj.x == startPos[0]+1:
                if proj.y == startPos[1]+1:
                  print("Player died at "+str(proj.x)+","+str(proj.y)+" by projectile #"+str(proj.name)+" on round #"+str(curRound))
                  alive = False
                  DeathMessage()
                  return
                
###tells projectiles to move###
def AProjMove(number):
  global curProj
  global curRound
  global RANDround
  curProj += 1
  count = 3
  if stage >= 1:
    count = 4
  if stage >= 3:
    count = 5
  if RAND:
    number = random.randint(0,count)
  if number == 0:
    if projectiles[0].move():
      blit()
  elif number == 1:
    if projectiles[1].move():
      blit()
  elif number == 2:
    if projectiles[2].move():
      blit()
  elif number == 3:
    if projectiles[3].move():
      blit()
      if stage < 1:
        curProj = 0
  elif number == 4:
    if projectiles[4].move():
      blit()
      if stage < 3:
        curProj = 0
  elif number == 5:
    if projectiles[5].move():
      blit()
    curProj = 0
  if RAND:
    RANDround += 1
    if RANDround >= 8 * projCount:
      RANDround = 0
      if curRound > 0:
        print("Passed round #"+str(curRound))
      curRound += 1

#runs the move function if the player is still alive
def ProjMove():
  for proj in projectiles:
    if alive:
      if proj.move():
        blit() #runs blit after moving the projectiles

###main loop###
while True:
  if not started:
    #stops moving during death message
    startPos[0] = 3
    startPos[1] = 3
    sense.stick.get_events()
    started = True
    blit()
    print("The player respawned at "+str(startPos[0])+","+str(startPos[1]))
  if alive and started:
    #new timer solution, shouldn't be affected by device performance anymore
    if (time.time() - startTime) > speed:
        startTime = time.time()
        #projectile spawning
        if ASYNC:
          AProjMove(curProj)
        else:
          ProjMove()
        for proj in projectiles:
          if proj.active == 0: #sets the new properties for the projectile if it is inactive
            if proj.name == 0 and not (ASYNC and RAND):
              if curRound > 0:
                print("Passed round #"+str(curRound))
              curRound += 1 #adds a round
            if proj.name == 4 and stage < 1:
              break
            if proj.name == 5 and stage < 3:
              break
            side = random.randint(0,3)
            #should ensure possibility by only allowing 3 going on the same axis
            if alongX > 2:
              side = random.choice([0,2])
            elif alongY > 2:
              side = random.choice([1,3])
            px = random.randint(0,7)
            if curRound == ROUNDLIMIT and stage == 0:
              stage = 1 #sets to stage 2
              projCount = 5
              print("Added a projectile")
            elif curRound == ROUNDLIMIT2 and stage == 1:
              stage = 2 #sets to stage 3
              print("Size increased")
            elif curRound == ROUNDLIMIT3 and stage == 2:
              stage = 3 #sets to stage 4
              projCount = 6
              print("Added a projectile")
            elif curRound == ROUNDLIMIT4 and stage == 3:
              stage = 4 #sets to stage 5
              speed *= 0.7
              print("Speed set to #"+str(speed))
            elif curRound == ROUNDLIMIT5 and stage == 4:
              stage = 5 #sets to stage 6
              speed *= 0.7
              print("Speed set to #"+str(speed))
            if side == 0:
              proj.x = px
              proj.y = 0
              proj.direction = 1
              proj.active = 1
              alongY += 1
            if side == 1:
              proj.x = 7
              proj.y = px
              proj.direction = 0
              proj.active = 1
              alongX += 1
            if side == 2:
              proj.x = px
              proj.y = 7
              proj.direction = 3
              proj.active = 1
              alongY += 1
            if side == 3:
              proj.x = 0
              proj.y = px
              proj.direction = 2
              proj.active = 1
              alongX += 1
            blit()
    
    for event in sense.stick.get_events():
        #movement - other methods seem better, but this works best so far
        if event.direction == up and startPos[1] > 0 and not moved:
            startPos[1] -= 1
            moved = True
            blit()
        elif event.direction == up and not moved:
          print("Player hit the roof")
        if event.direction == down and startPos[1] < 7 - max(min(stage - 1,1), 0) and not moved:
            startPos[1] += 1
            moved = True
            blit()
        elif event.direction == down and not moved:
          print("Player hit the floor")
        if event.direction == left and startPos[0] > 0 and not moved:
            startPos[0] -= 1
            moved = True
            blit()
        elif event.direction == left and not moved:
          print("Player hit the left wall")
        if event.direction == right and startPos[0] < 7 - max(min(stage - 1,1), 0) and not moved:
            startPos[0] += 1
            moved = True
            blit()
        elif event.direction == right and not moved:
          print("Player hit the right wall")
        #to stop moving when holding direction
        if event.action == "released":
          moved = False