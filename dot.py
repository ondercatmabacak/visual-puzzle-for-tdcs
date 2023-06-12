import pygame as pg
from pygame.locals import *

SIZE = (800, 600)
BGCOL = (128, 128, 128)
STIMCOL = (80, 255, 80)

screen = pg.display.set_mode((SIZE), HWSURFACE | DOUBLEBUF)
screen.fill(BGCOL)

surf = pg.Surface((200, 200), flags=HWSURFACE)
surf.fill(BGCOL)

pg.draw.circle(surf, STIMCOL, (10, 20, 40, 50))
pg.draw.cricle(surf, STIMCOL,  (60, 70, 80, 90))

screen.blit(surf, (100, 100))

pg.display.flip()

running = True
while running:
    surf = pg.transform.rotate(surf, -1) # updating rotation on the surface
    screen.blit(surf, (100, 100)) #bliting the resulting image every frame
    pg.display.flip()