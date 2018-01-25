import logic
import random
import tabulate
import math

"""
 - Try to gather cells in lower left corner.
 - Think a number of times ahead, depending on how many steps have 
already been taken
 - Criterion, which decides direction: normal Score + bonus for tiles 
with zero + bonus for merges in left-hand column (the more the earlier
they happen)
"""

class Mufflons:
    """ class which organises the thinking ahead procedure
    """ 
    def Init(self,matrix,directions,n):
        self.maxScore   = logic.score(matrix)
        self.matrix     = matrix
        self.directions = directions
        self.sameScore  = []
        # vector of directions: last entry is the one of 1st move,
        # 2nd to the last entry is the one of the 2nd move ...
        self.dirVector     = [] 
        # vector of matrices: last entry is the matrix with which is
        # started, 2nd to the last entry is the one of the 1st move ...
        self.matVector     = [] 
        for i in range(n): self.dirVector.append("empty")
        for i in range(n+1): self.matVector.append(matrix)
        self.nmax       = n

    def markTiles(self, mat):
        """ marks tiles which may be occupied with new number
        """ 
        coordinates = []
        for i in range(len(mat)):
            for j in range(len(mat)):
                if mat[i][j] == 0:
                    #mat[i][j] = 1
                    coordinates.append([i,j])
        print coordinates
        if coordinates!=[]: return coordinates

    def traceMergingTiles(self, mat1, mat2, direction):
        """ ascertain whether there was a merge in left most
            column (when going from mat11 to mat2), 
            if so find out which tiles merged
        """
#        print "go to {}".format(direction)
        coord_merging1 = [] # array of coordinates of daughter tile 1 of merge
        coord_merging2 = [] # array of coordinates of daughter tile 1 of merge
        coord_merged   = [] # array of coordinates of mother tile of merge

        if direction=='LEFT' or direction=='RIGHT':
            row_score1 = [0,0,0,0]
            row_score2 = [0,0,0,0]
            rows = []
            for i in range(len(mat1)):
                for j in range(len(mat1)):
                    if mat1[i][j] != 0:
                        row_score1[i] += 3 ** math.log(mat1[i][j], 2)
                    if mat2[i][j] != 0:
                        row_score2[i] += 3 ** math.log(mat2[i][j], 2)

            for i in range(len(mat1)):
                if row_score1[i] != row_score2[i]: 
#                    print "merge in row {}".format(i)
                    rows.append(i)

            for i in rows:
                if direction=='LEFT':
                    # check which tiles merge to which, when moving left
                    # merges which end up in left most (0th) column
                    if mat1[i][0] != 0:
                        if mat1[i][0] == mat1[i][1] and mat1[i][2] == mat1[i][3] and mat1[i][2] != 0: 
#                            print "merged tiles [{}][{}] and [{}][{}] to [{}][{}]".format(i,0,i,1,i,0)
#                            print "merged tiles [{}][{}] and [{}][{}] to [{}][{}]".format(i,2,i,3,i,2)
                            coord_merging1.append([i,0])
                            coord_merging2.append([i,1])
                            coord_merged.append([i,0])
                            coord_merging1.append([i,2])
                            coord_merging2.append([i,3])
                            coord_merged.append([i,2])
                            continue
                        elif mat1[i][0] == mat1[i][1]:
#                            print "merged tiles [{}][{}] and [{}][{}] to [{}][{}]".format(i,0,i,1,i,0)
                            coord_merging1.append([i,0])
                            coord_merging2.append([i,1])
                            coord_merged.append([i,0])
                            continue
                        elif mat1[i][1] == 0 and mat1[i][0] == mat1[i][2]:
#                            print "merged tiles [{}][{}] and [{}][{}] to [{}][{}]".format(i,0,i,2,i,0)
                            coord_merging1.append([i,0])
                            coord_merging2.append([i,2])
                            coord_merged.append([i,0])
                            continue
                        elif mat1[i][1] == 0 and mat1[i][2] == 0 and mat1[i][0] == mat1[i][3]:
#                            print "merged tiles [{}][{}] and [{}][{}] to [{}][{}]".format(i,0,i,3,i,0)
                            coord_merging1.append([i,0])
                            coord_merging2.append([i,3])
                            coord_merged.append([i,0])
                            continue
                    if mat1[i][0] == 0 and mat1[i][1] != 0:
                        if mat1[i][1] == mat1[i][2]:
