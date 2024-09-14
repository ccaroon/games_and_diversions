import curses
import math
import random
import time

import numpy as np
from scipy.spatial.distance import squareform, pdist
from numpy.linalg import norm

class BoidSimulation1:
    MIN_DISTANCE = 1.0
    MAX_RULE_VELO = 0.03
    MAX_VELOCITY = .55

    COLOR_BOID = 1
    COLOR_BLACK_GREEN = 2
    COLOR_DEBUG = 3

    def __init__(self, stdscr, count, **kwargs):
        curses.init_pair(self.COLOR_BOID,
                         curses.COLOR_GREEN, curses.COLOR_BLACK)
        curses.init_pair(self.COLOR_BLACK_GREEN,
                         curses.COLOR_BLACK, curses.COLOR_GREEN)
        curses.init_pair(self.COLOR_DEBUG,
                         curses.COLOR_RED, curses.COLOR_BLACK)

        self.__count = count
        self.__marker = kwargs.get("marker", "·")
        self.__iteration_count = kwargs.get("iterations", 100)
        self.__delay = kwargs.get("delay", 0.10)
        self.__debug = kwargs.get("debug", False)

        self.__screen = stdscr
        self.__screen.nodelay(True)

        self.__width = curses.COLS - 2
        self.__height = curses.LINES - 1

        self.__seed_center()
        # self.__seed_random()

        angles = 2 * math.pi * np.random.rand(count)
        self.vel = np.array(list(zip(np.cos(angles), np.sin(angles))))

        self.__iteration = 1

    def __seed_center(self):
        # position of each boid
        # ...each being a random distance from the center up to 10 units away
        # ...represented a `count` pairs of (x,y) coordinates
        self.__boids = [self.__width / 2.0, self.__height / 2.0] + 5 * np.random.rand(2 * self.__count).reshape(self.__count, 2)

    def __seed_random(self):
        # self.__boids = [0.0, 0.0] + np.random.randint(43, size=2 * self.__count).reshape(self.__count, 2)
        self.__boids = [self.__width, self.__height] * np.random.rand(2 * self.__count).reshape(self.__count, 2)

    def apply_boundary_wrap(self):
        delta_r = 0.99

        for coord in self.__boids:
            # Check Col
            if coord[0] > self.__width + delta_r:
                coord[0] = -delta_r

            if coord[0] < -delta_r:
                coord[0] = self.__width + delta_r

            # Check Row
            if coord[1] > self.__height + delta_r:
                coord[1] = -delta_r

            if coord[1] < -delta_r:
                coord[1] = self.__height + delta_r

    def apply_boundary_reflect(self):
        delta_r = 0.0
        # reverse_flock = False
        count = 0
        bad_boids = []
        for idx, coord in enumerate(self.__boids):
            boid_ok = True

            # Check Col
            if coord[0] > self.__width:
                coord[0] = self.__width - delta_r
                reverse_flock = True
                count += 1
                # self.vel[idx][1] *= -1
                boid_ok = False

            if coord[0] < 0:
                coord[0] = delta_r
                # reverse_flock = True
                count += 1
                # self.vel[idx][1] *= -1
                boid_ok = False

            # Check Row
            if coord[1] > self.__height:
                coord[1] = self.__height - delta_r
                # reverse_flock = True
                count += 1
                # self.vel[idx][0] *= -1
                boid_ok = False

            if coord[1] < 0:
                coord[1] = delta_r
                # reverse_flock = True
                count += 1
                # self.vel[idx][0] *= -1
                boid_ok = False

            if not boid_ok:
                bad_boids.append(idx)

        # If at least X hit boundary, reverse flock
        if count > (self.__count * .25):
            # for bidx in bad_boids:
                # self.vel[bidx][0] *= -1
                # self.vel[bidx][1] *= -1
            self.vel *= -1
            # self.vel[idx][0] *= -1
            # self.vel[idx][1] *= -1

    def apply_rules(self):
        # get pair-wise distances
        dist_matrix = squareform(pdist(self.__boids))

        # rule #1: separation
        D = dist_matrix < self.MIN_DISTANCE
        vel = self.__boids * D.sum(axis=1).reshape(self.__count, 1) - D.dot(self.__boids)
        self.limit(vel, self.MAX_RULE_VELO)

        D = dist_matrix < 50.0

        # rule #2 - alignment
        vel2 = D.dot(self.vel)
        self.limit(vel2, self.MAX_RULE_VELO)
        vel += vel2

        # rule #3 - cohesion
        vel3 = D.dot(self.__boids) - self.__boids
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

    def add(self, loc:tuple=None):
        # Add a new Boid
        row = loc[0] or (self.__height // 2)
        col = loc[1] or (self.__width // 2)
        self.__boids = np.concatenate(
            (self.__boids, np.array([[col,row]])),
            axis=0
        )
        angles = 2 * math.pi * np.random.rand(1)
        v = np.array(list(zip(np.sin(angles), np.cos(angles))))
        self.vel = np.concatenate((self.vel, v), axis=0)

        self.__count += 1

    def scatter(self, loc:tuple=None):
        row = loc[0] or random.randint(0, self.__height)
        col = loc[1] or random.randint(0, self.__width)
        self.vel += 0.1 * (self.__boids - np.array([[col, row]]))

    def tick(self):
        self.vel += self.apply_rules()
        self.limit(self.vel, self.MAX_VELOCITY)
        self.__boids += self.vel
        self.apply_boundary_reflect()

        self.__boids.reshape(2*self.__count)[::2],
        self.__boids.reshape(2*self.__count)[1::2]

        self.__iteration += 1

    def display(self):
        self.__screen.erase()

        line = 0
        for idx, boid in enumerate(self.__boids):
            col = int(boid[0])
            row = int(boid[1])
            marker = idx if self.__debug else self.__marker
            self.__screen.addstr(row, col, f"{marker}", curses.color_pair(self.COLOR_BOID))

            if self.__debug:
                self.__screen.addstr(line, 0, f"({row},{col})", curses.color_pair(self.COLOR_BOID))
                line += 1

        if self.__debug:
            for vel in self.vel:
                self.__screen.addstr(line, 0, f"{vel}", curses.color_pair(self.COLOR_DEBUG))
                line += 1

        self.__screen.addstr(
            self.__height, 0,
            f"Boids| {self.__width}x{self.__height} | {self.__count} | {self.__iteration}/{self.__iteration_count} | ",
            curses.color_pair(self.COLOR_BLACK_GREEN)
        )

        self.__screen.refresh()

    def run(self):
        curses.mousemask(curses.ALL_MOUSE_EVENTS)
        for _ in range(self.__iteration_count):
            self.display()
            self.tick()

            input = self.__screen.getch()
            if input == ord("q"):
                break
            elif input == ord("s"):
                self.scatter()
            elif input == ord("b"):
                self.add()
            elif input == curses.KEY_MOUSE:
                id,x,y,_,button = curses.getmouse()
                if button & curses.BUTTON1_CLICKED:
                    self.add((y,x))
                if button & curses.BUTTON2_CLICKED:
                    self.scatter((y,x))

            time.sleep(self.__delay)
