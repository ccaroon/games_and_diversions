import curses
import random
import time

from .ant import Ant

class AntzSimulation:
    COLOR_ANT1 = 1
    COLOR_ANT2 = 2
    COLOR_INFO_BAR = 3
    COLOR_DEBUG = 4

    MAX_DISTANCE = 3

    def __init__(self, stdscr, **kwargs):
        self.__screen = stdscr
        self.__screen.nodelay(True)

        self.__width = curses.COLS - 1
        # -1 extra for info line at bottom
        self.__height = curses.LINES - 2

        curses.init_pair(self.COLOR_ANT1,
                         curses.COLOR_RED, curses.COLOR_BLACK)
        curses.init_pair(self.COLOR_ANT2,
                         curses.COLOR_WHITE, curses.COLOR_BLACK)
        curses.init_pair(self.COLOR_INFO_BAR,
                         curses.COLOR_BLACK, curses.COLOR_WHITE)
        curses.init_pair(self.COLOR_DEBUG,
                         curses.COLOR_BLACK, curses.COLOR_RED)

        self.__show_trails = True
        self.__count = kwargs.get("count", 2)
        self.__day_len = kwargs.get("day_len", 0.10)
        self.__max_days = kwargs.get("max_days", 500)
        self.__ant_marker = kwargs.get("ant_marker", "●")
        self.__trail_marker = kwargs.get("trail_marker", "·")
        self.__camp_marker = kwargs.get("camp_marker", "⊙")
        self.__debug = kwargs.get("debug", False)

        self.__day = 1

        self.__antz = []
        self.__init_antz()

    def __init_antz(self):
        for idx in range(self.__count):
            self.__antz.append(
                Ant(
                    idx,
                    random.randint(0, self.__width),
                    random.randint(0, self.__height)
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
            ant.x = self.__width

        if ant.x > self.__width:
            ant.x = 0

        if ant.y < 0:
            ant.y = self.__height

        if ant.y > self.__height:
            ant.y = 0

    def __look_for_trail(self, ant):
        ant.following = None
        for other_ant in self.__antz:
            if other_ant is not ant:
                if ant.on_trail_of(other_ant):
                    ant.follow(other_ant)

    def tick(self):
        for ant in self.__antz:
            if ant.is_camping:
                ant.camp()
            else:
                ant.choose_direction()
                # Move in chosen direction for X distance
                distance = random.randint(1, self.MAX_DISTANCE)
                for _ in range(distance):
                    ant.move()
                    self.__look_for_trail(ant)
                    self.__check_bounds(ant)

                # Set up Camp every 3 days
                if self.__day % 3 == 0:
                    if ant.following is None:
                        ant.set_up_camp()

        self.__day += 1


    def display(self):
        self.__screen.erase()

        line = 0
        status = "LOST"
        for ant in self.__antz:
            row = ant.y
            col = ant.x
            marker = ant.id if self.__debug else self.__ant_marker

            if ant.following is not None:
                status = f"Ant#{ant.id} --> Ant#{ant.following.id}"

            color = self.COLOR_ANT1 if ant.id % 2 == 0 else self.COLOR_ANT2

            if self.__debug:
                self.__screen.addstr(line, 0, f"{ant.id}) ({row},{col}) -> [{ant.dx},{ant.dy}]", curses.color_pair(color))
                line += 1

            # Display Trail first so that it does not hide the antz current location
            if self.__show_trails:
                for tmark in ant.trail:
                    trow = tmark.y
                    tcol = tmark.x
                    self.__screen.addstr(trow, tcol, f"{self.__trail_marker}", curses.color_pair(color))

            # Display camp sites
            for site in ant.camp_sites:
                crow = site[1]
                ccol = site[0]
                self.__screen.addstr(crow, ccol, f"{self.__camp_marker}", curses.color_pair(color))

            # Lastly, display ant location
            self.__screen.addstr(row, col, f"{marker}", curses.color_pair(color))

        self.__screen.addstr(
            self.__height + 1, 0,
            f"Antz | {self.__width}x{self.__height} | {self.__count} | Day #{self.__day}/{self.__max_days} | {self.__day_len} | {status} |",
            curses.color_pair(self.COLOR_INFO_BAR)
        )

        self.__screen.refresh()

    def run(self):
        for _ in range(self.__max_days):
            self.display()
            self.tick()

            input = self.__screen.getch()
            if input == ord("q"):
                break
            elif input == ord("+"):
                self.__day_len -= 0.10
                if self.__day_len < 0.10:
                    self.__day_len = 0.10
            elif input == ord("-"):
                self.__day_len += 0.10
            elif input == ord("S"):
                self.__day_len = 1.0
            elif input == ord("t"):
                self.__show_trails = False if self.__show_trails else True

            time.sleep(self.__day_len)
