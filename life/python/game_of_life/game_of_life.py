import copy
import curses
import time
import random

import game_of_life.patterns as gol_patterns

class GameOfLife:
    """ Conway's Game of Life Simulator """

    COLOR_CELL = 1
    COLOR_BLACK_GREEN = 2

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
        
        self.__screen = stdscr

        self.__width = width
        if self.__width == -1:
            self.__width = curses.COLS // 2
        
        self.__height = height
        if self.__height == -1:
            self.__height = curses.LINES-1

        # COLS // 2 b/c a ' ' is printed between chars
        if self.__height > curses.LINES or self.__width > curses.COLS // 2:
            raise ValueError(f"Screen too small: Max Width: {curses.COLS // 2} | Max Height: {curses.LINES-1}")

        self.__alive = kwargs.get("alive", "*")
        self.__dead = kwargs.get("dead", " ")

        self.__generation = 0
        self.__max_gens = kwargs.get("max_gens", 100)

        self.__delay = kwargs.get("delay", 0.25)

        self.__board0 = self.__create_board()
        self.__board1 = self.__create_board()
        self.__boards = {
            "active": self.__board0,
            "standby": self.__board1
        }

        pattern_name = kwargs.get("pattern")
        pattern = gol_patterns.PATTERNS.get(pattern_name)
        if pattern:            
            self.__seed_from_pattern(
                self.__boards["active"], 
                pattern,
                center=True
            )
        else:
            self.__seed_randomly(self.__boards["active"], percent=50)

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

    def __display2(self):
        """ Display ACTIVE board w/ Curses """
        board = self.__boards["active"]
        # Display the board
        for y in range(self.__height):
            line = "  ".join(board[y])
            self.__screen.addstr(y, 0, line, curses.color_pair(self.COLOR_CELL))

        # Display generation count
        self.__screen.addstr(
            self.__height, 0, 
            f"|[{self.__width}]x[{self.__height}]|Generation: {self.__generation}|",
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

    def __seed_from_pattern(self, board, pattern, offset:tuple=(0,0), center=False):
        pat_width = pattern["width"]
        pat_height = pattern["height"]

        if pat_width > self.__width or pat_height > self.__height:
            raise ValueError(f"Board size to small for pattern. Min Size: ({pat_width}x{pat_height})")

        # Compute offset to center pattern on board
        if center:
            # // 4 b/c cells are printed with a ' ' between them
            off_x = (self.__width // 4) - (pat_width // 4)
            off_y = (self.__height // 2) - (pat_height // 2)
        else:
            off_x = offset[0]
            off_y = offset[1]

        bitmap = pattern["bitmap"]
        for (idx, state) in enumerate(bitmap):
            x = idx % pat_width
            y = idx // pat_width
            board[y+off_y][x+off_x] = self.__alive if state else self.__dead

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

            if (nx >= 0 and nx < width) and (ny >= 0 and ny < height):
                count += 1 if board[ny][nx] == self.__alive else 0
                # print(f"({x},{y}) - ({nx},{ny})...({board[nx][ny]})")

        # if count > 0:
        #     print(f"({x},{y})...{count}")

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
