#!/usr/bin/env python
import math
import pygame
import sys

WIDTH = 1024
HEIGHT = 1024

RED   = pygame.Color("red")
GREEN = pygame.Color("chartreuse")
BLUE  = pygame.Color("blue")
WHITE = pygame.Color("white")
GREY  = pygame.Color(32,32,32)

# -----------------------------------------------------------------------------
# INIT
# -----------------------------------------------------------------------------
pygame.init()
pygame.display.set_caption("Koch Snowflake")
screen = pygame.display.set_mode((WIDTH, HEIGHT))
screen.fill((0,0,0))


# -----------------------------------------------------------------------------
# GRID
# -----------------------------------------------------------------------------
pygame.draw.line(screen, GREY, (WIDTH/2,0), (WIDTH/2,HEIGHT))
pygame.draw.line(screen, GREY, (0,HEIGHT/2), (WIDTH,HEIGHT/2))

pygame.draw.line(screen, GREY, (0,0), (WIDTH,HEIGHT))
pygame.draw.line(screen, GREY, (WIDTH, 0), (0,HEIGHT))


# -----------------------------------------------------------------------------
# MAIN
# TODO: compute points relative to base line
# -----------------------------------------------------------------------------
segment_len = WIDTH / 3

p1 = (0,             HEIGHT/2)
p2 = (segment_len,   HEIGHT/2)
p3 = (segment_len*2, HEIGHT/2)
p4 = (segment_len*3, HEIGHT/2)

b = segment_len / 2
c = segment_len
a2 = c*c - b*b
a = math.sqrt(a2)

px = (segment_len + (segment_len/2), (HEIGHT/2) - a)

pygame.draw.lines(
    screen, GREEN, False,
    [
        p1,p2,px,p3,p4
    ]
)

# -----------------------------------------------------------------------------
# WAIT TO END
# -----------------------------------------------------------------------------
pygame.display.flip()
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()
# -----------------------------------------------------------------------------
