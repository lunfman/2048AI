#!/usr/bin/python3

# runs a single game for testing the AI

import game
import search
import numpy as np

board = game.new()
moves = 0
while True:
    print(board)
    move = search.search(board)
    if move is None:
        assert game.is_lost(board)
        break

    game.make_move(board, move)
    game.spawn_tile(board)
    moves += 1

print("Final position:")
print(board)
print("%d nodes processed in total, %d moves (%.2f nodes/move)" % (search.nodes_processed, moves, search.nodes_processed / moves))

