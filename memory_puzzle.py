# Memory Puzzle

import random, pygame, sys
from pygame.locals import *

""" Defining game dimensions, colors, and assets """
FPS          = 30  # frames per second, how long of a pause between each game loop
WINDOWWIDTH  = 640 # window width in pixels
WINDOWHEIGHT = 480 # window height in pixels
REVEALSPEED  = 8   # speed of box reveals and covers
BOXSIZE      = 40  # box height and width in pixels
GAPSIZE      = 10  # space between boxes
BOARDWIDTH   = 10  # number of columns of icons
BOARDHEIGTH  = 7   # number of rows and icons
assert (BOARDWIDTH * BOARDHEIGTH) % 2 is 0, "Board needs to have an even number of boxes for pairs of matches."
TILESIZE     = BOXSIZE + GAPSIZE
XMARGIN      = int((WINDOWWIDTH - (BOARDWIDTH * TILESIZE)) / 2)
YMARGIN      = int((WINDOWHEIGHT - (BOARDHEIGTH * TILESIZE)) / 2)

#            R    G    B
GRAY     = (100, 100, 100)
NAVYBLUE = ( 60,  60, 100)
WHITE    = (255, 255, 255)
RED      = (255,   0,   0)
GREEN    = (  0, 255,   0)
BLUE     = (  0,   0, 255)
YELLOW   = (255, 255,   0)
ORANGE   = (255, 255,   0)
PURPLE   = (255,   0, 255)
CYAN     = (  0, 255, 255)

BGCOLOR        = NAVYBLUE
LIGHTBGCOLOR   = GRAY
BOXCOLOR       = WHITE
HIGHLIGHTCOLOR = BLUE

DONUT   = "donut"
SQUARE  = "square"
DIAMOND = "diamond"
LINES   = "lines"
OVAL    = "oval"

ALLCOLORS = (RED, GREEN, BLUE, YELLOW, ORANGE, PURPLE, CYAN)
ALLSHAPES = (DONUT, SQUARE, DIAMOND, LINES, OVAL)
assert len(ALLCOLORS) * len(ALLSHAPES) * 2 >= BOARDWIDTH * BOARDHEIGTH, "Board is too big for the number of colors and shapes defined."
""" ------------ End of defining game dimensions, colors, and assets -------------- """

""" Main game loop """
def main():
    global FPSCLOCK, DISPLAYSURF
    pygame.init()
    FPSCLOCK    = pygame.time.Clock()
    DISPLAYSURF = pygame.display.set_mode((WINDOWWIDTH, WINDOWHEIGHT), 0, 32)

    mousex = 0 # stores x coordinate of mouse event
    mousey = 0 # stores y coordinate of mouse event
    pygame.display.set_caption("Memory Game")

    mainBoard = getRandomizedBoard()
    revealedBoxes = generateRevealedBoxesData(False)

    firstSelection = None # stores the (x, y) of the first box clicked

    DISPLAYSURF.fill(BGCOLOR)
    startGameAnimation(mainBoard)

    while(True): # main game loop
        mouseClicked = False

        DISPLAYSURF.fill(BGCOLOR) # drawing the window
        drawBoard(mainBoard, revealedBoxes)

        for event in pygame.event.get():
            if event.type is QUIT or (event.type is KEYUP and event.type is K_ESCAPE):
                pygame.quit()
                sys.exit()
            elif event.type is MOUSEMOTION:
                mousex, mousey = event.pos
            elif event.type is MOUSEBUTTONUP:
                mousex, mousey = event.pos
                mouseClicked = True

        boxx, boxy = getBoxAtPixel(mousex, mousey)
        if boxx != None and boxy != None:
            # The mouse is currently over a box
            if not revealedBoxes[boxx][boxy]:
                drawHighlightBox(boxx, boxy)
            if not revealedBoxes[boxx][boxy] and mouseClicked:
                revealBoxesAnimation(mainBoard, (boxx, boxy))
                revealedBoxes[boxx][boxy] = True

                if firstSelection == None: # This box was the first box clicked
                    firstSelection = (boxx, boxy)
                else: # The current box was the second one clicked
                    icon1shape, icon1color = getShapeAndColor(mainBoard, firstSelection[0], firstSelection[1])
                    icon2shape, icon2color = getShapeAndColor(mainBoard, boxx, boxy)

                    # Icons don't match, recover both selections
                    if icon1shape != icon2shape or icon1color != icon2color:
                        pygame.time.wait(1000)
                        coverBoxesAnimation(mainBoard, [(firstSelection[0], firstSelection[1]), (boxx, boxy)])
                        revealedBoxes[firstSelection[0]][firstSelection[1]] = False
                        revealedBoxes[boxx][boxy] = False
                    elif hasWon(revealedBoxes):





""" -------------------- End of main game loop ----------------------------------------"""

""" Helper methods for main """
def getRandomizedBoard():
    # get a list of every possible shape in every possible color
    icons = []
    for color in ALLCOLORS:
        for shape in ALLSHAPES:
            icons.append( (shape,color) )

    random.shuffle(icons) # randomize the order of the icons list
    numIconsNeeded = int(BOARDWIDTH * BOARDHEIGTH / 2)
    icons = icons[:numIconsNeeded] * 2 # make pairs of each icon
    random.shuffle(icons)

    # create the board data structure, with randomly placed icons
    board = []
    for x in range(BOARDWIDTH):
        column = []
        for y in range(BOARDHEIGTH):
            column.append(icons[0])
            del icons[0] # icon line moves forward
        board.append(column) # add column to board
    return board

def generateRevealedBoxesData(val):
    revealedBoxes = [] # empty list
    for i in range(BOARDWIDTH):
        revealedBoxes.append([val] * BOARDHEIGTH)
    return revealedBoxes

