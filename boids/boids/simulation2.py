#
# Ported / Adapted from https://github.com/beneater/boids
#
import curses
# import functools
import math
import random
import time

class Boid:
    MAX_HISTORY = 10

    def __init__(self, x, y, dx=None, dy=None):
        self.x = x
        self.y = y
        self.dx = dx or random.random() * 10 - 5
        self.dy = dy or random.random() * 10 - 5
        self.perching = False
        # Set to a random # of iterations when the boid perches
        self.perch_time = None
        # NOTE: Currently unused
        self.__history = []

    def __repr__(self):
        return f"Boid({self.x},{self.y},{self.dx},{self.dy})"

    def __str__(self):
        return self.__repr__()

    def update_history(self):
        self.__history.append([self.x, self.y])
        # Only keep MAX_HISTORY records
        self.__history = self.__history[-self.MAX_HISTORY:]


class BoidSimulation2:
    VISUAL_RANGE = 75
    MARGIN = 3

    MARKERS = {
        "small-dot": "·",
        "large-dot": "●",
        "circle-dot": "⊙"
    }
    DEFAULT_MARKER = MARKERS["small-dot"]

    COLOR_BOID = 1
    COLOR_BLACK_GREEN = 2
    COLOR_DEBUG = 3

    def __init__(self, stdscr, count, **kwargs):
        curses.init_pair(self.COLOR_BOID,
                         curses.COLOR_GREEN, curses.COLOR_BLACK)
        curses.init_pair(self.COLOR_BLACK_GREEN,
                         curses.COLOR_BLACK, curses.COLOR_GREEN)
        curses.init_pair(self.COLOR_DEBUG,
                         curses.COLOR_RED, curses.COLOR_BLACK)

        self.__count = count
        self.__marker = kwargs.get("marker", self.DEFAULT_MARKER)
        if len(self.__marker) > 1:
            self.__marker = self.MARKERS.get(self.__marker, self.DEFAULT_MARKER)

        self.__iteration_count = kwargs.get("iterations", 100)
        self.__delay = kwargs.get("delay", 0.075)
        self.__perch_chance = kwargs.get("perch_chance", 25) / 100.0
        self.__debug = kwargs.get("debug", False)

        self.__screen = stdscr
        self.__screen.nodelay(True)

        self.__width = curses.COLS - 1
        # -1 extra for info line at bottom
        self.__height = curses.LINES - 2
        self.__ground_level = self.__height - self.MARGIN

        self.__boids = []
        init_pattern = random.choice(("random", "center"))
        self.__init_boids(pattern=init_pattern)

        self.__iteration = 1


    def __init_boids(self, pattern="random"):
        for _ in range(self.__count):
            if pattern == "random":
                x = random.random() * self.__width
                y = random.random() * self.__height
            elif pattern == "center":
                x = (self.__width / 2.0) + 5 * random.random()
                y = (self.__height / 2.0) + 5 * random.random()

            self.__boids.append(
                Boid(x, y)
            )


    def __distance(self, boid1, boid2):
        return math.sqrt(
            (boid1.x - boid2.x) * (boid1.x - boid2.x) +
            (boid1.y - boid2.y) * (boid1.y - boid2.y)
        )


    # def __n_closest_boids(self, boid, n):
    #     cmp_func = lambda a,b: self.__distance(boid, a) - self.__distance(boid, b)
    #     key_func = functools.cmp_to_key(cmp_func)
    #
    #     # Sort the copy by distance from `boid`
    #     sorted_boids = sorted(self.__boids, key=key_func)
    #
    #     # Return the `n` closest
    #     return sorted_boids[1:n + 1]


    # Constrain a boid to within the window. If it gets too close to an edge,
    # nudge it back in and reverse its direction.
    def __keep_within_bounds(self, boid):
        turn_factor = 1

        if boid.x < self.MARGIN:
            boid.dx += turn_factor

        if boid.x > self.__width - self.MARGIN:
            boid.dx -= turn_factor

        if boid.y < self.MARGIN:
            boid.dy += turn_factor

        if boid.y > self.__height - self.MARGIN:
            boid.dy -= turn_factor

        if boid.y >= self.__ground_level and random.random() < self.__perch_chance:
            boid.perching = True
            # number of iterations to perch
            boid.perch_time = random.randint(5, 25)


    # Find the center of mass of the other boids and adjust velocity slightly to
    # point towards the center of mass.
    def __fly_towards_center(self, boid):
      # adjust velocity by this %
      centering_factor = 0.005

      center_x = 0
      center_y = 0
      num_neighbors = 0

      for other_boid in self.__boids:
        if self.__distance(boid, other_boid) < self.VISUAL_RANGE:
          center_x += other_boid.x
          center_y += other_boid.y
          num_neighbors += 1

      if num_neighbors:
        center_x = center_x / num_neighbors
        center_y = center_y / num_neighbors

        boid.dx += (center_x - boid.x) * centering_factor
        boid.dy += (center_y - boid.y) * centering_factor


    # Move away from other boids that are too close to avoid colliding
    def __avoid_others(self, boid):
      # The distance to stay away from other boids
      min_distance = 2;

      # Adjust velocity by this %
      avoid_factor = 0.05;

      move_x = 0
      move_y = 0

      for other_boid in self.__boids:
        if other_boid is not boid:
          if self.__distance(boid, other_boid) < min_distance:
            move_x += boid.x - other_boid.x
            move_y += boid.y - other_boid.y

      boid.dx += move_x * avoid_factor
      boid.dy += move_y * avoid_factor


    # // Find the average velocity (speed and direction) of the other boids and
    # // adjust velocity slightly to match.
    def __match_velocity(self, boid):
      # Adjust by this % of average velocity
      matching_factor = 0.05

      avg_dx = 0
      avg_dy = 0
      num_neighbors = 0

      for other_boid in self.__boids:
        if self.__distance(boid, other_boid) < self.VISUAL_RANGE:
          avg_dx += other_boid.dx
          avg_dy += other_boid.dy
          num_neighbors += 1

      if num_neighbors:
        avg_dx = avg_dx / num_neighbors
        avg_dy = avg_dy / num_neighbors

        boid.dx += (avg_dx - boid.dx) * matching_factor
        boid.dy += (avg_dy - boid.dy) * matching_factor


    # Speed will naturally vary in flocking behavior, but real animals can't go
    # arbitrarily fast.
    def __limit_speed(self, boid):
      speed_limit = 15

      speed = math.sqrt(boid.dx * boid.dx + boid.dy * boid.dy)
      if speed > speed_limit:
        boid.dx = (boid.dx / speed) * speed_limit
        boid.dy = (boid.dy / speed) * speed_limit


    def add(self, loc:tuple=None):
        # Add a new Boid
        row = loc[0] if loc is not None else self.__height // 2
        col = loc[1] if loc is not None else self.__width // 2

        self.__boids.append(Boid(col, row))
        self.__count += 1


    def __dump(self):
        dump_str = ""
        for boid in self.__boids:
            if boid.x < 0 or boid.x > self.__width or boid.y < 0 or boid.y > self.__height:
                dump_str += f"{boid}\n"
        return dump_str


    def tick(self):
        for boid in self.__boids:
            if boid.perching:
                if boid.perch_time > 0:
                    boid.perch_time -= 1
                else:
                    boid.perching = False
            else:
                # Update the velocities according to each rule
                self.__fly_towards_center(boid)
                self.__avoid_others(boid)
                self.__match_velocity(boid)
                self.__limit_speed(boid)
                self.__keep_within_bounds(boid)

                # Update the position based on the current velocity
                boid.x += boid.dx
                # Keep in col/width bounds
                boid.x = self.MARGIN if boid.x < 0 else boid.x
                boid.x = self.__width - self.MARGIN if boid.x > self.__width else boid.x

                boid.y += boid.dy
                # keep in row/height bounds
                boid.y = self.MARGIN if boid.y < 0 else boid.y
                boid.y = self.__height - self.MARGIN if boid.y > self.__height else boid.y
                # boid.update_history()

        self.__iteration += 1

    def display(self):
        self.__screen.erase()

        line = 0
        for idx, boid in enumerate(self.__boids):
            angle = math.atan2(boid.dy, boid.dx)
            col = int(boid.x)
            row = int(boid.y)
            marker = idx if self.__debug else self.__marker

            if self.__debug:
                self.__screen.addstr(line, 0, f"{idx}) ({row},{col}) -> [{angle}]/[{boid.dx},{boid.dy}]", curses.color_pair(self.COLOR_BOID))
                line += 1

            self.__screen.addstr(row, col, f"{marker}", curses.color_pair(self.COLOR_BOID))

        self.__screen.addstr(
            self.__height+1, 0,
            f"Boids| {self.__width}x{self.__height} | {self.__count} {self.__perch_chance*100}% | {self.__iteration}/{self.__iteration_count} | ",
            curses.color_pair(self.COLOR_BLACK_GREEN)
        )

        self.__screen.refresh()

    def run(self):
        curses.mousemask(curses.ALL_MOUSE_EVENTS)
        for _ in range(self.__iteration_count):

            try:
                self.display()
            except curses.error as err:
                xyzzy = self.__dump()
                raise RuntimeError(xyzzy)

            self.tick()

            input = self.__screen.getch()
            if input == ord("q"):
                break
            elif input == ord("b"):
                self.add()
            elif input == curses.KEY_MOUSE:
                id,x,y,_,button = curses.getmouse()
                if button & curses.BUTTON1_CLICKED:
                    self.add((y,x))
                # if button & curses.BUTTON2_CLICKED:
                #     self.scatter((y,x))

            time.sleep(self.__delay)
