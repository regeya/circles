#!/usr/bin/env python

import pygame, random, pygame.gfxdraw, math
from pygame.locals import *

window = pygame.display.set_mode((960, 720))

surf = pygame.Surface((320,240))

CGA = [
    "#000000",
    "#0000AA",
    "#00AA00",
    "#00AAAA",
    "#AA0000",
    "#AA00AA",
    "#AA5500",
    "#AAAAAA",
    "#555555",
    "#5555FF",
    "#55FF55",
    "#55FFFF",
    "#FF5555",
    "#FF55FF",
    "#FFFF55",
    "#FFFFFF"
] # 16 colors of the CGA palette.

for i in (math.radians(j) for j in range(0,360,10)):
    f = int(math.cos(i)*50)+160
    g = int(math.sin(i)*50)+120
    color = CGA[random.randint(1,15)]
    pygame.draw.circle(surf, color, (f, g), 50, width=1)

pygame.transform.smoothscale(surf,(960,720), window)
window.blit(surf, (960,720))
pygame.display.flip()
pygame.display.update()

done = False

while not done:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            quit()
        if event.type == KEYDOWN:
            if event.key == K_ESCAPE:
                done = True
