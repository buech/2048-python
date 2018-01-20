import numpy as np
import random
import ctypes
import bitutils
from math import log

"""
The minimax algorithm.
"""

lib = ctypes.CDLL('utils.so')

print 'Initializing tables ...'
lib.init()
print 'Done.'

lib.get_next_move.argtypes = [ctypes.c_uint64, ctypes.c_int]
lib.get_next_move.restype = ctypes.c_int

def getNextMoves(matrix):
    """ alrogithm to determine which moves to do next.

    return either a list of allowed moves (i.e. either 1,2,3 or 4, or as string "left", "right, "up", "down") or only the next move
    """

    max_depth = 2

    matrix = [[0 if x==0 else int(log(x,2)) for x in r] for r in matrix]

    board = bitutils.encode(matrix)

    best_move = lib.get_next_move(board, max_depth)

    return best_move if best_move else random.choice((1,2,3,4))
