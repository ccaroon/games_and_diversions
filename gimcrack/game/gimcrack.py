import copy
import curses
# import re
import time
import random

from .gem import Gem
from .match import Match

class GimCrack:
    """ A Simple, Self-Playing Gem Matching Game """

    COLOR_DEBUG = 99

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
        curses.mousemask(curses.ALL_MOUSE_EVENTS)

        curses.init_pair(self.COLOR_DEBUG, curses.COLOR_BLACK, curses.COLOR_RED)

        self.__screen = stdscr

        # Num spaces b/w gems on each row, i.e. horizontal spacing
        self.__spacing = 1

        self.__width = width
        max_width = curses.COLS
        if self.__width == -1:
            self.__width = curses.COLS

        if self.__spacing:
            self.__width //= self.__spacing
            max_width //= self.__spacing

        self.__height = height
        max_height = curses.LINES - 1
        if self.__height == -1:
            # -1 for info line
            self.__height = curses.LINES - 1

        # COLS // 2 b/c a ' ' is printed between chars
        if self.__height > max_height or self.__width > max_width:
            raise ValueError(f"Screen too small: Max Width: {max_width} | Max Height: {max_height}")

        self.__score = 0
        self.__move_count = 1
        self.__max_moves = kwargs.get("moves", 100)

        self.__delay = kwargs.get("delay", 0.25)

        self.__init_gems()

        self.__board0 = self.__create_board()
        # self.__board1 = self.__create_board()
        self.__boards = {
            "active": self.__board0,
            # "standby": self.__board1
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


    def __debug(self, msg, pause=False):
        self.__screen.addstr(0, 0, msg, curses.color_pair(self.COLOR_DEBUG))
        self.__screen.refresh()
        if pause:
            self.__screen.getch()


    def __display(self):
        """ Display ACTIVE board w/ Curses """
        board = self.__boards["active"]
        for row in range(self.__height):
            for col in range(0, self.__width, self.__spacing + 1):
                gem = board[row][col]
                # Add Gem
                self.__screen.addch(row, col, gem.icon, gem.color)

                # Add Spacer Gems, if any
                for i in range(1, self.__spacing + 1):
                    col_idx = col + i
                    if col_idx < self.__width:
                        self.__screen.addch(row, col_idx,
                            self.EMPTY_GEM.icon, self.EMPTY_GEM.color
                    )

        # Display Status Line
        self.__screen.addstr(
            self.__height, 0,
            f"|[{self.__height}]x[{self.__width}]|Move: {self.__move_count}/{self.__max_moves}|Score: {self.__score}",
            curses.color_pair(0) | curses.A_REVERSE
        )
        self.__screen.refresh()


    # def __update_boards(self):
    #     if self.__move_count % 2 == 0:
    #         self.__boards["active"] = self.__board0
    #         self.__boards["standby"] = self.__board1
    #     else:
    #         self.__boards["active"] = self.__board1
    #         self.__boards["standby"] = self.__board0


    def __find_match(self):
        """ Search the board for a match """
        match = None
        # bottom to top, left to right
        for row in range(self.__height - 1, -1, -1):
            if match:
                break

            for col in range(self.__width):
                match = self.__check_match(row, col)
                if match:
                    break

        return match


    def __check_match(self, row, col):
        """
        For Gem @ (row,col) ...

        * Is it part of an existing match of 3 or more
        * Can it be swapped (up,down,left,right) to make a match of 3 or more

        Returns:
            Match instance
        """
        # ...YOU ARE HERE...
        return None


    def __animate_swap(self, match):
        # -> swap gems to create match
        self.__display()
        time.sleep(self.__delay)


    def __animate_clear(self, match):
        # -> clear matched gems
        self.__display()
        time.sleep(self.__delay)


    def __animate_refill(self):
        # -> cascade gems down to fill clears spots
        self.__display()
        time.sleep(self.__delay)


    def __auto_match(self):
        match = self.__find_match()
        while match:
            if match.gem2:
                # Gems must be swapped to match
                self.__animate_swap(match)
                self.__animate_clear(match)
            else:
                # Gems already match in current positions
                self.__animate_clear(match)

            self.__animate_refill()
            self.__move_count += 1

            match = self.__find_match()


    def __auto_input(self):
        self.__auto_match()


    def __player_input(self):
        input = self.__screen.getch()

        # if input == ord("q"):
        #     break
        if input == curses.KEY_MOUSE:
            _, x, y, _, button = curses.getmouse()
            if button & curses.BUTTON1_CLICKED:
                self.__debug(f"Row: {y} | Col: {x}", pause=True)
            # if button & curses.BUTTON2_CLICKED:
            #     self.scatter((y,x))

        self.__move_count += 1


    def play(self):
        """ Play the game """
        for _ in range(self.__max_moves):
            self.__display()

            self.__auto_input()
            # self.__player_input()








# -----------------------------------------------------------------------------
