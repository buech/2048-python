from random import *
import math

def new_game(n):
    matrix = []

    for i in range(n):
        matrix.append([0] * n)
    return matrix


def add_two(mat):
    a=randint(0,len(mat)-1)
    b=randint(0,len(mat)-1)
    while(mat[a][b]!=0):
        a=randint(0,len(mat)-1)
        b=randint(0,len(mat)-1)
    mat[a][b]=2 if randint(1,10)>1 else 4
    return mat

def game_state(mat, endless_mode = False):
    if not endless_mode:
        for i in range(len(mat)):
            for j in range(len(mat[0])):
                if mat[i][j]==2048:
                    return 'win'
    for i in range(len(mat)-1): #intentionally reduced to check the row on the right and below
        for j in range(len(mat[0])-1): #more elegant to use exceptions but most likely this will be their solution
            if mat[i][j]==mat[i+1][j] or mat[i][j+1]==mat[i][j]:
                return 'not over'
    for i in range(len(mat)): #check for any zero entries
        for j in range(len(mat[0])):
            if mat[i][j]==0:
                return 'not over'
    for k in range(len(mat)-1): #to check the left/right entries on the last row
        if mat[len(mat)-1][k]==mat[len(mat)-1][k+1]:
            return 'not over'
    for j in range(len(mat)-1): #check up/down entries on last column
        if mat[j][len(mat)-1]==mat[j+1][len(mat)-1]:
            return 'not over'
    return 'lose'

def reverse(mat):
    new=[]
    for i in range(len(mat)):
        new.append([])
        for j in range(len(mat[0])):
            new[i].append(mat[i][len(mat[0])-j-1])
    return new

def transpose(mat):
    new=[]
    for i in range(len(mat[0])):
        new.append([])
        for j in range(len(mat)):
            new[i].append(mat[j][i])
    return new

def cover_up(mat):
    new = new_game(len(mat))
    done=False
    for i in range(len(mat)):
        count=0
        for j in range(len(mat)):
            if mat[i][j]!=0:
                new[i][count]=mat[i][j]
                if j!=count:
                    done=True
                count+=1
    return (new,done)

def merge(mat):
    done=False
    for i in range(len(mat)):
         for j in range(len(mat)-1):
             if mat[i][j]==mat[i][j+1] and mat[i][j]!=0:
                 mat[i][j]*=2
                 mat[i][j+1]=0
                 done=True
    return (mat,done)

def direction(game, direction):
    if type(direction) == str:
        if direction.lower() == "up":
            direction = 1
        elif direction.lower() == "down":
            direction = 2
        elif direction.lower() == "right":
            direction = 3
        elif direction.lower() == "left":
            direction = 4
    if direction==1:
        return up(game)
    elif direction==2:
        return down(game)
    elif direction==3:
        return right(game)
    elif direction==4:
        return left(game)

def up(game):
        # print("up")
        # return matrix after shifting up
        game=transpose(game)
        game,done=cover_up(game)
        temp=merge(game)
        game=temp[0]
        done=done or temp[1]
        game=cover_up(game)[0]
        game=transpose(game)
        return (game,done)

def down(game):
        # print("down")
        game=reverse(transpose(game))
        game,done=cover_up(game)
        temp=merge(game)
        game=temp[0]
        done=done or temp[1]
        game=cover_up(game)[0]
        game=transpose(reverse(game))
        return (game,done)

def left(game):
        # print("left")
        # return matrix after shifting left
        game,done=cover_up(game)
        temp=merge(game)
        game=temp[0]
        done=done or temp[1]
        game=cover_up(game)[0]
        return (game,done)

def right(game):
        # print("right")
        # return matrix after shifting right
        game=reverse(game)
        game,done=cover_up(game)
        temp=merge(game)
        game=temp[0]
        done=done or temp[1]
        game=cover_up(game)[0]
        game=reverse(game)
        return (game,done)

def score(matrix):
    """ calculated the score
    Adds scores if each cell, where each cell has a score according to:
    2 -> 3
    4 -> 9
    8 -> 27
    ...
    """
    total_score = 0
    for i in range(len(matrix)):
        for j in range(len(matrix[0])):
            if matrix[i][j] > 0:
                total_score += 3 ** math.log(matrix[i][j], 2)
    return int(total_score)