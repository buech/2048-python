import random
import ctypes
import bitutils
from math import log
import os

lib = ctypes.CDLL(os.getcwd() + '/utils_cpp.so')

lib.init()

lib.get_next_move.argtypes = [ctypes.c_uint64, ctypes.c_int]
lib.get_next_move.restype = ctypes.c_int

def unique(a):
    u = []
    [[u.append(e) if not e in u else 0 for e in r] for r in a]
    return u

def getNextMoves(matrix):
    max_depth = max(3, len(unique(matrix)) - 2)

    matrix = [[0 if x==0 else int(log(x,2)) for x in r] for r in matrix]

    board = bitutils.encode(matrix)

    best_move = lib.get_next_move(board, max_depth)

    return best_move if best_move else random.choice((1,2,3,4))
