import cProfile
import algorithms.minimax as mm

grid = [[0,0,2,4],[0,2,8,4],[2,2,8,32],[16,16,64,128]]

cProfile.run('mm.getNextMoves(grid)')
