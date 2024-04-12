import curses

from .simulation import AntzSimulation


class AntzCurses(AntzSimulation):
    COLOR_ANT1 = 1
    COLOR_ANT2 = 2
    COLOR_INFO_BAR = 3
    COLOR_DEBUG = 4

    def __init__(self, stdscr, **kwargs):
        self.__screen = stdscr
        self.__screen.nodelay(True)

        curses.init_pair(self.COLOR_ANT1,
                         curses.COLOR_RED, curses.COLOR_BLACK)
        curses.init_pair(self.COLOR_ANT2,
                         curses.COLOR_WHITE, curses.COLOR_BLACK)
        curses.init_pair(self.COLOR_INFO_BAR,
                         curses.COLOR_BLACK, curses.COLOR_WHITE)
        curses.init_pair(self.COLOR_DEBUG,
                         curses.COLOR_BLACK, curses.COLOR_RED)

        self.__show_trails = True
        width = curses.COLS - 1
        # -1 extra for info line at bottom
        height = curses.LINES - 2
        super().__init__(width, height, **kwargs)

    def display(self):
        self.__screen.erase()

        for ant in self._antz:
            row = ant.y
            col = ant.x
            marker = ant.uid if self._debug else self._ant_marker

            color = self.COLOR_ANT1 if ant.uid % 2 == 0 else self.COLOR_ANT2

            # Display Trail first so that it does not hide the antz current location
            if self.__show_trails:
                for tmark in ant.trail:
                    trow = tmark.y
                    tcol = tmark.x
                    self.__screen.addstr(trow, tcol, f"{self._trail_marker}", curses.color_pair(color))

            # Display camp sites
            for site in ant.camp_sites:
                crow = site[1]
                ccol = site[0]
                self.__screen.addstr(crow, ccol, f"{self._camp_marker}", curses.color_pair(color))

            # Lastly, display ant location
            self.__screen.addstr(row, col, f"{marker}", curses.color_pair(color))

            if self._debug:
                ant_info = f"{ant} {ant.status()}"
                self.__screen.addstr(ant.uid, 0, ant_info, curses.color_pair(color))

        self.__screen.addstr(
            self._height + 1, 0,
            f"Antz | {self._width}x{self._height} | {self._count} | Day #{self._day}/{self._max_days} | {self._day_len} | ",
            curses.color_pair(self.COLOR_INFO_BAR)
        )

        self.__screen.refresh()

    def _process_input(self):
        key = self.__screen.getch()
        if key == ord("q"):
            self._simulation_complete = True
        elif key == ord("+"):
            self._day_len -= 0.10
            if self._day_len < 0.10:
                self._day_len = 0.10
        elif key == ord("-"):
            self._day_len += 0.10
        elif key == ord("S"):
            self._day_len = 1.0
        elif key == ord("t"):
            self.__show_trails = False if self.__show_trails else True
