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


    def __getitem__(self, idx):
        value = None
        if idx == 0:
            value = self.__row
        elif idx == 1:
            value = self.__col
        else:
            raise IndexError(f"Index Out of Range: {idx}")

        return value


    def hdistance(self, other):
        return other.col - self.col


    def vdistance(self, other):
        return other.row - self.row


    def distance(self, other) -> tuple:
        rows = self.vdistance(other)
        cols = self.hdistance(other)
        return (rows, cols)
