class Location:
    def __init__(self, row, col):
        self.__row = row
        self.__col = col


    @property
    def row(self):
        return self.__row


    @property
    def col(self):
        return self.__col


    def __str__(self):
        return f"({self.__row},{self.__col})"


    def __add__(self, delta:tuple):
        return Location(
            self.__row + delta[0],
            self.__col + delta[1]
        )


    def __eq__(self, other):
        return self.row == other.row and self.col == other.col


    def hdistance(self, other):
        return self.distance(other)[1]


    def vdistance(self, other):
        return self.distance(other)[0]


    def distance(self, other) -> tuple:
        rows = other.row - self.row
        cols = other.col - self.col

        return (rows, cols)
