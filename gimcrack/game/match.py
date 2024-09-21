class Match:

    DIRECTION_UP = 1
    DIRECTION_DN = 2
    DIRECTION_LEFT = 3
    DIRECTION_RIGHT = 4

    def __init__(self, pos1:tuple, pos2:tuple, count, direction):
        """
        A match of `count` gems starting at `pos1` and moving in `direction`

        If `pos2` is None, then no swap is necessary to make the match, else
        a match is made by swapping the Gem at `pos1` with the Gem at `pos2`.

        `pos1` & `pos2` are tuple(row,col)

        Workflow:
            1. Swap Gems at `pos1` and `pos2`
            2. Now forms a match of `count` Gems moving in the given `direction`
        """
        self.__pos1 = pos1
        self.__pos2 = pos2
        self.__count = count
        self.__direction = direction


    def __str__(self):
        return f"Match({self.__pos1}, {self.__pos2}, {self.__count}, {self.__direction})"


    def is_exact(self):
        """ Is Exact Match. No Swapping Needed """
        return self.__pos1 is not None and self.__pos2 is None


    def is_swap(self):
        """ Match only formed by swapping two Gems """
        return self.__pos1 is not None and self.__pos2 is not None


    def locations(self) -> list:
        """
        Find all the locations(row, col) starting at `pos1` and moving in
        `direction` for a `count` places.
        """
        start = self.__pos1
        locations = [start]

        # TODO: code other directions
        if self.__direction == self.DIRECTION_LEFT:
            for cnt in range(1, self.__count):
                row = start[0]
                col = start[1] - cnt
                locations.append((row, col))


        return locations
