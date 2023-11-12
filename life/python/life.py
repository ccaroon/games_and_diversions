#!/usr/bin/env python
import copy
import time
import pprint
import random


# 15x25
CONWAY = {
    "width": 15,
    "bitmap": [
        0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,
        0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,
        0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,
        0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,
        0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,
        0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,
        0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,
        0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,
        0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,
        0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,
        0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,
        0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,
        0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,
        0,0,0,0,0,1,1,1,0,0,0,0,0,0,0,
        0,0,0,0,0,1,0,1,0,0,0,0,0,0,0,
        0,0,0,0,0,1,0,1,0,0,0,0,0,0,0,
        0,0,0,0,0,0,1,0,0,0,0,0,0,0,0,
        0,0,0,1,0,1,1,1,0,0,0,0,0,0,0,
        0,0,0,0,1,0,1,0,1,0,0,0,0,0,0,
        0,0,0,0,0,0,1,0,0,1,0,0,0,0,0,
        0,0,0,0,0,1,0,1,0,0,0,0,0,0,0,
        0,0,0,0,0,1,0,1,0,0,0,0,0,0,0,
        0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,
        0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,
        0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,
    ]
}

def create_board(width, height, fill="."):
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
            print(board[y][x], " ", end="")
        print()
    # pprint.pprint(board)

def seed_blinker(board, x, y):
    board[y][x] = ALIVE
    board[y][x+1] = ALIVE
    board[y][x+2] = ALIVE

def seed_from_bitmap(board, board_data):
    width = board_data["width"]
    bitmap = board_data["bitmap"]
    for (idx, state) in enumerate(bitmap):
        x = idx % width
        y = idx // width
        board[y][x] = ALIVE if state else DEAD

def seed_board(board, percent=50, marker="*"):
    width = len(board[0])
    height = len(board)
    # print(width,height)
    count = int(width * height * (percent/100))
    # print(width, height, count)
    # pprint.pprint(board)
    for i in range(count):
        x = random.randint(0, width-1)
        y = random.randint(0, height-1)
        # print(x,y, marker)
        board[y][x] = marker

#  [x-1, y-1][x, y-1][x+1, y-1]
#  [x-1, y  ][x, y  ][x+1, y  ]
#  [x-1, y+1][x, y+1][x+1, y+1]
def count_live_neighbors(board, cell:tuple):
    x = cell[0]
    y = cell[1]
    width = len(board[0])
    height = len(board)
    count = 0

    offsets = (
        (-1,-1),(+0,-1),(+1,-1),
        (-1,+0),        (+1,+0),
        (-1,+1),(+0,+1),(+1,+1)
    )
    for offset in offsets:
        nx = x + offset[0]
        ny = y + offset[1]

        if (nx >= 0 and nx < width) and (ny >= 0 and ny < height):
            count += 1 if board[ny][nx] == ALIVE else 0
            # print(f"({x},{y}) - ({nx},{ny})...({board[nx][ny]})")

    # if count > 0:
    #     print(f"({x},{y})...{count}")

    return count

def set_cell(board, cell:tuple, state, count):
    x = cell[0]
    y = cell[1]

    if state == ALIVE:
        # Any live cell with fewer than two live neighbours dies
        if count < 2:
            board[y][x] = DEAD
            # print(f"{x},{y}: ALIVE --> DEAD")
        # Any live cell with two or three live neighbours lives
        elif count == 2 or count == 3:
            board[y][x] = ALIVE
            # print(f"{x},{y}: ALIVE --> ALIVE")
        # Any live cell with more than three live neighbours dies
        elif count > 3:
            board[y][x] = DEAD
            # print(f"{x},{y}: ALIVE --> DEAD")
        # else:
        #     print(f"{x},{y} - [{count}] ALIVE --> ?????")
    elif state == DEAD:
        # Any dead cell with exactly three live neighbours becomes a live cell
        if count == 3:
            board[y][x] = ALIVE
            # print(f"{x},{y}: DEAD --> ALIVE")
        else:
            board[y][x] = DEAD
            # print(f"{x},{y} - [{count}] DEAD --> DEAD")
    # else:
    #     print(f"{x},{y}: ????? --> ?????")

def compute_generation(old_board, new_board):
    width = len(old_board[0])
    height = len(old_board)
    for y in range(height):
        for x in range(width):
            count = count_live_neighbors(old_board, (x,y))
            set_cell(new_board, (x,y), old_board[y][x], count)


# -----------------------------------------------------------------------------

ALIVE = "*"
DEAD = " "

GEN_COUNT = 75

WIDTH=32
HEIGHT=32
boards = (
    create_board(WIDTH, HEIGHT, fill=DEAD),
    create_board(WIDTH, HEIGHT, fill=DEAD)
)
curr_board = boards[0]
new_board = boards[1]

seed_board(curr_board, percent=75, marker=ALIVE)
# seed_blinker(curr_board, 1, 2)
# seed_from_bitmap(curr_board, CONWAY)
# display(curr_board)

for gen in range(GEN_COUNT):
    print("\033c\033[3J", end='')
    display(curr_board)
    print(f"Generation: {gen}")
    compute_generation(curr_board, new_board)

    # swap boards
    (curr_board, new_board) = (new_board, curr_board)

    # display(curr_board)

    # input()
    time.sleep(0.25)








#
