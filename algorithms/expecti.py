#import logic
import utils
import numpy as np
import random
import time
from evaluate import evaluate
from copy import deepcopy

"""
The minimax algorithm.
"""

directions = [1,2,3,4]
INF = 1e8

def generateValidMoves(grid):
    return np.where(np.array(grid) == 0)

def addTile(grid, i, j, num):
    grid[i][j] = num
    return grid

def search_max(grid, depth):
    maxScore = -INF

    for move in directions:
        new_grid, moved = utils.direction(tuple(map(tuple,grid)), move)
        if not moved:
            continue
        score = search_min(new_grid, depth-1)
        if score > maxScore:
            maxScore = score

    return maxScore

def search_min(grid, depth):
    if depth == 0:
        return evaluate(grid)

    validMoves = generateValidMoves(grid)
    nFreeTiles = len(validMoves[0])
    if nFreeTiles == 0:
        return evaluate(grid)

    score = 0

    for i,j in zip(*validMoves):
        for num, p in ((2, 0.9/nFreeTiles), (4, 0.1/nFreeTiles)):
            if p > 0.0:
                new_grid = addTile(deepcopy(grid), i, j, num)
                score += p * search_max(new_grid, depth)

    return score

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

        score = search_min(grid, maxDepth)

        if score > maxScore:
            maxScore = score
            best_move = move

    #print score, best_move
    #stop = time.time()
    #print("minimax time: ", "%.4fs"%(stop-start))

    return best_move
