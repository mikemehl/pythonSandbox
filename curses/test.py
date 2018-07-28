import time
import curses
from curses import wrapper

#Class for holding info about the game world, including:
#  * Map of the world
#  * List of actors present in the world (i.e. player/monsters)
#  * List of items in the world
#  * Methods for interacting with the above items
class GameWorld:
   MAX_X = 80
   MAX_Y = int(MAX_X / 4)
   def __init__(self):
      self.dungeonMap = []
      self.actorMap = []
      self.actorList = []
      self.itemList = []
      self.initMap()

   def initMap(self):
     amap = [[' ']*GameWorld.MAX_X]*GameWorld.MAX_Y
     for i in range(0,GameWorld.MAX_X):
             amap[0][i] = '#'
     amap[5][6] = '*'
     self.worldMap = amap 

#Class for representing the player's screen view
class Screen:
   def __init__(self, stdscr):
      self.xl = GameWorld.MAX_X
      self.yl = GameWorld.MAX_Y 
      self.theScreen = stdscr

   def drawDungeon(self, amap):
      #Draw the terrain
      for j in range(0, GameWorld.MAX_Y):
         self.theScreen.addstr(j, 0, amap[j][0])
      return

   def drawOverlay(self, actors):
      for actor in actors:
         actorChar = actor.repr
         actorPos = actor.pos
         self.theScreen.addstr(actorPos[1], \
            actorPos[0], actorChar)

   def refreshScreen(self):
      self.theScreen.refresh()

#Class for managing the game 
class DungeonMaster:
   def __init__(self, stdscr):
      curses.curs_set(0)
      self.energyThreshold = 5
      self.world = GameWorld()
      self.screen = Screen(stdscr)
      self.screen.drawDungeon(self.world.worldMap)
      self.screen.drawOverlay(self.world.actorList)
      self.screen.drawOverlay(self.world.itemList)
      self.screen.refreshScreen()
      time.sleep(5)
   
   def getInput(self):
      return self.screen.theScreen.getkey()

   def gameLoop(self):
      while True:
         #Go through the list of players.
         actors = self.world.actorList
         for actor in actors:
            #Call each ones action addEnergy method.
            actor.addEnergy()
            #If it's energy beats the threshold, it gets a turn.
            if actors.energy > self.energyThreshold:
               #If it's the player 
               if isinstance(actor, Player):
                  self.playerLoop(actor)
               #Call the actor's action method
               actor.action(self.world)

   def playerLoop(self, player):
      assert(isinstance(player, Player))
      #Update the screen 
      self.screen.drawDungeon(self.world.worldMap)
      self.screen.refreshScreen()
      inputCycle = True
      #Get user input 
      while inputCycle:
         key = self.getInput();
         #Tell the Player to process the input 
         inputCycle = actor.processInput(key) #on returning false, next action callback should be setup

#Super Class for representing an actor (i.e. player/monster) in the game world:
#  *pos - (x,y,z) where z is dungeon depth
#  *energy - for determining turns
#  *hp - health points obviously
#  *strength - basic combat damage stat
#  *speed - basic combat evade stat
#  *action - callback for what to do on a turn, takes 
#     -GameWorld for updating
#  *addEnergy - callback for how much energy to add
class Actor:
   def __init__(self):
      self.pos = [1,2,3]
      self.energy = 5
      self.hp = 10
      self.strength = 1
      self.speed = 1
      self.action = lambda : None
      self.addEnergy = lambda : None 

def main(stdscr):
   DungeonMaster(stdscr)            

if __name__ == '__main__':
    wrapper(main)
