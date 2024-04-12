import random
import time

from abc import ABC, abstractmethod

from .ant import Ant


class AntzSimulation(ABC):

    MAX_DISTANCE = 3

    # TODO: keep these?
    N = (0, -1)
    NE = (1, -1)
    E = (1, 0)
    SE = (1, 1)
    S = (0, 1)
    SW = (-1, 1)
    W = (-1, 0)
    NW = (-1, -1)

    def __init__(self, width, height, **kwargs):
        self._width = width
        self._height = height

        self._count = kwargs.get("count", 2)
        self._day_len = kwargs.get("day_len", 0.10)
        self._max_days = kwargs.get("max_days", 500)
        self._ant_marker = kwargs.get("ant_marker", "●")
        self._trail_marker = kwargs.get("trail_marker", "·")
        self._camp_marker = kwargs.get("camp_marker", "⊙")
        self._debug = kwargs.get("debug", False)

        self._day = 1
        self._simulation_complete = False

        self._antz = []
        if self._debug:
            self.__debug_init_antz()
        else:
            self.__init_antz()

    def __debug_init_antz(self):
        self._antz.append(Ant(1, 16, 32))
        self._antz[0].dx = self.NE[0]
        self._antz[0].dy = self.NE[1]

        self._antz.append(Ant(2, 21, 30))
        self._antz[1].dx = self.N[0]
        self._antz[1].dy = self.N[1]

    def __init_antz(self):
        for idx in range(self._count):
            self._antz.append(
                Ant(
                    idx + 1,
                    random.randint(0, self._width),
                    random.randint(0, self._height)
                )
            )

    # TODO: Define Rule Methods
    # - [x] move
    #   - [x] move for 1 day
    #   - [x] camp for 3 days
    #   - [x] if camping, dont move
    # - [x] check bounds
    # - check if on another antz trail
    #   - if so, follow the trail
    #   - no camping
    # - check if in another antz camp site
    #   - if so, leave in same direction

    def __check_bounds(self, ant):
        if ant.x < 0:
            ant.x = self._width

        if ant.x > self._width:
            ant.x = 0

        if ant.y < 0:
            ant.y = self._height

        if ant.y > self._height:
            ant.y = 0

    def __look_for_trail(self, ant):
        for other_ant in self._antz:
            if other_ant is not ant:
                if ant.on_trail_of(other_ant):
                    ant.follow(other_ant)

    def tick(self):
        for ant in self._antz:
            if ant.is_camping:
                ant.camp()
            else:
                if not self._debug:
                    ant.choose_direction()
                # Move in chosen direction for X distance
                # TODO: fix random distance
                distance = 1  # random.randint(1, self.MAX_DISTANCE)
                for _ in range(distance):
                    ant.move()
                    self.__look_for_trail(ant)
                    self.__check_bounds(ant)

                # Set up Camp every 3 days
                if self._day % 3 == 0:
                    if ant.following is None:
                        ant.set_up_camp()

        # They have been reunited. Stop the simulation.
        if self._antz[0].location() == self._antz[1].location():
            self._simulation_complete = True

        self._day += 1

    @abstractmethod
    def _process_input(self):
        pass

    @abstractmethod
    def display(self):
        pass

    def run(self):
        self.display()

        while self._day < self._max_days and not self._simulation_complete:
            self.tick()
            self.display()

            self._process_input()

            time.sleep(self._day_len)
