import utils_fortran
import numpy as np
import random

utils_fortran.eval.init()

def getNextMoves(matrix):
    max_depth = 2

    mat_np = np.array(matrix)
    mat_log = np.log2(mat_np, where=mat_np!=0)

    best_move = utils_fortran.expecti.get_next_move(mat_log, max_depth)

    return best_move if best_move else random.choice((1,2,3,4))
