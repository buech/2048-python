import random
import ctypes
from math import log
import os


solver = ctypes.CDLL(os.getcwd() + '/utils.so')

solver.init()

solver.get_next_move.argtypes = [ctypes.c_uint64, ctypes.c_int]
solver.get_next_move.restype = ctypes.c_int

def encode_row(row):
    return row[0] << 12 | row[1] << 8 | row[2] << 4 | row[3]

def encode(board):
    return (encode_row(board[0]) << 48 |
            encode_row(board[1]) << 32 |
            encode_row(board[2]) << 16 |
            encode_row(board[3]))

def unique(a):
    u = []
    [[u.append(e) if not e in u else 0 for e in r] for r in a]
    return u

def getNextMoves(matrix):
    max_depth = max(3, len(unique(matrix)) - 2)

    matrix = [[0 if x==0 else int(log(x,2)) for x in r] for r in matrix]

    board = encode(matrix)

    best_move = solver.get_next_move(board, max_depth)

    return best_move if best_move else random.choice((1,2,3,4))
