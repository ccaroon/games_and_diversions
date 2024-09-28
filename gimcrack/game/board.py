import random

from .gem import Gem
from .location import Location

class Board:
    """ Playing Board """

    def __init__(self, screen, rows, cols, fill:Gem):
        self.__rows = rows
        self.__cols = cols
        self.__screen = screen

        self.__board = [[]] * self.__rows
        for row in range(self.__rows):
            self.__board[row] = [fill] * self.__cols


    @property
    def rows(self):
        return self.__rows


    @property
    def cols(self):
        return self.__cols


    def set(self, row, col, gem:Gem):
        self.__board[row][col] = gem


    def get(self, row, col):
        return self.__board[row][col]


    # TODO: implement `direction`
    def walk(self, callback, direction="TB-LR"):
        # bottom to top, left to right
        for row in range(self.__rows - 1, -1, -1):
            for col in range(self.__cols):
                callback(row, col)


    def populate(self, values):
        """ Populate the Board with Random Choices from a set of Values"""
        for row in range(self.__rows):
            for col in range(self.__cols):
                self.__board[row][col] = random.choice(values)


    def refresh(self):
        for row in range(self.__rows):
            scr_col = 0
            for col in range(self.__cols):
                gem = self.__board[row][col]
                self.__screen.addch(row, scr_col, gem.icon, gem.color)
                # Inc by 2 to leave a space between each Gem in the column
                scr_col += 2