def splitIntoGroupsOf(groupSize, theList):
    # Splits a list into a list of lists, where the inner lists have
    # at most groupSize elements
    result = []
    for i in range(0, len(theList), groupSize):
        result.append(theList[i:i + groupSize])
    return result

def leftTopCoordsOfBox(boxx, boxy):
    # Convert bord coordinates to pixel coordinates
    left = boxx * (BOXSIZE + GAPSIZE) + XMARGIN
    top = boxy * (BOXSIZE + GAPSIZE) + YMARGIN
    return (left, top)

def getBoxAtPixel(x, y):
    for boxx in range(BOARDWIDTH):
        for boxy in range(BOARDHEIGTH):
            left, top = leftTopCoordsOfBox(x, y)
            boxRect = pygame.draw.rect(left, top, BOXSIZE, BOXSIZE)
            if boxRect.collidepoint(x, y): # if x, y is within the box, return the box
                return (boxx, boxy)
    return (None, None)

def getShapeAndColor(board, boxx, boxy):
    # shape value for x, y spot is stored in board[x][y][0]
    # color value for x, y spot is stored in board[x][y][1]
    return board[boxx][boxy][0], board[boxx][boxy][1]

def drawIcon(shape, color, boxx, boxy):
    quarter = int(BOXSIZE * 0.25) # syntactic sugar
    half    = int(BOXSIZE * 0.5)  # syntactic sugar

    left, top = leftTopCoordsOfBox(boxx, boxy) # get pixel coords from board coords

    # Draw the shapes
    if shape is DONUT:
        pygame.draw.circle(DISPLAYSURF, color, (left + half, top + half), half - 5)
        pygame.draw.circle(DISPLAYSURF, BGCOLOR, (left + half, top + half), quarter - 5)
    elif shape is SQUARE:
        pygame.draw.rect(DISPLAYSURF, color, (left + quarter, top + quarter, BOXSIZE - half, BOXSIZE - half))
    elif shape is DIAMOND:
        pygame.draw.polygon(DISPLAYSURF, color, ((left + half, top), (left + BOXSIZE - 1, top + half), (left + half, top + BOXSIZE - 1), (left, top + half)))
    elif shape is LINES:
        for i in range(0, BOXSIZE, 4):
            pygame.draw.line(DISPLAYSURF, color, (left, top + i), (left + i, top))
            pygame.draw.line(DISPLAYSURF, color, (left + i, top + BOXSIZE - 1), (left + BOXSIZE - 1, top + i))
    elif shape is OVAL:
        pygame.draw.ellipse(DISPLAYSURF, color, (left, top + quarter, BOXSIZE, half))

def drawBoxCovers(board, boxes, coverage):
    # Draws boxes being covered/revealed. "boxes" is a list
    # of two item tuples, which have the x & y spot of the box
    for box in boxes: # get a single x, y tuple pair from boxes
        left, top = leftTopCoordsOfBox(box[0], box[1]) # here we find top-left corner of box pixel coordinates
        pygame.draw.rect(DISPLAYSURF, BGCOLOR, (left, top, BOXSIZE, BOXSIZE))
        shape, color = getShapeAndColor(board, box[0], box[1])
        drawIcon(shape, color, box[0], box[1])
        if coverage > 0: # only draw covers if there is coverage
            pygame.draw.rect(DISPLAYSURF, BOXCOLOR, (left, top, coverage, BOXSIZE))
    pygame.display.update()
    FPSCLOCK.tick(FPS)

def revealBoxesAnimation(board, boxesToReveal):
    # Reveal shape contained by box
    for coverage in range(BOXSIZE, (-REVEALSPEED) - 1, - REVEALSPEED):
        drawBoxCovers(board, boxesToReveal, coverage)

def coverBoxesAnimation(board, boxesToCover):
    # Cover shape contained by box
    for coverage in range(0, BOXSIZE + REVEALSPEED, REVEALSPEED):
        drawBoxCovers(board, boxesToCover, coverage)

def drawBoard(board, revealed):
    # Draws all of the boxes in their covered or revealed state.
    for boxx in range(BOARDWIDTH):
        for boxy in range(BOARDHEIGTH):
            left, top = leftTopCoordsOfBox(boxx, boxy)
            if not revealed[boxx][boxy]:
                # Draw a covered box
                pygame.draw.rect(DISPLAYSURF, BOXCOLOR, (left, top, BOXSIZE, BOXSIZE))
            else:
                # Draw the (revealed) icon
                shape, color = getShapeAndColor(board, boxx, boxy)
                drawIcon(shape, color, boxx, boxy)

def drawHighlightBox(boxx, boxy):
    left, top = leftTopCoordsOfBox(boxx, boxy)
    pygame.draw.rect(DISPLAYSURF, HIGHLIGHTCOLOR, (left-5, top-5, BOXSIZE+10, BOXSIZE+10), 4)

def startGameAnimation(board):
    # randomly reveal the boxes 8 at a time
    coveredBoxes = generateRevealedBoxesData(False)
    boxes = []
    for x in range(BOARDWIDTH):
        for y in range(BOARDHEIGTH):
            boxes.append( (x, y) )
    random.shuffle(boxes)
    boxGroups = splitIntoGroupsOf(8, boxes)

    drawBoard(board, coveredBoxes)
    for boxGroup in boxGroups:
        revealBoxesAnimation(board, boxGroup)
        coverBoxesAnimation(board, boxGroup)

def hasWon(revealedBoxes):
    for i in revealedBoxes: # data structure representing the board as an [x][y] pairs
        if False in i: # This checks for a False value in the x column
            return False
    return True






""" End of helper methods for main """

