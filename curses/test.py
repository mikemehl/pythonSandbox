import curses
from curses import wrapper

MAX_X = 80
MAX_Y = int(MAX_X / 4)


def main(stdscr):
    curses.curs_set(0)
    playerx = int(MAX_X / 2 )
    playery = int(MAX_Y / 2 )
    themap = initMap()
    stdscr.clear()
    drawMap(themap, stdscr)
    stdscr.addstr(playery, playerx, '@')
    key = stdscr.getkey()
    keepGoing = True
    while keepGoing:
        stdscr.clear()
        if key=='k':
            if playery > 0:
                    playery -=1
        if key=='h':
            if playerx > 0:
                    playerx -=1
        if key=='j':
            if playery < MAX_Y:
                    playery += 1
        if key=='l':
            if playerx < MAX_X:
                    playerx += 1
        if key=='q':
            keepGoing = False
        drawMap(themap, stdscr)
        stdscr.addstr(playery, playerx, '@')
        stdscr.refresh()
        key = stdscr.getkey()

def drawMap(amap, screen):
    for j in range(0, MAX_Y):
            screen.addstr(j, 0, amap[j][0])
    return

def initMap():
        amap = [[' ']*MAX_X]*MAX_Y
        for i in range(0,MAX_X):
                amap[0][i] = '#'
        amap[5][6] = '*'
        return amap
            

if __name__ == '__main__':
    wrapper(main)

#Class for holding info about the game world, including:
#  * Map of the world
#  * List of actors present in the world (i.e. player/monsters)
#  * List of items in the world
#  * Methods for interacting with the above items
class GameWorld
   def __init__(self):
      self.worldMap = []
      self.actorList = []
      self.itemList = []

#Super Class for representing an actor (i.e. player/monster) in the game world:
#  *energy - for determining turns
#  *hp - health points obviously
#  *strength - basic combat damage stat
#  *speed - basic combat evade stat
class Actor
   def __init__(self):
      self.energy = 5
      self.hp = 10
      self.strength = 1
      self.speed = 1

#Class for representing the player's screen view
class Screen
   def __init__(self):
      self.xl = 100
      self.yl = 100
      self.theScreen = [];

#Class for managing the game 
class DungeonMaster
   def __init__(self):
      self.world = GameWorld()
      self.screen = Screen()
