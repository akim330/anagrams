import pygame, sys
from pygame.locals import *

pygame.init()

DISPLAYSURF = pygame.display.set_mode((500,400), 0, 32)
pygame.display.set_caption('Drawing')

BLACK = (0,0,0)
WHITE = (255, 255, 255)
RED = (255, 0 , 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)

DISPLAYSURF.fill(WHITE)
pygame.draw.polygon(DISPLAYSURF, GREEN, ((146,0), (291, 106), (236, 277), (56, 277), (0, 106)))
pygame.draw.line(DISPLAYSURF, BLUE, (60, 60), (120, 60), 10)
pygame.draw.line(DISPLAYSURF, RED, (60, 100), (120, 100), 1)
pygame.draw.circle(DISPLAYSURF, BLUE, (60, 100), 30, 0)
pygame.draw.circle(DISPLAYSURF, BLUE, (300, 50), 20, 0)

pixObj = pygame.PixelArray(DISPLAYSURF)
pixObj[121][100] = BLACK
del pixObj

while True:
    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            sys.exit()
    pygame.display.update()

