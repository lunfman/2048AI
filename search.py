#!/usr/bin/python3

# game tree search and evaluation

import numpy as np
import game

snake = np.array([[13, 14, 15, 16], [12, 11, 10, 9], [5, 6, 7, 8], [4, 3, 2, 1]])
snake = np.float64(2) ** (-snake)
def evaluate(board):
    # encourage the snake formation, more empty tiles
    s1 = (snake * board).sum() 
    s2 = (np.flip(snake, axis=(0, 1)) * board).sum() 
    s3 = (np.flip(snake.T, axis=0) * board).sum() 
    s4 = (np.flip(snake.T, axis=1) * board).sum()
    return np.max([s1, s2, s3, s4]) + (board == 0).sum() * 1

nodes_processed = 0
def expectimax(board, depth):
    global nodes_processed
    nodes_processed += 1

    if game.is_lost(board):
        return -1
    if depth == 0:
        return evaluate(board)

    exp = 0
    sp = 0
    moves = np.array(game.generate_chance_moves(board))
    # to speed up search we can check a randomly selected subset of possible moves
    # selected_moves = np.random.default_rng().choice(moves, size=int(np.ceil(len(moves) * 1)), replace=False, p=moves[:, 3]):
    for x, y, v, p in moves:
        x, y, v = int(x), int(y), int(v)
        board[y][x] = v
        value = -1
        for move in [game.U, game.D, game.R, game.L]:
            b = board.copy()
            game.make_move(b, move)
            if np.all(b == board):
                continue
            
            value = max(value, expectimax(b, depth - 1))

        exp += value * p
        sp += p
        board[y][x] = 0
    exp /= sp

    return exp

def search(board):
    depth = 2 # 3 is too slow (>1 min per move)
    bestmove = None
    bestvalue = -1
    for move in [game.U, game.D, game.R, game.L]:
        b = board.copy()
        game.make_move(b, move)
        if np.all(b == board):
            continue

        value = expectimax(b, depth)
        if value >= bestvalue:
            bestvalue = value
            bestmove = move

    return bestmove

def ai(board):
    # check the dimensions
    if len(board) != 4 or len(board[0]) != 4:
        print('wrong board dimensions:')
        print(board)

    # check that each value is indeed a power of two
    for i in range(len(board)):
        for j in range(len(board[0])):
            v = board[i][j]
            if v == 0: continue
            nv = 2**int(np.log2(v))
            if v & (v - 1):
                print(f'invalid value {v}, assuming {nv}:')
                print(board)
            board[i][j] = nv

    board = np.array([[(int(np.log2(i)) if i > 0 else 0) for i in row] for row in board])
    move = search(board)
    if move == None:
        print('game over')
        return "left"
    return {game.U:'up', game.D:'down', game.R:'right', game.L:'left'}[move]


