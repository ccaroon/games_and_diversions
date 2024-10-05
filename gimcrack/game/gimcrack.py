import curses
import time
import random

from .board import Board
from .gem import Gem
from .location import Location
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

    def __init__(self, stdscr, rows, cols, **kwargs):
        # Hide the cursor / make it invisible
        curses.curs_set(0)
        curses.mousemask(curses.ALL_MOUSE_EVENTS)

        curses.init_pair(self.COLOR_DEBUG, curses.COLOR_BLACK, curses.COLOR_RED)

        self.__screen = stdscr

        board_rows = rows
        src_height = curses.LINES - 1
        if board_rows == -1:
            # -1 for info line
            board_rows = curses.LINES - 1

        board_cols = cols
        scr_width = curses.COLS
        if board_cols == -1:
            # Div 2 b/c there's a space between each displayed Gem
            board_cols = curses.COLS // 2

        if board_rows > src_height or board_cols > scr_width // 2:
            raise ValueError(f"Screen too small: Max Rows: {src_height} | Max Cols: {scr_width // 2}")

        self.__score = 0
        self.__move_count = 1
        self.__max_moves = kwargs.get("moves", 100)

        self.__delay = kwargs.get("delay", 0.25)

        self.__init_gems()

        self.__board = Board(
            self.__screen,
            board_rows, board_cols,
            self.EMPTY_GEM
        )
        self.__board.populate(list(self.GEMS.values()))


    def __init_gems(self):
        # Black / Blank / Empty Gem
        self.EMPTY_GEM = Gem(" ", curses.color_pair(0))
        self.MATCH_GEM = Gem("🟏", curses.color_pair(2) | curses.A_BOLD)
        # self.MATCH_GEM = Gem("܍", curses.color_pair(2) | curses.A_BOLD)
        # self.MATCH_GEM = Gem("🌟", curses.color_pair(0))

        # Colored Gems
        color_idx = 1
        for name, data in self.GEM_DEFS.items():
            curses.init_pair(color_idx, data[1], curses.COLOR_BLACK)
            color = curses.color_pair(color_idx) | curses.A_BOLD
            self.GEMS[name] = Gem(data[0], color)
            color_idx += 1


    # TODO: move to bottom
    def __debug(self, msg, row=0, col=0, pause=False):
        self.__screen.addstr(row, col, str(msg), curses.color_pair(self.COLOR_DEBUG))
        self.__screen.refresh()
        if pause:
            self.__screen.getch()


    def __display(self):
        """ Display ACTIVE board w/ Curses """
        self.__board.refresh()

        # Display Status Line
        # TODO: move to top of screen
        self.__screen.addstr(
            self.__board.rows, 0,
            f"|[{self.__board.rows}]x[{self.__board.cols}]|Move: {self.__move_count}/{self.__max_moves}|Score: {self.__score}",
            curses.color_pair(0) | curses.A_REVERSE
        )
        self.__screen.refresh()


    def __find_match(self):
        """ Search the board for a match """
        match = None
        # bottom to top, left to right
        # TODO: use board.walk()
        for row in range(self.__board.rows - 1, -1, -1):
            if match:
                break

            for col in range(self.__board.cols):
                gem_loc = Location(row, col)
                # self.__debug(f"Checking {gem_loc}", True)

                # Is there a match with NO swap?
                match = self.__check_match(row, col)

                if not match:
                    # Check for Swap Matches
                    for direction in (Board.LEFT, Board.UP, Board.RIGHT, Board.DOWN):
                        check_loc = gem_loc + direction
                        if self.__board.valid_location(check_loc):
                            self.__board.swap_to(gem_loc, direction)
                            match = self.__check_match(check_loc.row, check_loc.col)

                            if match:
                                break
                            else:
                                # Swap Gem Back to original postion
                                self.__board.swap(gem_loc, check_loc)

                if match:
                    break

        return match


    def __check_match(self, row, col):
        """
        Checks to see if there are 3 or more consecutive, identical gems starting
        at the given location (row,col).

        Returns:
            Match instance
        """
        board = self.__board
        gem = board.get(row,col)
        gem_loc = Location(row, col)

        axes = (board.vertical_axis, board.horizontal_axis)

        match = None
        for axis in axes:
            start_loc = gem_loc
            end_loc = gem_loc
            # --- Part One ---
            # Check to see if there are at least 3 consecutive, identical gems
            # ...in this axis
            # ...start at `gem_loc` moving in the `dir1` direction
            curr_loc = gem_loc + axis["dir1"]
            while curr_loc[axis["coord"]] >= 0 and board.get(curr_loc.row, curr_loc.col) == gem:
                start_loc = curr_loc
                curr_loc += axis["dir1"]

            # --- Part Two ---
            # IF found at least 3 consecutive, identical gems in this axis
            # ...gem at `gem_loc` + at least 2 others
            # Check to see if the match can be extended in the `dir2` direction.
            if start_loc.distance(gem_loc)[axis["coord"]] >= 2:
                curr_loc = gem_loc + axis["dir2"]
                while curr_loc[axis["coord"]] < axis["max"] and board.get(curr_loc.row, curr_loc.col) == gem:
                    end_loc = curr_loc
                    curr_loc += axis["dir2"]

                match = Match(start_loc, end_loc)

            if match:
                break

        return match


    def __animate_swap(self, match):
        # -> swap gems to create match
        self.__display()
        time.sleep(self.__delay)


    def __animate_show(self, match):
        # -> show matched gem set
        locs = match.locations()
        for loc in locs:
            self.__board.set(loc.row, loc.col, self.MATCH_GEM)

        self.__display()
        time.sleep(self.__delay)


    def __animate_clear(self, match):
        # -> clear matched gems
        locs = match.locations()
        for loc in locs:
            self.__board.set(loc.row, loc.col, self.EMPTY_GEM)

        self.__display()
        time.sleep(self.__delay)


    def __animate_refill(self, match):
        # Cascade gems down to fill cleared spaces
        for loc in match.locations():
            start = Location(0, loc.col)
            end = loc
            self.__board.shift_down(start, end)

        # self.__display()
        # time.sleep(self.__delay)

        # refill cleared spaces
        gems = list(self.GEMS.values())
        for idx in range(match.count):
            if match.direction == Match.HORIZONTAL:
                row = 0
                col = match.start.col + idx
            elif match.direction == Match.VERTICAL:
                row = idx
                col = match.start.col

            self.__board.set(row, col, random.choice(gems))

        self.__display()
        time.sleep(self.__delay)


    def __auto_match(self):
        match = self.__find_match()
        while match:
            # TODO: remove
            # self.__debug(f"{match}", True)

            self.__animate_swap(match)
            self.__animate_show(match)
            self.__animate_clear(match)
            self.__animate_refill(match)

            match = self.__find_match()


    def __auto_play(self):
        # Give a chance to view the board before changing it.
        # TODO: Remove later???
        time.sleep(self.__delay)

        self.__auto_match()
        self.__move_count += 1


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

            self.__auto_play()
            # self.__player_input()








# -----------------------------------------------------------------------------
