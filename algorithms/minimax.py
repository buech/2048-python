import logic
import numpy as np

"""
The minimax algorithm.
"""

directions = [1,2,3,4]
INF = 1000000000
MAX_DEPTH = 2

nextMove = 0

def generateValidMoves(player, grid):
    validMoves = []
    if player == 1:
        for d in directions:
            if logic.direction(grid, d)[1]:
                validMoves.append(d)
            else:
                pass

        return validMoves

    else:
        for i in range(4):
            for j in range(4):
                if grid[i][j] == 0:
                    validMoves.append([i,j])

        return validMoves

def addTile(grid, i, j, num):
    grid[i][j] = num
    return grid

def search_max(player, depth, grid):
    validMoves = generateValidMoves(player, grid)
    if (depth == 0) or (len(validMoves) == 0):
        return evaluate(grid)
    maxScore = -INF
    for move in validMoves:
        new_grid, done = logic.direction(grid, move)
        score = search_min(-player, depth-1, new_grid)
        if score > maxScore:
            maxScore = score
            if depth == MAX_DEPTH:
                nextMove = move

    return maxScore

def search_min(player, depth, grid):
    validMoves = generateValidMoves(player, grid)
    if (depth == 0) or (len(validMoves) == 0):
        return evaluate(grid)
    minScore = INF
    for i,j in validMoves:
        for num in [2,4]:
            new_grid = addTile(grid, i, j, num)
            score = search_max(-player, depth-1, new_grid)
            if score < minScore:
                minScore = score

    return minScore
    
def evaluate(grid):
    return logic.score(grid)

def getNextMoves(matrix):
    """ alrogithm to determine which moves to do next.

    return either a list of allowed moves (i.e. either 1,2,3 or 4, or as string "left", "right, "up", "down") or only the next move
    """
    global nextMove

    depth = MAX_DEPTH
    score = search_max(1, depth, matrix)

    print score, nextMove

    return nextMove
