import curses
import os
from curses import wrapper

def logout():
    os.system("openbox --exit")
def lock():
    os.system("slock")
def suspend():
    os.system("acpiconf -s3")
def shutdown():
    os.system("poweroff")
def reboot():
    os.system("notify-send çalışmıyor")
def main(stdscr):
    curses.curs_set(0)
    curses.mousemask(1)
    curses.init_pair(1, curses.COLOR_BLACK, curses.COLOR_WHITE)
    curses.init_pair(2, curses.COLOR_RED, curses.COLOR_BLACK)
    curses.init_pair(3, curses.COLOR_GREEN, curses.COLOR_BLACK)
    curses.init_pair(4, curses.COLOR_YELLOW, curses.COLOR_BLACK)
    curses.init_pair(5, curses.COLOR_MAGENTA, curses.COLOR_BLACK)
    curses.init_pair(6, curses.COLOR_CYAN, curses.COLOR_BLACK)
    curses.init_pair(7, curses.COLOR_RED, curses.COLOR_WHITE)
    stdscr.addstr(0,28, ">>>>>>>>>>KYAK-3<<<<<<<<<<", curses.color_pair(1))
    stdscr.addstr(2,13, ">>>>>>press p to shutdown(poweroff)", curses.color_pair(2))
    stdscr.addstr(3,13, ">>>>>>press r to reboot)", curses.color_pair(3))
    stdscr.addstr(4,13, ">>>>>>press z to suspend", curses.color_pair(4))
    stdscr.addstr(5,13, ">>>>>>press . to lock", curses.color_pair(5))
    stdscr.addstr(6,13, ">>>>>>press l to logout", curses.color_pair(6)) 
    stdscr.addstr(7,13, "As you see buttons on below",curses.color_pair(1))
    
    stdscr.addstr(9,17, "POWEROFF",curses.color_pair(2))
    stdscr.addstr(11,17, "REBOOT",curses.color_pair(3))
    stdscr.addstr(13,17, "SUSPEND",curses.color_pair(4))
    stdscr.addstr(15,17, "LOCK",curses.color_pair(5))
    stdscr.addstr(17,17, "LOGOUT",curses.color_pair(6))
                          
    while True:
          stdscr.refresh()
          key = stdscr.getch()  
          if key == ord('p'):
             shutdown()
          elif key == ord('l'):
             logout()
          elif key == ord('r'):
             reboot()
          elif key == ord('.'):
             lock()
          elif key == ord('z'):
             suspend()
          if key == curses.KEY_MOUSE:
             _,x,y,_,_ =curses.getmouse()
             if y == 9 and x in range(17,26):
                shutdown()
             elif y == 11 and x in range(17,23):
                reboot()
             elif y == 13 and x in range(17,24):
                suspend()
             elif y == 15 and x in range(17,21):
                lock()
             elif y == 17 and x in range(17,23):
                logout()
          
    stdscr.refresh()
    stdscr.getch()
    
curses.wrapper(main)
