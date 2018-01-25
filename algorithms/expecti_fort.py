import utils_fortran
import numpy as np
import random

utils_fortran.utils.init_tables()

def unique(a):
    u = []
    [[u.append(e) if not e in u else 0 for e in r] for r in a]
    return u

def getNextMoves(matrix):
    max_depth = 2#max(3, len(unique(matrix)) - 2)

    mat_np = np.array(matrix)
    mat_log = np.log2(mat_np, where=mat_np!=0)

    best_move = utils_fortran.expecti.get_next_move(mat_log, max_depth)

    return best_move if best_move else random.choice((1,2,3,4))