#                            print "merged tiles [{}][{}] and [{}][{}] to [{}][{}]".format(i,1,i,2,i,0)
                            coord_merging1.append([i,1])
                            coord_merging2.append([i,2])
                            coord_merged.append([i,0])
                            continue
                        elif mat1[i][2] == 0 and mat1[i][1] == mat1[i][3]:
#                            print "merged tiles [{}][{}] and [{}][{}] to [{}][{}]".format(i,1,i,3,i,0)##########
                            coord_merging1.append([i,1])
                            coord_merging2.append([i,3])
                            coord_merged.append([i,0])
                            continue
                    if mat1[i][0] == 0 and mat1[i][1] == 0 and mat1[i][2] != 0:
                        if mat1[i][2] == mat1[i][3]:
#                            print "merged tiles [{}][{}] and [{}][{}] to [{}][{}]".format(i,2,i,3,i,0)
                            coord_merging1.append([i,2])
                            coord_merging2.append([i,3])
                            coord_merged.append([i,2])
                            continue
                    # merges which end up in 1st column
                    if mat1[i][1] != 0:
                        if mat1[i][1] == mat1[i][2]:
#                            print "merged tiles [{}][{}] and [{}][{}] to [{}][{}]".format(i,1,i,2,i,1)
                            coord_merging1.append([i,1])
                            coord_merging2.append([i,2])
                            coord_merged.append([i,1])
                            continue
                        elif mat1[i][2] == 0 and mat1[i][1] == mat1[i][3]:
#                            print "merged tiles [{}][{}] and [{}][{}] to [{}][{}]".format(i,1,i,3,i,1)
                            coord_merging1.append([i,1])
                            coord_merging2.append([i,3])
                            coord_merged.append([i,1])
                            continue
                    if mat1[i][1] == 0 and mat1[i][2] == 0:
                        if mat1[i][2] == mat1[i][3]:
#                            print "merged tiles [{}][{}] and [{}][{}] to [{}][{}]".format(i,2,i,3,i,1)
                            coord_merging1.append([i,2])
                            coord_merging2.append([i,3])
                            coord_merged.append([i,1])
                            continue
                    # merges which end up in 2nd column
                    if mat1[i][2] != 0:
                        if mat1[i][2] == mat1[i][3]: 
#                            print "merged tiles [{}][{}] and [{}][{}] to [{}][{}]".format(i,2,i,3,i,2)
                            coord_merging1.append([i,2])
                            coord_merging2.append([i,3])
                            coord_merged.append([i,2])
                            continue

        if direction=='DOWN' or direction=='UP':
            column_score1 = [0,0,0,0]
            column_score2 = [0,0,0,0]
            columns = []
            for i in range(len(mat1)):
                for j in range(len(mat1)):
                    if mat1[j][i] != 0:
                        column_score1[i] += 3 ** math.log(mat1[j][i], 2)
                    if mat2[j][i] != 0:
                        column_score2[i] += 3 ** math.log(mat2[j][i], 2)
            for i in range(len(mat1)):
                if column_score1[i] != column_score2[i]: 
#                    print "merge in column {}".format(i)
                    columns.append(i)

            for i in columns:
                if direction=='UP':
                    # check which tiles merge to which, when moving up
                    # merges which end up in upper most (0th) row
                    if mat1[0][i] != 0:
                        if mat1[0][i] == mat1[1][i] and mat1[2][i] == mat1[3][i] and mat1[2][i] != 0: 
#                            print "merged tiles [{}][{}] and [{}][{}] to [{}][{}]".format(0,i,1,i,0,i)
#                            print "merged tiles [{}][{}] and [{}][{}] to [{}][{}]".format(2,i,3,i,2,i)
                            coord_merging1.append([0,i])
                            coord_merging2.append([1,i])
                            coord_merged.append([0,i])
                            coord_merging1.append([2,i])
                            coord_merging2.append([3,i])
                            coord_merged.append([2,i])
                            continue
                        elif mat1[0][i] == mat1[1][i]:
#                            print "merged tiles [{}][{}] and [{}][{}] to [{}][{}]".format(0,i,1,i,0,i)
                            coord_merging1.append([0,i])
                            coord_merging2.append([1,i])
                            coord_merged.append([0,i])
                            continue
                        elif mat1[1][i] == 0 and mat1[0][i] == mat1[2][i]:
