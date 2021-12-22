#!/usr/bin/env python
# I'm going to include the full source up here, and then paste it in with the similar Python/PyGame code.

# 10 SCREEN 7
# 15 CLS
# 20 KEY OFF
# 30 FOR I=0 TO 360 STEP 10
# 40 LET R = I*(3.14/180)
# 50 LET F = COS(R)*50+160
# 60 LET G = SIN(R)*50+100
# 70 COLOR INT(RND*14)+1
# 80 CIRCLE (F,G),50
# 90 NEXT
# 100 COLOR 15
# 110 WHILE INKEY$="": WEND
# 120 SYSTEM : REM FOR COMPLETENESS SAKE

import pygame, random, pygame.gfxdraw, math
from pygame.locals import *

# 10 SCREEN 7
# 15 CLS
# 20 KEY OFF: REM TURNS OFF FUNCTION KEY DISPLAY IN EDITOR

window = pygame.display.set_mode((960, 720))
surf = pygame.Surface((320,240))

# I'm creating a new window that's 3x the size I want, or 960x720.  Then I'm creating a surface that's set
# to be 320x240, or perfectly 4:3 ratio.  This is a little different from the Tandy/PCjr/EGA 320x200x16 color mode.
# At the end I'll use a smooth scaling routine to draw the 320x240 image at 960x720.

# The following was cribbed from Wikipedia.  CGA's 16 colors are 4-bit, with an red, green, and blue bit, and an
# intensity bit.  At the hardware level, though, some bit combinations are altered to change the color palette.

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

# 30 FOR I=0 TO 360 STEP 10
# 40 LET R = I*(3.14/180)
for r in (math.radians(i) for i in range(0,360,10)):
    # A little explanation here.  'for' loops in Python loop through iterables.  Here I have nested iterables.
    # range() is itself an iterable, returning the next number in the list every time the loop repeats until
    # we're done.  The (f for f in x) is shorthand for an iterable; for every item in the range, I'm converting
    # the degree number in integer to radians.
    # In the original GW-BASIC, I'm just converting to radians by multiplying I by pi/180.

    # 50 LET F = COS(R)*50+160
    # 60 LET G = SIN(R)*50+100
    f = int(math.cos(r)*50)+160
    g = int(math.sin(r)*50)+120

    # 70 COLOR INT(RND*14)+1
    # 80 CIRCLE (F,G),50
    # 90 NEXT
    color = CGA[random.randint(1,15)]
    pygame.draw.circle(surf, color, (f, g), 50, width=1)
    # PyGame's circle() routine is a little different but similar.  the first parameter is the surface you're drawing
    # to, the color is obvious from context, and (f, g) are the (x, y) coordinates. If width=0, the circle is filled;
    # otherwise, width sets the number of pixels wide the line is.


# the moment of truth.  smoothscale() scales the surface up to 960x720 and draws it on window.
pygame.transform.smoothscale(surf,(960,720), window)
# Now we're blitting surfac to the window...
window.blit(surf, (960,720))
# ...and page flipping to make it display...
pygame.display.flip()
# ...and running update() to refresh the window.
pygame.display.update()

# 100 COLOR 15
# 110 WHILE INKEY$="": WEND
# 120 SYSTEM : REM FOR COMPLETENESS SAKE

done = False

while not done:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            quit()
        if event.type == KEYDOWN:
            done = True
