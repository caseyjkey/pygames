# Snake
# By Casey Key casey.key@protonmail.com
# http://whatspython.com

import random, pygame, sys
from pygame.locals import *

""" 1. Canvas dimensions """
FPS = 15
WINDOWWIDTH = 640
WINDOWHEIGHT = 480
CELLSIZE = 20
assert WINDOWWIDTH % CELLSIZE == 0, "Window width must be multiple of cell size."
assert WINDOWHEIGHT % CELLSIZE == 0, "Window height must be multiple of cell size."
CELLWIDTH = int(WINDOWWIDTH/CELLSIZE)
CELLHEIGHT = int(WINDOWHEIGHT/CELLSIZE)

""" 2. Colors """
#             R    G    B
WHITE     = (255, 255, 255)
BLACK     = (  0,   0,   0)
RED       = (255,   0,   0)
GREEN     = (  0, 255,   0)
DARKGREEN = (  0, 155,   0)
DARKGREY  = ( 40,  40,  40)
BGCOLOR = BLACK

""" 3. String constants """
UP = 'up'
DOWN = 'down'
LEFT = 'left'
RIGHT = 'right'

HEAD = 0 # Syntactic sugar, 0 is the Snake's head

def main():
    global FPSCLOCK, DISPLAYSURF, BASICFONT

    pygame.init() # always init pygame at start of game
    FPSCLOCK = pygame.time.Clock()
    DISPLAYSURF = pygame.display.set_mode((WINDOWWIDTH, WINDOWHEIGHT))
    BASICFONT = pygame.font.Font("cooperblackstdopentype", 18)
    pygame.display.set_caption('Snake Game')

    showStartScreen()
    while True: # main game loop
        runGame()
        showGameOverScreen()

def showStartScreen():
    titleFont = pygame.font.Font("cooperblackstdopentype", 100)
    titleSurf1 = titleFont.render('Snake!', True, WHITE, DARKGREEN)
    titleSurf2 = titleFont.render('Snake!', True, GREEN)

    degrees1 = 0
    degrees2 = 0
