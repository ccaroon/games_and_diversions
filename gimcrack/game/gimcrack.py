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
    def __debug(self, msg, pause=False):
        self.__screen.addstr(0, 0, str(msg), curses.color_pair(self.COLOR_DEBUG))
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
                # self.__debug(f"Checking [{row},{col}]", True)
                match = self.__check_match(row, col)
                if match:
                    break

        # self.__debug(str(match), True)

        return match


    def __check_match(self, row, col):
        """
        For Gem @ (row,col) ...

        * Is it part of an existing match of 3 or more
        * Can it be swapped (up,down,left,right) to make a match of 3 or more

        Returns:
            Match instance
        """
        board = self.__board
        gem = board.get(row,col)
        gem_loc = Location(row, col)

        planes = (board.vertical_plane, board.horizontal_plane)

        match = None
        # EXISTING MATCH -- No Swap Needed
        for plane in planes:
            start_loc = gem_loc
            end_loc = gem_loc
            # --- Part One ---
            # Check to see if there are at least 3 consequetive, identical gems
            # ...in this plane
            # ...start at `gem_loc` moving in the `dir1` direction
            curr_loc = gem_loc + plane["dir1"]
            while curr_loc[plane["coord"]] >= 0 and board.get(curr_loc.row, curr_loc.col) == gem:
                start_loc = curr_loc
                curr_loc += plane["dir1"]

            # --- Part Two ---
            # IF found at least 3 consequetive, identical gems in this plane
            # ...gem at `gem_loc` + at least 2 others
            # Check to see if the match can be extended in the `dir2` direction.
            if start_loc.distance(gem_loc)[plane["coord"]] >= 2:
                curr_loc = gem_loc + plane["dir2"]
                while curr_loc[plane["coord"]] < plane["max"] and board.get(curr_loc.row, curr_loc.col) == gem:
                    end_loc = curr_loc
                    curr_loc += plane["dir2"]

                match = Match(start_loc, end_loc)

            if match:
                break

        # TODO: SWAP to MATCH


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


    def __animate_refill(self,match):
        # -> cascade gems down to fill clears spots
        # NOTE: Only temporary.
        # Real code will allow Gems to fall down, then repopulate
        # at the top
        # ---- TEMPORARY ---
        locs = match.locations()
        for loc in locs:
            self.__board.set(loc.row, loc.col, random.choice(list(self.GEMS.values())))
        # --- TEMPORARY ---

        self.__display()
        time.sleep(self.__delay)


    def __auto_match(self):
        match = self.__find_match()
        while match:
            # self.__debug(f"Match Found: ({match})", True)
            # if match.is_swap():
            #     # Gems must be swapped to match
            #     self.__animate_swap(match)
            #     self.__animate_show(match)
            #     self.__animate_clear(match)
            # elif match.is_exact():
            # Gems already match in current positions
            self.__animate_show(match)
            self.__animate_clear(match)
            # else:
            #     raise ValueError("Unknown match type")

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
