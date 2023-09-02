#!/usr/bin/env python

import pygame
import sys
import time

from color import Color
from mandelbrot import Mandlebrot

DISPLAY_WIDTH = 640
DISPLAY_HEIGHT = 480

pygame.init()

pygame.display.set_caption("Mandlebrot")
screen = pygame.display.set_mode((DISPLAY_WIDTH, DISPLAY_HEIGHT))
screen.fill((0,0,0))

# Animate
curr_iter = 1
iter_inc = 1
max_iter = 35

# Detailed
# curr_iter = 50
# iter_inc = 5
# max_iter = 50

# m = Mandlebrot(-2, 1, -1, 1)
# m = Mandlebrot(-2,1,-1.25,1.25)
m = Mandlebrot(-1,0,-0.75,0.75)

Color.set_pallete(Color.RAINBOW)
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()

    if curr_iter <= max_iter:
        curr_iter += iter_inc

        m.compute(curr_iter, screen)

        # pygame.draw.rect(screen, Color.RED, pygame.Rect((DISPLAY_WIDTH/2)-5, (DISPLAY_HEIGHT/2)-5, 10, 10))
        pygame.draw.line(screen, Color.RED, (DISPLAY_WIDTH/2,DISPLAY_HEIGHT/2), (DISPLAY_WIDTH/2,DISPLAY_HEIGHT/2))

        pygame.display.flip()
        print("%d/%d" % (curr_iter, max_iter))

        Color.rotate_pallete()

        # time.sleep(0.25)
