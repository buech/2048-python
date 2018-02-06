import utils
import random
import time
from evaluate import evaluate

directions = [1,2,3,4]
INF = 1e8

def search_max(grid, depth):
    maxScore = -INF

    for move in directions:
        new_grid, moved = utils.direction(grid, move)
        if not moved:
            continue
        score = search_min(new_grid, depth-1)
        if score > maxScore:
            maxScore = score

    return maxScore

def search_min(grid, depth):
    if depth == 0:
        return evaluate(grid)

    free_positions = utils.get_idx_free(grid)
    n_free = len(free_positions[0])
    if n_free == 0:
        return evaluate(grid)

    score = 0

    for num, p in ((2, 0.9), (4, 0.1)):
        for i,j in zip(*free_positions):
            new_grid = utils.add_tile(grid, i, j, num)
            score += p * search_max(new_grid, depth)

    return score / n_free

def getNextMoves(matrix):
    maxDepth = 1
    maxScore = -INF
    best_move = random.choice(directions)

    for move in directions:
        grid, moved = utils.direction(tuple(map(tuple,matrix)), move)
        if not moved:
            continue

        score = search_min(grid, maxDepth)

        if score > maxScore:
            maxScore = score
            best_move = move

    return best_move
