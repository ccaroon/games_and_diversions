class Match:

    def __init__(self, gem1:tuple, gem2:tuple, count):
        """
        A match of `count` gems starting at `gem1` if swapped with `gem2`.

        If `gem2` is None, the no swap is necessary to make the match.

        `gem1` & `gem2` are tuple(row,col)
        """
        self.count = count
        self.gem1 = gem1
        self.gem2 = gem2


    def __str__(self):
        return f"Match({self.gem1}, {self.gem2}, {self.count})"
