import ast
import copy
import curses
import re
import time
import random

class GameOfLife:
    """ Conway's Game of Life Simulator """

    COLOR_CELL = 1
    COLOR_BLACK_GREEN = 2
    COLOR_DEBUG = 3

    NEIGHBOR_OFFSETS = (
        (-1,-1),(+0,-1),(+1,-1),
        (-1,+0),        (+1,+0),
        (-1,+1),(+0,+1),(+1,+1)
    )

    def __init__(self, stdscr, width, height, **kwargs):
        curses.init_pair(self.COLOR_CELL,
            curses.COLOR_GREEN, curses.COLOR_BLACK)
        curses.init_pair(self.COLOR_BLACK_GREEN,
            curses.COLOR_BLACK, curses.COLOR_GREEN)
        curses.init_pair(self.COLOR_DEBUG,
            curses.COLOR_RED, curses.COLOR_BLACK)

        self.__screen = stdscr

        self.__width = width
        if self.__width == -1:
            self.__width = curses.COLS // 2

        self.__height = height
        if self.__height == -1:
            # -1 for info line
            self.__height = curses.LINES-1

        # self.__debug(f"{self.__width}x{self.__height} | {curses.COLS}x{curses.LINES}", True)

        # COLS // 2 b/c a ' ' is printed between chars
        if self.__height > curses.LINES or self.__width > curses.COLS // 2:
            raise ValueError(f"Screen too small: Max Width: {curses.COLS // 2} | Max Height: {curses.LINES-1}")

        self.__alive = kwargs.get("alive", "●")
        self.__dead = kwargs.get("dead", " ")

        self.__generation = 1
        self.__max_gens = kwargs.get("max_gens", 100)

        self.__delay = kwargs.get("delay", 0.25)

        self.__wrap_edges = kwargs.get("wrap_edges", False)

        self.__board0 = self.__create_board()
        self.__board1 = self.__create_board()
        self.__boards = {
            "active": self.__board0,
            "standby": self.__board1
        }

        self.__pattern_name = None
        pattern = kwargs.get("pattern")
        if pattern:
            self.__pattern_name = pattern
            self.__seed_from_pattern(pattern, center=True)
        else:
            self.__pattern_name = "Random"
            seed_percent = kwargs.get("seed_percent", 50)
            self.__seed_randomly(self.__boards["active"], percent=seed_percent)

    # NOTE:
    # x,y indexes will need to be reversed when indexing boards created
    # this way.
    # I.e. y == row, x == col
    # Have to index the ROW first, then the COL -> board[y][x]
    def __create_board(self):
        row = [self.__dead] * self.__width
        board = []
        for _ in range(self.__height):
            board.append(copy.deepcopy(row))
        return board

    def __debug(self, msg, pause=False):
        self.__screen.addstr(0, 0, msg, curses.color_pair(self.COLOR_DEBUG))
        self.__screen.refresh()
        if pause:
            self.__screen.getch()

    def __display2(self):
        """ Display ACTIVE board w/ Curses """
        board = self.__boards["active"]
        # Display the board
        for y in range(self.__height):
            line = " ".join(board[y])
            self.__screen.addstr(y, 0, line, curses.color_pair(self.COLOR_CELL))

        # Display generation count
        self.__screen.addstr(
            self.__height, 0,
            f"|[{self.__width}]x[{self.__height}]|{self.__pattern_name}|Wrap: {self.__wrap_edges}|Gen: {self.__generation}/{self.__max_gens}|",
            curses.color_pair(self.COLOR_BLACK_GREEN)
        )
        self.__screen.refresh()

    def __display(self):
        """ Display the ACTIVE board """
        board = self.__boards["active"]

        # Clear the screen
        print("\033c\033[3J", end='')

        # Display the board
        for y in range(self.__height):
            line = "  ".join(board[y])
            print(line)
        print()

        # Display generation count
        print(f"Generation: {self.__generation}")

    def __seed_from_pattern(self, pattern, **kwargs):
        # Figure out the path to the pattern file
        pattern_path = pattern
        if not pattern_path.startswith(("/", "./")):
            pattern_path = f"./patterns/{pattern}"

        # Read the pattern from the file & glean some metdata
        pat_width = 0
        pat_height = 0
        bitmap = []
        with open(pattern_path, "r", encoding="utf-8") as fptr:
            line = fptr.readline()
            while line:
                line = re.sub("\s+", "", line)
                if line.startswith("#"):
                    # Example: gol-hint:center=False;offset=(1,2)
                    if "gol-hint" in line:
                        (_, hint_str) = line.split(":", 2)
                        hints = hint_str.split(";")
                        for hint in hints:
                            # self.__debug(hint, True)
                            (option, value) = hint.split("=", 2)
                            kwargs[option] = ast.literal_eval(value)
                else:
                    pat_width = len(line)
                    pat_height += 1
                    bitmap.extend(list(line))

                line = fptr.readline()

        if pat_width > self.__width or pat_height > self.__height:
            raise ValueError(f"Board size to small for pattern. Min Size: ({pat_width}x{pat_height})")

        center = kwargs.get("center", False)
        offset = kwargs.get("offset", (0,0))
        # Compute offset to center pattern on board
        if center:
            # // 4 b/c cells are printed with a ' ' between them
            off_x = (self.__width // 4) - (pat_width // 4)
            off_y = (self.__height // 2) - (pat_height // 2)
        else:
            off_x = offset[0]
            off_y = offset[1]

        # Populate the board
        board = self.__boards["active"]
        for (idx, state) in enumerate(bitmap):
            x = idx % pat_width
            y = idx // pat_width
            board[y+off_y][x+off_x] = self.__alive if int(state) else self.__dead

    def __seed_randomly(self, board, percent=50):
        width = self.__width
        height = self.__height
        count = int(width * height * (percent/100))

        for _ in range(count):
            x = random.randint(0, width-1)
            y = random.randint(0, height-1)
            board[y][x] = self.__alive

    def __count_live_neighbors(self, board, cell:tuple):
        x = cell[0]
        y = cell[1]
        width = self.__width
        height = self.__height
        count = 0

        for offset in self.NEIGHBOR_OFFSETS:
            nx = x + offset[0]
            ny = y + offset[1]

            if self.__wrap_edges:
                nx = width-1 if nx < 0 else nx
                nx = 0 if nx >= width else nx

                ny = height-1 if ny < 0 else ny
                ny = 0 if ny >= height else ny

            if (nx >= 0 and nx < width) and (ny >= 0 and ny < height):
                count += 1 if board[ny][nx] == self.__alive else 0

            # self.__debug(f"({x},{y}) - ({nx},{ny})...({board[nx][ny]})")

        return count

    def __set_cell(self, board, cell:tuple, state, count):
        x = cell[0]
        y = cell[1]

        if state == self.__alive:
            # Any live cell with fewer than two live neighbours dies
            if count < 2:
                board[y][x] = self.__dead
                # print(f"{x},{y}: ALIVE --> DEAD")
            # Any live cell with two or three live neighbours lives
            elif count == 2 or count == 3:
                board[y][x] = self.__alive
                # print(f"{x},{y}: ALIVE --> ALIVE")
            # Any live cell with more than three live neighbours dies
            elif count > 3:
                board[y][x] = self.__dead
                # print(f"{x},{y}: ALIVE --> DEAD")
            # else:
            #     print(f"{x},{y} - [{count}] ALIVE --> ?????")
        elif state == self.__dead:
            # Any dead cell with exactly three live neighbours becomes a live cell
            if count == 3:
                board[y][x] = self.__alive
                # print(f"{x},{y}: DEAD --> ALIVE")
            else:
                board[y][x] = self.__dead
                # print(f"{x},{y} - [{count}] DEAD --> DEAD")
        # else:
        #     print(f"{x},{y}: ????? --> ?????")

    def __update_boards(self):
        if self.__generation % 2 == 0:
            self.__boards["active"] = self.__board0
            self.__boards["standby"] = self.__board1
        else:
            self.__boards["active"] = self.__board1
            self.__boards["standby"] = self.__board0

    def compute_generation(self):
        """ Compute the Next Generation """
        old_board = self.__boards["active"]
        new_board = self.__boards["standby"]
        width = self.__width
        height = self.__height
        for y in range(height):
            for x in range(width):
                count = self.__count_live_neighbors(old_board, (x,y))
                self.__set_cell(new_board, (x,y), old_board[y][x], count)

        self.__generation += 1
        self.__update_boards()

    def run(self):
        """ Run the Simulation """
        for _ in range(self.__max_gens):
            # self.__display()
            self.__display2()
            time.sleep(self.__delay)
            self.compute_generation()








# -----------------------------------------------------------------------------
