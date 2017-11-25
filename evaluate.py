import numpy as np

def count_zeros(grid):
    return sum(r.count(0) for r in grid)

def smoothness(grid):
    #grid2 = np.log2(np.array(grid) + 2)
    ax0 = np.diff(grid, axis=0)
    ax1 = np.diff(grid, axis=1)
    return 0.5 * (np.sum(abs(ax0)) + np.sum(abs(ax1)))

#def evaluate(grid):
#    return logic.score(grid)

def evaluate(grid):
    return -smoothness(grid) - (16 - count_zeros(grid))**2 #+ 0.1*np.sum(np.log2(np.array(grid)+2)**2)
