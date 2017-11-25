import cProfile
from algorithms import minimax, alpha_beta, expecti

grid = [[0,0,2,4],[0,2,8,4],[2,2,8,32],[16,16,64,128]]

sort_key = 'cumtime'

cProfile.run('minimax.getNextMoves(grid)', sort=sort_key)
cProfile.run('alpha_beta.getNextMoves(grid)', sort=sort_key)
cProfile.run('expecti.getNextMoves(grid)', sort=sort_key)
