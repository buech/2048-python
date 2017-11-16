import logic
import numpy as np
import random
import time

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

def search_max(grid, depth, alpha, beta):
    maxScore = alpha

    if depth == 0:
        return evaluate(grid)

    #i = 0
    for move in directions:
        new_grid, moved = logic.direction(grid, move)
        if not moved:
            #i += 1
            continue
        score = search_min(grid, depth-1, maxScore, beta)
        if score > maxScore:
            maxScore = score
            if maxScore >= beta:
                break

    #if i > 3:
    #    return evaluate(grid)

    return maxScore

def search_min(grid, depth, alpha, beta):
    if depth == 0:
        return evaluate(grid)

    validMoves = generateValidMoves(grid)
    if len(validMoves[0]) == 0:
        return evaluate(grid)

    minScore = beta

    for i,j in zip(*validMoves):
        for num in [2,4]:
            new_grid = addTile(grid, i, j, num)
            score = search_max(new_grid, depth-1, alpha, minScore)
            if score < minScore:
                minScore = score
                if minScore <= alpha:
                    break

    return minScore

def countFreeTiles(grid):
    return sum(r.count(0) for r in grid)

def smoothness(grid):
    #grid2 = np.log2(np.array(grid) + 2
    ax0 = np.diff(grid, axis=0)
    ax1 = np.diff(grid, axis=1)
    return 0.5 * (np.sum(abs(ax0)) + np.sum(abs(ax1)))

#def evaluate(grid):
#    return logic.score(grid)

def evaluate(grid):
    return -smoothness(grid) - (16 - countFreeTiles(grid))**2 #+ np.log2(np.max(grid))

def getNextMoves(matrix):
    """ alrogithm to determine which moves to do next.

    return either a list of allowed moves (i.e. either 1,2,3 or 4, or as string "left", "right, "up", "down") or only the next move
    """

    maxDepth = 2
    maxScore = -INF - 1
    best_move = random.choice(directions)

    start = time.time()
    for move in directions:
        grid, moved = logic.direction(matrix, move)
        if not moved:
            continue

        score = search_min(grid, maxDepth, maxScore, INF)

        if score > maxScore:
            maxScore = score
            best_move = move

    #print score, best_move
    stop = time.time()
    #print("alpha-beta time: ", "%.4fs"%(stop-start))

    return best_move