#                            print "merged tiles [{}][{}] and [{}][{}] to [{}][{}]".format(0,i,2,i,0,i)
                            coord_merging1.append([0,i])
                            coord_merging2.append([2,i])
                            coord_merged.append([0,i])
                            continue
                        elif mat1[1][i] == 0 and mat1[2][i] == 0 and mat1[0][i] == mat1[3][i]:
#                            print "merged tiles [{}][{}] and [{}][{}] to [{}][{}]".format(0,i,3,i,0,i)
                            coord_merging1.append([0,i])
                            coord_merging2.append([3,i])
                            coord_merged.append([0,i])
                            continue
                    if mat1[0][i] == 0 and mat1[1][i] != 0:
                        if mat1[1][i] == mat1[2][i]:
#                            print "merged tiles [{}][{}] and [{}][{}] to [{}][{}]".format(1,i,2,i,0,i)
                            coord_merging1.append([1,i])
                            coord_merging2.append([2,i])
                            coord_merged.append([0,i])
                            continue
                        elif mat1[2][i] == 0 and mat1[1][i] == mat1[3][i]:
#                            print "merged tiles [{}][{}] and [{}][{}] to [{}][{}]".format(1,i,3,i,0,i)
                            coord_merging1.append([1,i])
                            coord_merging2.append([3,i])
                            coord_merged.append([0,i])
                            continue
                    if mat1[0][i] == 0 and mat1[1][i] == 0 and mat1[2][i] != 0:
                        if mat1[2][i] == mat1[3][i]:
#                            print "merged tiles [{}][{}] and [{}][{}] to [{}][{}]".format(2,i,3,i,0,i)
                            coord_merging1.append([2,i])
                            coord_merging2.append([3,i])
                            coord_merged.append([0,i])
                            continue
                    # merges which end up in 1st row
                    if mat1[1][i] != 0:
                        if mat1[1][i] == mat1[2][i]:
#                            print "merged tiles [{}][{}] and [{}][{}] to [{}][{}]".format(1,i,2,i,1,i)
                            coord_merging1.append([1,i])
                            coord_merging2.append([2,i])
                            coord_merged.append([1,i])
                            continue
                        elif mat1[2][i] == 0 and mat1[1][i] == mat1[3][i]:
#                            print "merged tiles [{}][{}] and [{}][{}] to [{}][{}]".format(1,i,3,i,1,i)
                            coord_merging1.append([1,i])
                            coord_merging2.append([3,i])
                            coord_merged.append([1,i])
                            continue
                    if mat1[1][i] == 0 and mat1[2][i] == 0:
                        if mat1[2][i] == mat1[3][i]:
#                            print "merged tiles [{}][{}] and [{}][{}] to [{}][{}]".format(2,i,3,i,1,i)
                            coord_merging1.append([2,i])
                            coord_merging2.append([3,i])
                            coord_merged.append([1,i])
                            continue
                    # merges which end up in 2nd column
                    if mat1[2][i] != 0:
                        if mat1[2][i] == mat1[3][i]: 
#                            print "merged tiles [{}][{}] and [{}][{}] to [{}][{}]".format(2,i,3,i,2,i)
                            coord_merging1.append([2,i])
                            coord_merging2.append([3,i])
                            coord_merged.append([2,i])
                            continue

                if direction=='DOWN':
                    # check which tiles merge to which, when moving down
                    # merges which end up in lower most (3rd) row
                    if mat1[3][i] != 0:
                        if mat1[3][i] == mat1[2][i] and mat1[1][i] == mat1[0][i] and mat1[3][i] != 0: 
#                            print "merged tiles [{}][{}] and [{}][{}] to [{}][{}]".format(3,i,2,i,3,i)
#                            print "merged tiles [{}][{}] and [{}][{}] to [{}][{}]".format(1,i,0,i,1,i)
                            coord_merging1.append([3,i])
                            coord_merging2.append([2,i])
                            coord_merged.append([3,i])
                            coord_merging1.append([1,i])
                            coord_merging2.append([0,i])
                            coord_merged.append([1,i])
                            continue
                        elif mat1[3][i] == mat1[2][i]:
#                            print "merged tiles [{}][{}] and [{}][{}] to [{}][{}]".format(3,i,2,i,3,i)
                            coord_merging1.append([3,i])
                            coord_merging2.append([2,i])
                            coord_merged.append([3,i])
                            continue
                        elif mat1[2][i] == 0 and mat1[3][i] == mat1[1][i]:
