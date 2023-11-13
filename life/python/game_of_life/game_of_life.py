import copy
import time
import random

class GameOfLife:

    NEIGHBOR_OFFSETS = (
        (-1,-1),(+0,-1),(+1,-1),
        (-1,+0),        (+1,+0),
        (-1,+1),(+0,+1),(+1,+1)
    )
        
    def __init__(self, width, height, **kwargs):
        self.__width = width
        self.__height = height

        self.__alive = kwargs.get("alive", "*")
        self.__dead = kwargs.get("dead", " ")

        self.__generation = 0
        self.__max_gens = kwargs.get("max_gens", 100)

        self.__board0 = self.__create_board()
        self.__board1 = self.__create_board()
        self.__boards = {
            "active": self.__board0,
            "standby": self.__board1
        }

        self.__random_seed(self.__boards["active"], percent=50)
        self.__display()

    def __create_board(self):
        row = [self.__dead] * self.__width
        board = []
        for _ in range(self.__height):
            board.append(copy.deepcopy(row))
        return board

    def __display(self):
        """ Display the ACTIVE board """
        board = self.__boards["active"]
        
        # Clear the screen
        print("\033c\033[3J", end='')
        
        # Display the board
        for y in range(self.__height):
            for x in range(self.__width):
                print(board[y][x], " ", end="")
            print()

        # Display generation count
        print(f"Generation: {self.__generation}")

    # def __seed_from_bitmap(bitmap):
    #     width = board_data["width"]
    #     for (idx, state) in enumerate(bitmap):
    #         x = idx % width
    #         y = idx // width
    #         board[y][x] = ALIVE if state else DEAD

    def __random_seed(self, board, percent=50):
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
        self.__display()

    def run(self, delay=0.5):
        for _ in range(self.__max_gens):
            self.compute_generation()
            time.sleep(delay)










# -----------------------------------------------------------------------------
