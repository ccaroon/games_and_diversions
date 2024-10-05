import random

from .gem import Gem

class Board:
    """ Playing Board """

    # Horizontal
    LEFT  = (0, -1)
    RIGHT = (0, +1)

    # Vertical
    UP   = (-1, 0)
    DOWN = (+1, 0)

    def __init__(self, screen, rows, cols, fill:Gem):
        self.__rows = rows
        self.__cols = cols
        self.__screen = screen
        self.__fill_gem = fill

        self.__board = [[]] * self.__rows
        for row in range(self.__rows):
            self.__board[row] = [fill] * self.__cols

        self.__axis = {
            "vertical": {
                "coord": 0,
                "max": self.__rows,
                "dir1": self.UP, "dir2": self.DOWN
            },
            "horizontal": {
                "coord": 1,
                "max": self.__cols,
                "dir1": self.LEFT, "dir2": self.RIGHT
            }
        }


    @property
    def rows(self):
        return self.__rows


    @property
    def cols(self):
        return self.__cols


    @property
    def vertical_axis(self):
        return self.__axis.get("vertical")


    @property
    def horizontal_axis(self):
        return self.__axis.get("horizontal")


    def set(self, row, col, gem:Gem):
        self.__board[row][col] = gem


    def get(self, row, col):
        return self.__board[row][col]


    def swap(self, loc1, loc2):
        """ Swap the Location of Two Gems """
        gem1 = self.get(loc1.row, loc1.col)
        gem2 = self.get(loc2.row, loc2.col)

        self.set(loc1.row, loc1.col, gem2)
        self.set(loc2.row, loc2.col, gem1)


    def swap_to(self, loc, direction:tuple):
        """ Swap a Gem with the Gem on the Left """
        self.swap(loc, loc + direction)


    def valid_location(self, loc):
        return (
            loc.row > -1 and loc.col > -1
            and
            loc.row < self.rows and loc.col < self.cols
        )

    # TODO: implement `direction`
    # def walk(self, callback, direction="TB-LR"):
    #     # bottom to top, left to right
    #     for row in range(self.__rows - 1, -1, -1):
    #         for col in range(self.__cols):
    #             callback(row, col)


    def populate(self, values):
        """ Populate the Board with Random Choices from a set of Values"""
        for row in range(self.__rows):
            for col in range(self.__cols):
                self.__board[row][col] = random.choice(values)


    def shift_down(self, start, end):
        """ Shift a Column Down """
        cursor = end
        while cursor != start:
            above = cursor + (-1, 0)
            gem = self.get(above.row, above.col)
            self.set(cursor.row, cursor.col, gem)
            cursor += (-1, 0)

        # fill spaces at top with EMPY
        self.set(start.row, start.col, self.__fill_gem)


    def refresh(self):
        for row in range(self.__rows):
            scr_col = 0
            for col in range(self.__cols):
                gem = self.__board[row][col]
                self.__screen.addch(row, scr_col, gem.icon, gem.color)
                # Inc by 2 to leave a space between each Gem in the column
                scr_col += 2
