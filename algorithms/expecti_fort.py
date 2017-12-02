import utils_fortran
import numpy as np
import random

"""
The minimax algorithm.
"""

def getNextMoves(matrix):
    """ alrogithm to determine which moves to do next.

    return either a list of allowed moves (i.e. either 1,2,3 or 4, or as string "left", "right, "up", "down") or only the next move
    """

    max_depth = 1

    best_move = utils_fortran.expecti.get_next_move(np.array(matrix), max_depth)

    return best_move if best_move else random.choice((1,2,3,4))
