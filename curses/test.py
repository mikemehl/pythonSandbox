import curses
from curses import wrapper

def main(stdscr):
    curses.curs_set(0)
    playerx = 5
    playery = 5
    stdscr.clear()
    stdscr.addstr(playery, playerx, '@')
    key = stdscr.getkey()
    keepGoing = True
    while keepGoing:
        stdscr.clear()
        if key=='k':
            playery -=1
        if key=='h':
            playerx -=1
        if key=='j':
            playery += 1
        if key=='l':
            playerx += 1
        if key=='q':
            keepGoing = False
        stdscr.addstr(playery, playerx, '@')
        stdscr.refresh()
        key = stdscr.getkey()

if __name__ == '__main__':
    wrapper(main)
