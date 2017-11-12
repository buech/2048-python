from kcwu import *
import logic
from copy import deepcopy

ai = AI()

def getNextMoves(matrix):
    grid = deepcopy(logic.transpose(matrix))

    for i in range(4):
        for j in range(4):
            if grid[i][j] == 0:
                grid[i][j] = None

    direction = ai.getNextMove(grid)

    return direction

