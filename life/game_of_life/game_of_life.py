import ast
import copy
import curses
import re
import time
import random

class GameOfLife:
    """ Conway's Game of Life Simulator """

    MARKER_SETS = {
        "char": {
            "alive": "*",
            "dead": " ",
            "undead": "+"
        },
        "nomoji": {
            "alive": "●",
            "dead": " ",
            "undead": "❇"
        },
        # 💀 🤓 🙂 🤢
        "emoji": {
            "alive": "🙂",
            "dead": " ",
            "undead": "🤢"
        }
    }

    COLOR_CELL_LIVE = 1
    COLOR_CELL_DEAD = 2
    COLOR_CELL_UNDEAD = 3
    COLOR_STATUS = 4
    COLOR_DEBUG = 5

    NEIGHBOR_OFFSETS = (
        (-1,-1),(+0,-1),(+1,-1),
        (-1,+0),        (+1,+0),
        (-1,+1),(+0,+1),(+1,+1)
    )

    def __init__(self, stdscr, width, height, **kwargs):
        curses.init_pair(self.COLOR_CELL_LIVE,
            curses.COLOR_WHITE, curses.COLOR_BLACK)
        curses.init_pair(self.COLOR_CELL_DEAD,
            curses.COLOR_BLACK, curses.COLOR_BLACK)
        curses.init_pair(self.COLOR_CELL_UNDEAD,
            curses.COLOR_RED, curses.COLOR_BLACK)

        curses.init_pair(self.COLOR_STATUS,
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

        self.__zombies = kwargs.get("zombies", False)
        if self.__zombies < 0 or self.__zombies > 100:
            raise ValueError(f"Invalid Zombie Percentage")

        self.__alive = kwargs.get("alive", "●")
        self.__dead = kwargs.get("dead", " ")
        self.__undead = kwargs.get("undead", "*")

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
            # line = " ".join(board[y])
            # self.__screen.addstr(y, 0, line, curses.color_pair(self.COLOR_CELL_LIVE))
            scr_x = 0
            for x in range(self.__width):
                color = curses.color_pair(self.COLOR_CELL_DEAD)
                if board[y][x] == self.__alive:
                    color = curses.color_pair(self.COLOR_CELL_LIVE)
                elif board[y][x] == self.__undead:
                    color = curses.color_pair(self.COLOR_CELL_UNDEAD)

                self.__screen.addstr(y, scr_x, f"{board[y][x]} ", color)
                # Inc by 2 to leave a space between each Gem in the column
                scr_x += 2


        # Display generation count
        self.__screen.addstr(
            self.__height, 0,
            f"|[{self.__width}]x[{self.__height}]|{self.__pattern_name}|Wrap: {self.__wrap_edges}|Zombies: {self.__zombies}|Gen: {self.__generation}/{self.__max_gens}|",
            curses.color_pair(self.COLOR_STATUS)
        )
        self.__screen.refresh()


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
                line = re.sub(r"\s+", "", line)
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

            # If Zombies, X% chance to change live to a zombie
            if self.__zombies and int(state) and random.random() <= self.__zombies / 100.0:
                board[y+off_y][x+off_x] = self.__undead


    def __seed_randomly(self, board, percent=50):
        width = self.__width
        height = self.__height
        count = int(width * height * (percent/100))

        for _ in range(count):
            x = random.randint(0, width-1)
            y = random.randint(0, height-1)
            board[y][x] = self.__alive

            # If Zombies, X% chance to change live to a zombie
            if self.__zombies and random.random() <= self.__zombies / 100.0:
                board[y][x] = self.__undead


    def __count_neighbors(self, board, cell:tuple):
        x = cell[0]
        y = cell[1]
        width = self.__width
        height = self.__height
        counts = { "alive": 0, "undead": 0}

        for offset in self.NEIGHBOR_OFFSETS:
            nx = x + offset[0]
            ny = y + offset[1]

            if self.__wrap_edges:
                nx = width-1 if nx < 0 else nx
                nx = 0 if nx >= width else nx

                ny = height-1 if ny < 0 else ny
                ny = 0 if ny >= height else ny

            if (nx >= 0 and nx < width) and (ny >= 0 and ny < height):
                if board[ny][nx] == self.__alive:
                    counts["alive"] += 1
                elif board[ny][nx] == self.__undead:
                    counts["undead"] += 1

            # self.__debug(f"({x},{y}) - ({nx},{ny})...({board[nx][ny]})")

        return counts


    def __set_cell(self, board, cell:tuple, state, counts):
        x = cell[0]
        y = cell[1]

        alive_count = counts.get("alive", 0)
        undead_count = counts.get("undead", 0)
        total_count = alive_count + undead_count

        ## ALIVE
        if state == self.__alive:
            # A live cell with fewer than two neighbours dies
            if total_count < 2:
                board[y][x] = self.__dead
            # A live cell with 2 or 3 undead neighbors becomes undead
            elif undead_count == 2 or undead_count == 3:
                board[y][x] = self.__undead
            # A live cell with two or three live neighbours stays alive
            elif alive_count == 2 or alive_count == 3:
                board[y][x] = self.__alive
            # A live cell with more than three neighbours dies
            elif total_count > 3:
                board[y][x] = self.__dead

        ## DEAD
        elif state == self.__dead:
            # A dead cell with exactly three live neighbours becomes alive
            if alive_count == 3:
                board[y][x] = self.__alive
            # otherwise it stays dead
            else:
                board[y][x] = self.__dead

        # UNDEAD
        elif state == self.__undead:
            # An undead cell with NO live neighbours (i.e. food) has a chance to die
            if alive_count == 0:
                if random.random() <= .33:
                    board[y][x] = self.__dead
            # An undead cell with two or three live neighbours dies
            elif alive_count == 2 or alive_count == 3:
                board[y][x] = self.__dead
            # An undead cell with two or three undead neighbours stays undead
            elif undead_count == 2 or undead_count == 3:
                board[y][x] = self.__undead
            else:
                board[y][x] = self.__undead

        # self.__debug(f"{y},{x}: ({alive_count})|({undead_count})|({total_count}) [{state}] => [{board[y][x]}]", True)


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

        for y in range(self.__height):
            for x in range(self.__width):
                # self.__debug(f"{y},{x}", True)
                counts = self.__count_neighbors(old_board, (x,y))
                self.__set_cell(new_board, (x,y), old_board[y][x], counts)

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
