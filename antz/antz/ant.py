import random

class TrailMark:
    def __init__(self, ant):
        self.x = ant.x
        self.y = ant.y
        self.dx = ant.dx
        self.dy = ant.dy

    def __eq__(self, other):
        return (self.x, self.y) == (other.x, other.y)
        # return (self.x, self.y, self.dx, self.dy) == (other.x, other.y, other.dx, other.dy)
        # return self.x == other.x and self.y == other.y and self.dx == other.dx and self.dy == other.dy

# class CampSite:
#     def __init__(self, ant):
#         self.x = ant.x
#         self.y = ant.y
#         self.dx = ant.dx
#         self.dy = ant.dy

class Ant:
    MAX_TRAIL = 100
    MAX_CAMPS = MAX_TRAIL // 3

    def __init__(self, id, x, y):
        self.id = id
        self.x = x
        self.y = y

        # dx, dy: -1, 0, 1
        # moving back, staying or moving forward
        self.dx = 0
        self.dy = 0

        self.trail = []

        self.following = None

        self.is_camping = False
        self.__camp_days = 0
        self.camp_sites = []

    def __valid_direction(self, curr_dx, curr_dy):
        valid = True

        # No standing still
        if self.dx == 0 and self.dy == 0:
            valid = False

        # No backtracking
        if curr_dx == -self.dx and curr_dy == -self.dy:
            valid = False

        return valid

    def __set_direction(self):
        self.dx = random.choice((-1, 0, 1))
        self.dy = random.choice((-1, 0, 1))

    def choose_direction(self):
        curr_dx = self.dx
        curr_dy = self.dy

        self.__set_direction()
        while not self.__valid_direction(curr_dx, curr_dy):
            self.__set_direction()

    def on_trail_of(self, other_ant):
        on_trail = False
        ant_loc = TrailMark(self)
        if ant_loc in other_ant.trail:
            on_trail = True
        return on_trail

    def follow(self, other_ant):
        ant_loc = TrailMark(self)
        other_trail = other_ant.trail.copy()
        other_trail.reverse()
        mark_idx = other_trail.index(ant_loc)

        mark = other_ant.trail[mark_idx]
        self.dx = mark.dx
        self.dy = mark.dy

        self.following = other_ant

    def move(self):
        self.mark_trail()

        self.x += self.dx
        self.y += self.dy

    def set_up_camp(self):
        self.is_camping = True
        self.__camp_days = 0

        self.camp_sites.append((self.x, self.y))
        self.camp_sites = self.camp_sites[-self.MAX_CAMPS:]

    def pack_up_camp(self):
        self.is_camping = False
        self.__camp_days = 0

    def camp(self):
        self.__camp_days += 1
        if self.__camp_days == 3:
            self.pack_up_camp()

    def mark_trail(self):
        self.trail.append(TrailMark(self))
        self.trail = self.trail[-self.MAX_TRAIL:]
