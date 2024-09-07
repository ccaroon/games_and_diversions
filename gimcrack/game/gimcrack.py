import copy
import curses
# import re
import time
import random

from .gem import Gem

class GimCrack:
    """ A Simple, Self-Playing Gem Matching Game """

    GEM_DEFS = {
        "RED":     ("⬢", curses.COLOR_RED),
        "YELLOW":  ("⬢", curses.COLOR_YELLOW),
        "GREEN":   ("⭓", curses.COLOR_GREEN),
        "CYAN":    ("⬟", curses.COLOR_CYAN),
        "BLUE":    ("⬣", curses.COLOR_BLUE),
        "MAGENTA": ("■", curses.COLOR_MAGENTA),
        "WHITE":   ("⬤", curses.COLOR_WHITE)
    }
    # GEM_DEFS = {
    #     "RED":     ("X", curses.COLOR_RED),
    #     "YELLOW":  ("X", curses.COLOR_YELLOW),
    #     "GREEN":   ("X", curses.COLOR_GREEN),
    #     "CYAN":    ("X", curses.COLOR_CYAN),
    #     "BLUE":    ("X", curses.COLOR_BLUE),
    #     "MAGENTA": ("X", curses.COLOR_MAGENTA),
    #     "WHITE":   ("X", curses.COLOR_WHITE)
    # }
    GEMS = {}

    def __init__(self, stdscr, width, height, **kwargs):
        # Hide the cursor / make it invisible
        curses.curs_set(0)
        self.__screen = stdscr

        self.__spacing = 1
        self.__width = width
        if self.__width == -1:
            self.__width = curses.COLS // self.__spacing

        self.__height = height
        if self.__height == -1:
            # -1 for info line
            self.__height = curses.LINES - 1

        # COLS // 2 b/c a ' ' is printed between chars
        if self.__height > curses.LINES or self.__width > curses.COLS // self.__spacing:
            raise ValueError(f"Screen too small: Max Width: {curses.COLS // self.__spacing} | Max Height: {curses.LINES-1}")

        self.__move_count = 1
        self.__max_moves = kwargs.get("moves", 100)

        self.__delay = kwargs.get("delay", 0.25)

        self.__init_gems()

        self.__board0 = self.__create_board()
        self.__board1 = self.__create_board()
        self.__boards = {
            "active": self.__board0,
            "standby": self.__board1
        }

        self.__init_board(self.__boards["active"])


    def __init_gems(self):
        # Black / Blank / Empty Gem
        self.EMPTY_GEM = Gem(" ", curses.color_pair(0))

        # Colored Gems
        color_idx = 1
        for name, data in self.GEM_DEFS.items():
            curses.init_pair(color_idx, data[1], curses.COLOR_BLACK)
            color = curses.color_pair(color_idx) | curses.A_BOLD
            self.GEMS[name] = Gem(data[0], color)
            color_idx += 1


    def __create_board(self):
        board = [[]] * self.__height
        for row in range(self.__height):
            board[row] = [self.EMPTY_GEM] * self.__width

        return board


    def __init_board(self, board):
        gems = list(self.GEMS.values())

        for row in range(self.__height):
            for col in range(self.__width):
                board[row][col] = random.choice(gems)


    # def __debug(self, msg, pause=False):
    #     self.__screen.addstr(0, 0, msg, curses.color_pair(self.COLOR_DEBUG))
    #     self.__screen.refresh()
    #     if pause:
    #         self.__screen.getch()


    def __display(self):
        """ Display ACTIVE board w/ Curses """
        board = self.__boards["active"]
        for row in range(self.__height):
            for col in range(self.__width):
                gem = board[row][col]
                # TODO: use self.__spacing
                self.__screen.addch(row, col, gem.icon, gem.color)

        # Display Status Line
        self.__screen.addstr(
            self.__height, 0,
            f"|[{self.__width}]x[{self.__height}]|Move: {self.__move_count}/{self.__max_moves}|Score: ??",
            curses.color_pair(0) | curses.A_REVERSE
        )
        self.__screen.refresh()


    def __update_boards(self):
        if self.__move_count % 2 == 0:
            self.__boards["active"] = self.__board0
            self.__boards["standby"] = self.__board1
        else:
            self.__boards["active"] = self.__board1
            self.__boards["standby"] = self.__board0


    def __compute_next_move(self):
        self.__move_count += 1
        self.__update_boards()

    # def compute_generation(self):
    #     """ Compute the Next Generation """
    #     old_board = self.__boards["active"]
    #     new_board = self.__boards["standby"]
    #     width = self.__width
    #     height = self.__height
    #     for y in range(height):
    #         for x in range(width):
    #             count = self.__count_live_neighbors(old_board, (x,y))
    #             self.__set_cell(new_board, (x,y), old_board[y][x], count)

    #     self.__generation += 1
    #     self.__update_boards()


    def play(self):
        """ Play the game """
        for _ in range(self.__max_moves):
            self.__display()
            time.sleep(self.__delay)
            self.__compute_next_move()








# -----------------------------------------------------------------------------
