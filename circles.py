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

import pygame as pg
import moderngl
import crt
import math, random

view_width, view_height = 320, 240
screen_width, screen_height = 960, 720

pg.init()
screen = pg.display.set_mode((screen_width, screen_height), pg.DOUBLEBUF | pg.OPENGL)

surf = pg.Surface((view_width, view_height), flags=pg.SRCALPHA)

crt_processor = crt.CRTProcessor(
    (view_width, view_height), (screen_width, screen_height)
)

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
    "#FFFFFF",
]

circle_positions = []

circle_colors = [CGA[random.randint(1, 15)] for _ in circle_positions]

clock = pg.time.Clock()
done = False
redraw = True

while not done:
    for event in pg.event.get():
        if event.type == pg.QUIT:
            done = True
        elif event.type == pg.KEYDOWN:
            redraw = True

    surf.fill((0, 0, 0, 255))
    if redraw:
        for r in (math.radians(i) for i in range(0, 360, 10)):
            f = int(math.cos(r) * 50) + 160
            g = int(math.sin(r) * 50) + 120
            c = CGA[random.randint(1, 15)]
            pg.draw.circle(surf, c, (f, g), 50, width=1)

        crt_processor.ctx.clear(0, 0, 0)

        crt_processor.render(surf)

        pg.display.flip()
        clock.tick(60)
        redraw = False

pg.quit()