#                            print "merged tiles [{}][{}] and [{}][{}] to [{}][{}]".format(3,i,1,i,3,i)
                            coord_merging1.append([3,i])
                            coord_merging2.append([1,i])
                            coord_merged.append([3,i])
                            continue
                        elif mat1[2][i] == 0 and mat1[1][i] == 0 and mat1[3][i] == mat1[0][i]:
#                            print "merged tiles [{}][{}] and [{}][{}] to [{}][{}]".format(3,i,0,i,3,i)
                            coord_merging1.append([3,i])
                            coord_merging2.append([0,i])
                            coord_merged.append([3,i])
                            continue
                    if mat1[3][i] == 0 and mat1[2][i] != 0:
                        if mat1[2][i] == mat1[1][i]:
#                            print "merged tiles [{}][{}] and [{}][{}] to [{}][{}]".format(2,i,1,i,3,i)
                            coord_merging1.append([2,i])
                            coord_merging2.append([1,i])
                            coord_merged.append([3,i])
                            continue
                        elif mat1[1][i] == 0 and mat1[2][i] == mat1[0][i]:
#                            print "merged tiles [{}][{}] and [{}][{}] to [{}][{}]".format(2,i,0,i,3,i)
                            coord_merging1.append([2,i])
                            coord_merging2.append([0,i])
                            coord_merged.append([1,i])
                            continue
                    if mat1[3][i] == 0 and mat1[2][i] == 0 and mat1[1][i] != 0:
                        if mat1[1][i] == mat1[0][i]:
#                            print "merged tiles [{}][{}] and [{}][{}] to [{}][{}]".format(1,i,0,i,3,i)
                            coord_merging1.append([1,i])
                            coord_merging2.append([0,i])
                            coord_merged.append([3,i])
                            continue
                    # merges which end up in 2nd row
                    if mat1[2][i] != 0:
                        if mat1[2][i] == mat1[1][i]:
#                            print "merged tiles [{}][{}] and [{}][{}] to [{}][{}]".format(2,i,1,i,2,i)
                            coord_merging1.append([2,i])
                            coord_merging2.append([1,i])
                            coord_merged.append([2,i])
                            continue
                        elif mat1[1][i] == 0 and mat1[2][i] == mat1[0][i]:
#                            print "merged tiles [{}][{}] and [{}][{}] to [{}][{}]".format(2,i,0,i,2,i)
                            coord_merging1.append([2,i])
                            coord_merging2.append([0,i])
                            coord_merged.append([2,i])
                            continue
                    if mat1[2][i] == 0 and mat1[1][i] == 0:
                        if mat1[1][i] == mat1[0][i]:
#                            print "merged tiles [{}][{}] and [{}][{}] to [{}][{}]".format(1,i,0,i,2,i)
                            coord_merging1.append([1,i])
                            coord_merging2.append([0,i])
                            coord_merged.append([2,i])
                            continue
                    # merges which end up in 3rd column
                    if mat1[1][i] != 0:
                        if mat1[1][i] == mat1[0][i]: 
#                            print "merged tiles [{}][{}] and [{}][{}] to [{}][{}]".format(1,i,0,i,1,i)
                            coord_merging1.append([1,i])
                            coord_merging2.append([0,i])
                            coord_merged.append([1,i])
                            continue
        if coord_merged==[]: return "no merge"
        if coord_merged!=[]: return [coord_merged, coord_merging1, coord_merging2]


    def myScore(self, matrix):
        """ count number of zeros and assign positive weight for them
        """
        thisScore = logic.score(matrix)
        # add bonus for tiles with zero
        for i in range(len(matrix)-1): 
            for j in range(len(matrix)-1): 
                if matrix[i][j]==0: thisScore += (self.nmax-1)*10
        # add bonus for merge in left most column, the earlier, the better        
        for n in range(self.nmax-1):
            mat1 = self.matVector[self.nmax-n]
            mat2 = self.matVector[self.nmax-n-1]
            direction = self.dirVector[self.nmax-n-1]
            coord = self.traceMergingTiles(mat1,mat2,direction)
            if coord=="no merge": continue
            coord_merged = coord[0]
            coord_merging1 = coord[1]
            coord_merging2 = coord[2]
            for i in range(len(coord_merged)):
                # check whether x-coordinate of every merged tile is 0, i.e. in left most column
                # and at least one of the merging tiles does not come from column 0
                if coord_merged[i][1] == 0 and (coord_merging1[i][1] > 0 or coord_merging2[i][1] > 0): 
