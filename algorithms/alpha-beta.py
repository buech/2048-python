import utils
import random
import time
from evaluate import evaluate

"""
The minimax algorithm.
"""

directions = [1,2,3,4]
INF = 1e8

def search_max(grid, depth, alpha, beta):
    maxScore = alpha

    for move in directions:
        new_grid, moved = utils.direction(grid, move)
        if not moved:
            continue
        score = search_min(new_grid, depth-1, maxScore, beta)
        if score > maxScore:
            maxScore = score
            if maxScore >= beta:
                break

    return maxScore

def search_min(grid, depth, alpha, beta):
    if depth == 0:
        return evaluate(grid)

    free_positions = utils.get_idx_free(grid)
    if len(free_positions[0]) == 0:
        return evaluate(grid)

    minScore = beta

    for num in [2,4]:
        for i,j in zip(*free_positions):
            new_grid = utils.add_tile(grid, i, j, num)
            score = search_max(new_grid, depth, alpha, minScore)
            if score < minScore:
                minScore = score
                if minScore <= alpha:
                    break

    return minScore

def getNextMoves(matrix):
    """ alrogithm to determine which moves to do next.

    return either a list of allowed moves (i.e. either 1,2,3 or 4, or as string "left", "right, "up", "down") or only the next move
    """

    maxDepth = 1
    maxScore = -INF
    best_move = random.choice(directions)

    #start = time.time()
    for move in directions:
        grid, moved = utils.direction(tuple(map(tuple,matrix)), move)
        if not moved:
            continue

        score = search_min(grid, maxDepth, maxScore, INF)

        if score > maxScore:
            maxScore = score
            best_move = move

    #print score, best_move
    #stop = time.time()
    #print("alpha-beta time: ", "%.4fs"%(stop-start))

    return best_move
