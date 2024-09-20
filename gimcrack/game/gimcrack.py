import curses
import time

from .board import Board
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

        self.__width = width
        max_width = curses.COLS
        if self.__width == -1:
            self.__width = curses.COLS

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

        self.__board = Board(
            self.__screen, self.__height, self.__width, self.EMPTY_GEM)
        self.__board.populate(list(self.GEMS.values()))


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


    # TODO: move to bottom
    def __debug(self, msg, pause=False):
        self.__screen.addstr(0, 0, msg, curses.color_pair(self.COLOR_DEBUG))
        self.__screen.refresh()
        if pause:
            self.__screen.getch()


    def __display(self):
        """ Display ACTIVE board w/ Curses """
        self.__board.refresh()

        # Display Status Line
        # TODO: move to top
        self.__screen.addstr(
            self.__height, 0,
            f"|[{self.__height}]x[{self.__width}]|Move: {self.__move_count}/{self.__max_moves}|Score: {self.__score}",
            curses.color_pair(0) | curses.A_REVERSE
        )
        self.__screen.refresh()


    def __find_match(self):
        """ Search the board for a match """
        match = None
        # bottom to top, left to right
        # TODO: use board.walk()
        for row in range(self.__height - 1, -1, -1):
            if match:
                break

            for col in range(self.__width):
                self.__debug(f"Checking [{row},{col}]", True)
                match = self.__check_match(row, col)
                if match:
                    break

        self.__debug(str(match), True)

        return match


    def __check_match(self, row, col):
        """
        For Gem @ (row,col) ...

        * Is it part of an existing match of 3 or more
        * Can it be swapped (up,down,left,right) to make a match of 3 or more

        Returns:
            Match instance
        """
        # ==> YOU ARE HERE <==
        found = None
        board = self.__board
        gem = board.get(row,col)

        # check left
        # TODO: not working something funky is going on
        is_match = True
        direction = -1
        for count in range(2,3):
            col_idx = col + (count * direction)
            if col_idx < 0 or board.get(row,col_idx) != gem:
                is_match = False
                break

        if is_match:
            found = Match((row,col), (row,col + direction), 3)

        # check up
        # check right
        # check down


        return found


    def __animate_swap(self, match):
        # -> swap gems to create match
        board = self.__board
        r1 = match.gem1[0]
        c1 = match.gem1[1]

        r2 = match.gem2[0]
        c2 = match.gem2[1]

        board.set(r1, c1, Gem("A", curses.color_pair(1)))
        board.set(r2, c2, Gem("B", curses.color_pair(1)))

        self.__display()
        self.__debug(f"A[{r1},{c1}] | B[{r2},{c2}]", True)
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

        # def blah(row, col):
        #     self.__board.set(row, col, self.EMPTY_GEM)
        #     self.__display()
        #     time.sleep(self.__delay)

        # self.__board.walk(blah)

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
