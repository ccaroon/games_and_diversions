# import curses
import random
# import time

from .gem import Gem

class Board:
    """ Playing Board """

    DISPLAY_SPACING = 1

    def __init__(self, screen, rows, cols, blank:Gem):
        self.__width = cols
        self.__height = rows
        self.__screen = screen
        self.__blank = blank

        self.__board = [[]] * self.__height
        for row in range(self.__height):
            self.__board[row] = [blank] * self.__width


    def set(self, row, col, gem:Gem):
        self.__board[row][col] = gem


    def get(self, row, col):
        return self.__board[row][col]


    # TODO: implement `direction`
    def walk(self, callback, direction="TB-LR"):
        # bottom to top, left to right
        for row in range(self.__height - 1, -1, -1):
            for col in range(self.__width):
                callback(row, col)


    def populate(self, values):
        for row in range(self.__height):
            for col in range(self.__width):
                self.__board[row][col] = random.choice(values)


    def refresh(self):
        for row in range(self.__height):
            for col in range(0, self.__width, self.DISPLAY_SPACING + 1):
                gem = self.__board[row][col]
                # Add Gem
                self.__screen.addch(row, col, gem.icon, gem.color)

                # Add Spacer Gems
                for i in range(1, self.DISPLAY_SPACING + 1):
                    col_idx = col + i
                    if col_idx < self.__width:
                        self.__screen.addch(row, col_idx,
                            self.__blank.icon, self.__blank.color
                    )
