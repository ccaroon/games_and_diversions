#!/usr/bin/env python
import curses
import math
import time

import numpy as np
from scipy.spatial.distance import squareform, pdist
from numpy.linalg import norm


class Simulation:
    MIN_DISTANCE = 15.0
    MAX_RULE_VELO = 0.03
    MAX_VELOCITY = 0.75

    COLOR_BOID = 1
    COLOR_BLACK_GREEN = 2
    COLOR_DEBUG = 3

    def __init__(self, stdscr, count):
        curses.init_pair(self.COLOR_BOID,
                         curses.COLOR_GREEN, curses.COLOR_BLACK)
        curses.init_pair(self.COLOR_BLACK_GREEN,
                         curses.COLOR_BLACK, curses.COLOR_GREEN)
        curses.init_pair(self.COLOR_DEBUG,
                         curses.COLOR_RED, curses.COLOR_BLACK)

        self.__screen = stdscr

        self.WIDTH = curses.COLS
        self.HEIGHT = curses.LINES

        # position of each boid
        # ...each being a random distance from the center up to 10 units away
        # ...represented a `count` pairs of (x,y) coordinates
        self.pos = [self.WIDTH / 2.0, self.HEIGHT / 2.0] + 15 * np.random.rand(2 * count).reshape(count, 2)

        angles = 2 * math.pi * np.random.rand(count)
        self.vel = np.array(list(zip(np.cos(angles), np.sin(angles))))
        self.count = count

    def apply_boundary(self):
        delta_r = 2.0

        for coord in self.pos:
            if coord[0] > self.WIDTH + delta_r:
                coord[0] = -delta_r

            if coord[0] < -delta_r:
                coord[0] = self.WIDTH + delta_r

            if coord[1] > self.HEIGHT + delta_r:
                coord[1] = -delta_r

            if coord[1] < -delta_r:
                coord[1] = self.HEIGHT + delta_r

    def apply_rules(self):
        # get pair-wise distances
        dist_matrix = squareform(pdist(self.pos))

        # rule #1: separation
        D = dist_matrix < self.MIN_DISTANCE
        vel = self.pos * D.sum(axis=1).reshape(self.count, 1) - D.dot(self.pos)
        self.limit(vel, self.MAX_RULE_VELO)

        D = dist_matrix < 50.0

        # rule #2 - alignment
        vel2 = D.dot(self.vel)
        self.limit(vel2, self.MAX_RULE_VELO)
        vel += vel2

        # rule #3 - cohesion
        vel3 = D.dot(self.pos) - self.pos
        self.limit(vel3, self.MAX_RULE_VELO)
        vel += vel3

        return vel

    def limit(self, vel, max_val):
        for vec in vel:
            self.limit_vec(vec, max_val)

    def limit_vec(self, vec, max_val):
        mag = norm(vec)
        if mag > max_val:
            vec[0], vec[1] = vec[0]*max_val/mag, vec[1]*max_val/mag

    def button_press(self, event):
        if event.button == 1:
            self.pos = np.concatenate(
                (self.pos, np.array([[event.xdata, event.ydata]])),
                axis=0
            )
            angles = 2 * math.pi * np.random.rand(1)
            v = np.array(list(zip(np.sin(angles), np.cos(angles))))
            self.vel = np.concatenate((self.vel, v), axis=0)

            self.count += 1
        elif event.button == 3:
            self.vel += 0.1 * (self.pos - np.array([[event.xdata, event.ydata]]))

    def tick(self):
        self.vel += self.apply_rules()
        self.limit(self.vel, self.MAX_VELOCITY)
        self.pos += self.vel
        self.apply_boundary()

        self.pos.reshape(2*self.count)[::2],
        self.pos.reshape(2*self.count)[1::2]

    def display(self):
        self.__screen.addstr(0, 70, "Craig N. Caroon",curses.color_pair(self.COLOR_DEBUG))
        # line = 1
        for boid in self.pos:
            col = int(boid[0])
            row = int(boid[1])
            self.__screen.addstr(row, col, ".", curses.color_pair(self.COLOR_BOID))

            # self.__screen.addstr(line, 0, f"{row},{col}", curses.color_pair(self.COLOR_DEBUG))
            # line += 1

        self.__screen.refresh()

    def run(self):
        # self.display()
        # self.tick()
        # time.sleep(1)
        # self.display()
        for _ in range(100):
            self.display()
            self.tick()
            time.sleep(0.25)
