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

import pygame, moderngl, struct, random, pygame.gfxdraw, math
from pygame.locals import *

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

pygame.init()

FPS=30
clock = pygame.time.Clock()

VIRTUAL_RES=(320, 240)
REAL_RES=(960, 720)

screen = pygame.Surface(VIRTUAL_RES).convert((255, 65280, 16711680, 0))
pygame.display.set_mode(REAL_RES, DOUBLEBUF|OPENGL)

ctx = moderngl.create_context()

texture_coordinates = [0, 1,  1, 1,
                       0, 0,  1, 0]

world_coordinates = [-1, -1,  1, -1,
                     -1,  1,  1,  1]

render_indices = [0, 1, 2,
                  1, 2, 3]

prog = ctx.program(
    vertex_shader='''
#version 330
in vec2 vert;
in vec2 in_text;
out vec2 v_text;
void main() {
   gl_Position = vec4(vert, 0.0, 1.0);
   v_text = in_text;
}
''',
fragment_shader='''
#version 330
precision mediump float;
uniform sampler2D Texture;

out vec4 color;
in vec2 v_text;
void main() {
  vec2 center = vec2(0.5, 0.5);
  vec2 off_center = v_text - center;

  off_center *= 1.0 + 0.5 * pow(abs(off_center.yx), vec2(5.5));

  vec2 v_text2 = center+off_center;

  if (v_text2.x > 1.0 || v_text2.x < 0.0 ||
      v_text2.y > 1.0 || v_text2.y < 0.0){
    color=vec4(0.0, 0.0, 0.0, 1.0);
  } else {
    color = vec4(texture(Texture, v_text2).rgb, 1.0);
    float fv = fract(v_text2.y * float(textureSize(Texture,0).y));
    fv=min(1.0, 0.8+0.5*min(fv, 1.0-fv));
    color.rgb*=fv;
  }
}
''')

screen_texture = ctx.texture(
    VIRTUAL_RES, 3,
    pygame.image.tostring(screen, "RGB", 1))

screen_texture.repeat_x = False
screen_texture.repeat_y = False

vbo = ctx.buffer(struct.pack('8f', *world_coordinates))
uvmap = ctx.buffer(struct.pack('8f', *texture_coordinates))
ibo= ctx.buffer(struct.pack('6I', *render_indices))

vao_content = [
    (vbo, '2f', 'vert'),
    (uvmap, '2f', 'in_text')
]

vao = ctx.vertex_array(prog, vao_content, ibo)

def render():
    texture_data = screen.get_view('1')
    screen_texture.write(texture_data)
    ctx.clear(14/255,40/255,66/255)
    screen_texture.use()
    vao.render()
    pygame.display.flip()

#MAIN LOOP

done=False

for r in (math.radians(i) for i in range(0,360,10)):
    f = int(math.cos(r)*50)+160
    g = int(math.sin(r)*50)+120
    color = CGA[random.randint(1,15)]
    pygame.draw.circle(screen, color, (f, g), 50, width=1)

render()

while not done:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            quit()
        if event.type == KEYDOWN:
            done = True
