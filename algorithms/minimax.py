import logic
import numpy as np
import random

"""
The minimax algorithm.
"""

directions = [1,2,3,4]
INF = 1e8

def generateValidMoves(grid):
    validMoves = []
    for i in range(4):
        for j in range(4):
            if grid[i][j] == 0:
                validMoves.append([i,j])

    return validMoves

def addTile(grid, i, j, num):
    grid[i][j] = num
    return grid

def search_max(grid, depth):
    maxScore = -INF

    if depth == 0:
        return evaluate(grid)

    #i = 0
    for move in directions:
        new_grid, moved = logic.direction(grid, move)
        if not moved:
            #i += 1
            continue
        score = search_min(grid, depth-1)
        if score > maxScore:
            maxScore = score

    #if i > 3:
    #    return evaluate(grid)

    return maxScore

def search_min(grid, depth):
    validMoves = generateValidMoves(grid)

    if (depth == 0) or (len(validMoves) == 0):
        return evaluate(grid)

    minScore = INF

    for i,j in validMoves:
        for num in [2,4]:
            new_grid = addTile(grid, i, j, num)
            score = search_max(new_grid, depth-1)
            if score < minScore:
                minScore = score

    return minScore

def countFreeTiles(grid):
    return sum(r.count(0) for r in grid)

def smoothness(grid):
    ax0 = np.diff(grid, axis=0)
    ax1 = np.diff(grid, axis=1)
    return 0.5 * (np.sum(abs(ax0)) + np.sum(abs(ax1)))

#def evaluate(grid):
#    return logic.score(grid)

def evaluate(grid):
    return np.log10(logic.score(grid)) - smoothness(grid) - (16 - countFreeTiles(grid))**2

def getNextMoves(matrix):
    """ alrogithm to determine which moves to do next.

    return either a list of allowed moves (i.e. either 1,2,3 or 4, or as string "left", "right, "up", "down") or only the next move
    """

    maxDepth = 3
    maxScore = -INF
    best_move = random.choice(directions)

    for move in directions:
        grid, moved = logic.direction(matrix, move)
        if not moved:
            continue

        score = search_min(grid, maxDepth)

        if score > maxScore:
            maxScore = score
            best_move = move

    #print score, best_move

    return best_move
