from .location import Location

class Match:

    VERTICAL = "VERTICAL"
    HORIZONTAL = "HORIZONTAL"

    def __init__(self, start:Location, end:Location):
        """
        A Gem Match from start to end.

        Direction of match and number of gems forming the match are calculated.
        """
        self.__start = start
        self.__end = end

        self.__direction = None
        # Same ROW -> Left to Right
        if self.__start.row == self.__end.row:
            self.__direction = self.HORIZONTAL
        # Same COL -> Up & Down
        elif self.__start.col == self.__end.col:
            self.__direction = self.VERTICAL
        else:
            raise ValueError(f"Unable to calcuate direction: {self.__start} to {self.__end}")

        self.__count = None
        if self.__direction == self.HORIZONTAL:
            self.__count = (self.__end.col - self.__start.col) + 1
        elif self.__direction == self.VERTICAL:
            self.__count = (self.__end.row - self.__start.row) + 1


    @property
    def start(self):
        return self.__start


    @property
    def end(self):
        return self.__end


    @property
    def direction(self):
        return self.__direction


    @property
    def count(self):
        return self.__count


    def __str__(self):
        return f"Match({self.__start}, {self.__end}, {self.__count}, {self.__direction})"


    def locations(self) -> list:
        """
        Find all the locations(row, col) starting at `start` and moving in
        `direction` for `count` places.
        """
        start = self.__start
        locations = [start]

        if self.__direction == self.HORIZONTAL:
            for cnt in range(1, self.__count):
                row = start.row
                col = start.col + cnt
                locations.append(Location(row, col))
        elif self.__direction == self.VERTICAL:
            for cnt in range(1, self.__count):
                row = start.row + cnt
                col = start.col
                locations.append(Location(row, col))


        return locations
