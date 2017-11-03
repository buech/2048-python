import logic
import random

def getNextMoves(matrix):
    """ alrogithm to determine which moves to do next.

    return either a list of allowed moves (i.e. either 1,2,3 or 4, or as string "left", "right, "up", "down") or only the next move
    """

    #  if possible move to right bottom corner
    max_score = logic.score(matrix)
    same_score = []
    for i in ["right","down","left","up"]:
        temp, done = logic.direction(matrix, i)
        if not done: continue
        this_score = logic.score(temp)
        if this_score > max_score:
            max_score = this_score
            same_score = []
        if this_score == max_score:
            same_score.append(i)
    # pick one of possible directions with highest scored according to priorities
    return same_score[0]
