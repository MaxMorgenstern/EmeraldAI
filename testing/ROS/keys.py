import select
import sys

import pygame
from pygame.locals import *

pygame.init()
pygame.display.set_mode((100,100))

currentPress = None

while True:
    for event in pygame.event.get():
        if event.type == QUIT: sys.exit()
        if event.type == KEYDOWN and event.dict['key'] == 27: sys.exit()

        if event.type == KEYUP:
            #print "Up", event.key
            if currentPress == event.key:
                currentPress = None

        if event.type == KEYDOWN:
            #print "Down", event.key
            currentPress = event.key
            
    if currentPress != None:
        print "Pressed", currentPress

        """
        if event.type == KEYDOWN and event.dict['key'] == 273:
            print 'up'
        if event.type == KEYDOWN and event.dict['key'] == 274:
            print 'down'
        if event.type == KEYDOWN and event.dict['key'] == 275:
            print 'right'
        if event.type == KEYDOWN and event.dict['key'] == 276:
            print 'left'
        
        if event.type == KEYDOWN:
            print event.dict['key']
        """
    pygame.event.pump()



"""
while True:
    i,o,e = select.select([sys.stdin],[],[],0)
    for s in i:
        if s == sys.stdin:
            input = sys.stdin.readline()
            print "...", input
"""

#-----

"""
import curses

screen = curses.initscr()
screen.addstr("Hello World!!!")
screen.refresh()
while True:
    x = screen.getch()
    if c == ord('p'):
        print "p was pressesd"
"""