#                    print "merged in left most column occured in {} in step {}".format(coord_merged[i], n+1)
#                    print self.dirVector
#                    print "merged tile has value {}".format(mat2[coord_merged[i][0]][coord_merging1[i][1]])
                    thisScore += 1.*(self.nmax-n)/(self.nmax) *mat2[coord_merged[i][0]][coord_merging1[i][1]]
        return thisScore

    def nLoops(self,n):
        """ simulate all possible outcomes for going n steps
            and take from the sequence, which leads the highest score
            the first step
        """
        if n>1: 
            for i in self.directions:
                self.matVector[n-1], done = \
                logic.direction(self.matVector[n], i)
                if not done: continue
                # todo: check whether merge in left column has happend
                self.dirVector[n-1]=i
                #self.traceMergingTiles(self.matVector[n],self.matVector[n-1],i)
                self.nLoops(n-1)
        else:
            for i in self.directions:
                self.matVector[n-1], done = logic.direction(self.matVector[n], i)
                if not done: continue
                self.dirVector[n-1]=i
                #self.vetoMoves() # method should return boolian
                if self.nmax>1: thisScore = self.myScore(self.matVector[n-1])
                else: thisScore = logic.score(self.matVector[n-1])
                if thisScore > self.maxScore: # todo: include veto of vetoMoves() here
                    self.maxScore = thisScore
                    self.sameScore = []
                if thisScore == self.maxScore: # todo: include veto of vetoMoves() here
#                    print "dirVector = {}".format(self.dirVector)
#                    print "dirVector[nmax-1] = {}".format(self.dirVector[self.nmax-1])
                    # append first direction in decision tree
                    self.sameScore.append(self.dirVector[self.nmax-1])
#                    print(tabulate.tabulate(self.matVector[n-1], tablefmt="grid"))
#                    print "samescore = {}".format(self.sameScore)

    def nAhead(self,matrix,directions,n):
        self.Init(matrix,directions,n)
        self.nLoops(n)
        if self.sameScore!=[]:  
            mat, trash = logic.direction(matrix,self.sameScore[0])
#            print(tabulate.tabulate(mat, tablefmt="grid"))
        if self.sameScore==[] and n>1: 
#            print "try one step less"
            self.nAhead(matrix,directions,n-1)
        if self.sameScore!=[]: return self.sameScore[0]


def columnMoveable(matrix, i):
    """ checks whether ith column is moveable
        i==0 is left most column
        i==1 is second coumn to the left ...
    """
    return matrix[0][i]==0 or matrix[1][i]==0 \
    or matrix[2][i]==0 or matrix[3][i]==0 \
    or matrix[0][i]==matrix[1][i] \
    or matrix[1][i]==matrix[2][i] \
    or matrix[2][i]==matrix[3][i] 

def procedure(matrix,think,j):
    """ try to go in lower left corner by optimising 
        score, by thinking j times ahead
    """

    if not columnMoveable(matrix,0): 
        move = think.nAhead(matrix,["LEFT","DOWN","UP"],j)
#        move = think.nAhead(matrix,["LEFT","UP","DOWN"],j)
        if move: return move

#    print "try left or down"
    move = think.nAhead(matrix,["LEFT","DOWN"],j)
    if move: return move

    # otherwise go up or right+left
#    print "try up and down"
    mat, done = logic.up(matrix)
    if done: return ["UP","DOWN"] # todo: down must not be possible
    return ["RIGHT","LEFT"]

def getNextMoves(matrix):
    """ alrogithm to determine which moves to do next.
    return one direction or list of them
    """
    # increment counter of calls
    if not hasattr(getNextMoves, "counter"):
        getNextMoves.counter = 0
    getNextMoves.counter += 1
#    print "-------------------------------------------"
#    print getNextMoves.counter

    think = Mufflons()

    # in 50 first moves 
    if getNextMoves.counter <= 50: return procedure(matrix,think,1)
    
    # in move 51-100 
    elif getNextMoves.counter <= 100: return procedure(matrix,think,2)
    
    # in move 101-150 
    elif getNextMoves.counter <= 150: return procedure(matrix,think,3)
    
    # after 150 moves 
#    elif getNextMoves.counter <= 830: return procedure(matrix,think,4)
    else: return procedure(matrix,think,4)
