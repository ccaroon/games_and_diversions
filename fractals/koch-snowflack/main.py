#!/usr/bin/env python
import pygame
import sys
import time

WIDTH = 1024
HEIGHT = 768

RED = (255,0,0)
GREEN = (96,255,0)

pygame.init()

pygame.display.set_caption("Koch Snowflake")
screen = pygame.display.set_mode((WIDTH, HEIGHT))
screen.fill((0,0,0))

points = []

for y in range(0,HEIGHT, 10):
    p = ((0,0), (WIDTH, y))
    points.append(p)

# print(points)

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()

    if len(points) > 0:
        pt = points.pop()
        pygame.draw.line(
            screen, GREEN,
            pt[0], pt[1]
        )

        pygame.display.flip()
        time.sleep(0.05)
