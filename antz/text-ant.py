#!/usr/bin/env python
import random

from antz.ant import Ant

# WIDTH = 64
# HEIGHT = 64

N = (0, -1)
NE = (1, -1)
E = (1, 0)
SE = (1, 1)
S = (0, 1)
SW = (-1, 1)
W = (-1, 0)
NW = (-1, -1)


ant1 = Ant(1, 16,32)
ant1.dx = NE[0]
ant1.dy = NE[1]

ant2 = Ant(2, 21, 30)
ant2.dx = N[0]
ant2.dy = N[1]

antz = [ant1, ant2]


def look_for_trail(ant):
    ant.following = None
    for other_ant in antz:
        if other_ant is not ant:
            if ant.on_trail_of(other_ant):
                ant.follow(other_ant)

def move_one(ant):
    ant.move()
    look_for_trail(ant)

def move_many(ant):
    distance = 2 #random.randint(1, 2)
    for _ in range(distance):
        move_one(ant)

day = 1
while True:
    print(f"-- Day #{day} --")

    for ant in antz:
        if ant.is_camping:
            ant.camp()
        else:
            # move_one(ant)
            move_many(ant)

            if day % 3 == 0:
                if ant.following is None:
                    ant.set_up_camp()

        print(ant)


    if ant1.location() == ant2.location():
        print(f"Reunited!")
        break

    key = input()
    if key == 'q':
        break

    day += 1
