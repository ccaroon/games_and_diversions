from .location import Location

class Match:

    DIRECTION_VERTICAL = "VERTICAL"
    DIRECTION_HORIZONTAL = "HORIZONTAL"

    def __init__(self, loc1:Location, loc2:Location):
        """
        A Gem Match from loc1 to loc2.

        Direction of match and number of gems forming the match are calculated.
        """
        self.__loc1 = loc1
        self.__loc2 = loc2

        self.__direction = None
        # Same ROW -> Left to Right
        if self.__loc1.row == self.__loc2.row:
            self.__direction = self.DIRECTION_HORIZONTAL
        # Same COL -> Up & Down
        elif self.__loc1.col == self.__loc2.col:
            self.__direction = self.DIRECTION_VERTICAL
        else:
            raise ValueError(f"Unable to calcuate direction: {self.__loc1} to {self.__loc2}")

        self.__count = None
        if self.__direction == self.DIRECTION_HORIZONTAL:
            self.__count = (self.__loc2.col - self.__loc1.col) + 1
        elif self.__direction == self.DIRECTION_VERTICAL:
            self.__count = (self.__loc2.row - self.__loc1.row) + 1


    def __str__(self):
        return f"Match({self.__loc1}, {self.__loc2}, {self.__count}, {self.__direction})"


    def locations(self) -> list:
        """
        Find all the locations(row, col) starting at `loc1` and moving in
        `direction` for `count` places.
        """
        start = self.__loc1
        locations = [start]

        if self.__direction == self.DIRECTION_HORIZONTAL:
            for cnt in range(1, self.__count):
                row = start.row
                col = start.col + cnt
                locations.append(Location(row, col))
        elif self.__direction == self.DIRECTION_VERTICAL:
            for cnt in range(1, self.__count):
                row = start.row + cnt
                col = start.col
                locations.append(Location(row, col))


        return locations
