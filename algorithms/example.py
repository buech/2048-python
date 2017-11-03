import logic

def getNextMoves(matrix):
    """ alrogithm to determine which moves to do next.

    return either a list of allowed moves (i.e. either 1,2,3 or 4, or as string "left", "right, "up", "down") or only the next move
    """

    #  if possible move to right bottom corner
    mat, done = logic.right(matrix)
    if done: return ["RIGHT"]
    mat, done = logic.down(matrix)
    if done: return ["DOWN"]

    #  otherwise try to any other move
    mat, done = logic.left(matrix)
    if done: return ["LEFT", "RIGHT"]

    return ["UP", "DOWN"]
