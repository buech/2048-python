import logic

"""
The minimax algorithm.
"""

def generateValidMoves(player, grid):
    if player == 1:
        return [direction(grid, move)[1] for move in range(len(grid))]
    else:
        return 0

def search_max(player, depth, grid):
    validMoves = generateValidMoves(player, grid)
    if (depth == 0) or len(validMoves) == 0:
        

def getNextMoves(matrix):
    """ alrogithm to determine which moves to do next.

    return either a list of allowed moves (i.e. either 1,2,3 or 4, or as string "left", "right, "up", "down") or only the next move
    """
    
    depth = 1
    score, move = search_max(1, depth, matrix)

    return move
