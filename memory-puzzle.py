import random, pygame, sys
from pygame import *

FPS = 30 # frames per second, the general speed of the program
WINDOWWIDTH = 640 # size of window's width in pixels
WINDOWHEIGHT = 480 # size of window's height in pixels
REVEALSPEED = 8 # speed boxes' sliding reveals and covers
BOXSIZE = 40 # size of box height & width in pixels
GAPSIZE = 10 # size of gap between boxes in pixels
BOARDWIDTH = 10 # number of columns of icons
BOARDHEIGHT = 7 # number of rowns of icons
assert (BOARDWIDTH * BOARDHEIGHT) % 2 == 0, 'Board needs to have an even number of boxes for pairs of matches.'
XMARGIN = int((WINDOWWIDTH - (BOARDWIDTH * (BOXSIZE + GAPSIZE))) / 2)
YMARGIN = int((WINDOWHEIGHT - (BOARDHEIGHT * (BOXSIZE + GAPSIZE))) / 2)

#
GRAY     = (100, 100, 100)
NAVYBLUE = ( 60,  60, 100)
WHITE    = (255, 255, 255)
RED      = (255,   0,   0)
GREEN    = (  0, 255,   0)
BLUE     = (  0,   0, 255)
YELLOW   = (255, 255,   0)
ORANGE   = (255, 128,   0)
PURPLE   = (255,   0, 255)
CYAN     = (  0, 255, 255)

BGCOLOR = NAVYBLUE
LIGHTBGCOLOR = GRAY
BOXCOLOR = WHITE
HIGHLIGHTCOLOR = BLUE

DONUT, SQUARE, DIAMOND, LINES, OVAL = 1, 2, 3, 4, 5

ALLCOLORS = (RED, GREEN, BLUE, YELLOW, ORANGE, PURPLE, CYAN)
ALLSHAPES = (DONUT, SQUARE, DIAMOND, LINES, OVAL)
assert len(ALLCOLORS) * len(ALLSHAPES) * 2 >= BOARDWIDTH * BOARDHEIGHT, 'Board is too big for the number of shapes/colors defined.'

def main():
	global fpsClock, DISPLAYSURF
	pygame.init()
	fpsClock = pygame.time.Clock()
	DISPLAYSURF = pygame.display.set_mode((WINDOWWIDTH, WINDOWHEIGHT))

	mousex, mousey = 0, 0

	pygame.display.set_caption('Memory Game')

	mainBoard = getRandomizedBoard()
	revealedBoxes = generateRevealedBoxesData(False)

	firstSelection = None

	DISPLAYSURF.fill(BGCOLOR)
	startGameAnimation(mainBoard)

	while True:
		mouseClicked = False

		DISPLAYSURF.fill(BGCOLOR)
		drawBoard(mainBoard, revealedBoxes)

		for event in pygame.event.get():
			if event.type == QUIT or (event.type == KEYUP and event.key == K_ESCAPE):
				pygame.quit()
				sys.exit()
			elif event.type == MOUSEMOTION:
				mousex, mousey = event.pos
			elif event.type == MOUSEBUTTONUP:
				mousex, mousey = event.pos
				mouseClicked = True

			boxx, boxy = getBoxAtPixel(mousex, mousey)
			if boxx != None and boxy != None:
				if not revealedBoxes[boxx][boxy]:
					drawHighlightBox(boxx, boxy)
				if not revealedBoxes[boxx][boxy]:
					revealBoxesAnimation(mainboard, [(boxx, boxy)])
					revealedBoxes[boxx][boxy] = True
					if firstSelection == None:
						firstSelection = (boxx, boxy)
					else:
						icon1shape, icon1color = getShapeAndColor(mainBoard, firstSelection[0], firstSelection[1])
						icon2shape, icon2color = getShapeAndColor(mainBoard, boxx, boxy)
						if icon1shape != icon2shape or icon1color != icon2color:
							pygame.time.wait(1000)
							coverBoxesAnimation(mainBoard, [(firstSelection[0], firstSelection[1]), (boxx, boxy)])
							revealedBoxes[fisrtSelection[0], firstSelection[1]] = False
							revealedBoxes[boxx][boxy] = False
						elif hasWon(revealedBoxes):
							gameWonAnimation(mainBoard)
							pygame.time.wait(2000)

							mainBoard = getRandomizedBoard()
							revealedBoxes = generateRevealedBoxesData(False)

							drawBoard(mainBoard, revealedBoxes)
							pygame.display.update()
							pygame.time.wait(1000)

							startGameAnimation(mainBoard)
						firstSelection = None
					pygame.display.update()
					fpsClock.tick(FPS)

def generateRevealedBoxesData(val):
	return [[val] * BOARDHEIGHT for i in range(BOARDWIDTH)]	

def getRandomizedBoard():
	icons = [(shape, color) for color in ALLCOLORS for shape in ALLSHAPES]
	random.shuffle(icons)
	numIconsUsed = int(BOARDWIDTH * BOARDHEIGHT / 2)
	icons = icons[:numIconsUsed] * 2
	random.suffle(icons)

	

if __name__ == '__main__':
	main()
