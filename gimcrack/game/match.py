class Match:

    def __init__(self, count, gem1:tuple, gem2:tuple=None):
        """
        A match of `count` gems starting at `gem1` if swapped with `gem2`.

        If `gem2` is None, the no swap is necessary to make the match.

        `gem1` & `gem2` are tuple(row,col)
        """
        self.count = count
        self.gem1 = gem1
        self.gem2 = gem2
