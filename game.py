#!/usr/bin/python3

# game rules and logic
# game board is represented as a 2d numpy array that stores exponents (1 for 2, 2 for 4 etc.)

import numpy as np

U = 1
D = 2
R = 3
L = 4

W = 4
H = 4

TILE_PROBABILITY = {1: 0.9, 2: 0.1}

# returns a new random tile value according to TILE_PROBABILITY
def get_random_tile():
    return np.random.choice(list(TILE_PROBABILITY.keys()), p=list(TILE_PROBABILITY.values()))

def get_empty_tiles(board):
    return [(j, i) for i in range(W) for j in range(H) if board[j][i] == 0]

# spawns a new tile in an empty square
def spawn_tile(board):
    empty_tiles = get_empty_tiles(board)
    y, x = empty_tiles[np.random.randint(len(empty_tiles))]
    board[y][x] = get_random_tile()

# creates a new board with two random tiles in it
def new():
    b = np.zeros((H, W), dtype=int)
    spawn_tile(b)
    spawn_tile(b)
    return b

# change 'board' according to 'move'
def make_move(board, move):
    # transform the board so it always looks like we're doing the 'down' push
    t = board
    if move == D:
        t = np.flip(board, axis=0)
    elif move == R:
        t = np.flip(board.T, axis=0)
    elif move == L:
        t = np.flip(board.T, axis=1)

    # logic
    for x in range(t.shape[1]):
        c = 0
        for y in range(1, t.shape[0]):
            if t[y][x] == 0:
                continue

            if t[y][x] == t[c][x]:
                t[c][x] += 1
                t[y][x] = 0
                c += 1
            elif t[c][x] == 0:
                t[c][x] = t[y][x]
                t[y][x] = 0
            else:
                if y > c + 1:
                    t[c + 1][x] = t[y][x]
                    t[y][x] = 0
                c += 1
    
    return board

# all possible ways a new tile can spawn
def generate_chance_moves(board):
    moves = []
    empty_tiles = get_empty_tiles(board)
    for y, x in empty_tiles:
        for v, p in TILE_PROBABILITY.items():
            moves.append((x, y, v, p / len(empty_tiles)))
    return moves

# game is lost if (and only if) there are no empty tiles and no two adjacent tiles with the same value
def is_lost(board):
    if board.min() == 0:
        return False

    for y in range(H - 1):
        for x in range(W - 1):
            if board[y][x] == board[y][x + 1] or board[y][x] == board[y + 1][x]:
                return False

    return True
