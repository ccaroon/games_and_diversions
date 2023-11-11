#!/usr/bin/env python
import copy
import time
import pprint
import random

# * Any live cell with fewer than two live neighbours dies, as if by underpopulation.
# * Any live cell with two or three live neighbours lives on to the next generation.
# * Any live cell with more than three live neighbours dies, as if by overpopulation.
# * Any dead cell with exactly three live neighbours becomes a live cell, as if by reproduction


def create_board(width, height, fill=0):
    row = [fill] * width
    board = []
    for _ in range(height):
        board.append(copy.deepcopy(row))
    return board

def display(board):
    width = len(board[0])
    height = len(board)
    for y in range(height):
        for x in range(width):
            print(board[x][y], " ", end="")
        print()
    # pprint.pprint(board)

def seed_board(board, percent=50, marker="."):
    width = len(board[0])
    height = len(board)
    count = int(width * height * (percent/100))
    # print(width, height, count)
    for i in range(count):
        x = random.randint(0, width-1)
        y = random.randint(0, height-1)
        # print(x,y, marker)
        board[x][y] = marker


def compute_generation(old_board, new_board):
    pass

# -----------------------------------------------------------------------------

ALIVE = "*"
DEAD = " "

GEN_COUNT = 10

board1 = create_board(10,10, fill=DEAD)
# board2 = create_board(10,10, fill=DEAD)
curr_board = board1

seed_board(curr_board, percent=10, marker=ALIVE)
# curr_board[0][0] = ALIVE

for _ in range(GEN_COUNT):
    display(curr_board)
    time.sleep(1)
    seed_board(curr_board, percent=10, marker=ALIVE)
    print("\033c\033[3J", end='')







#
