def transpose(grid):
    return tuple(zip(*grid))

def reverse(grid):
    return tuple(row[::-1] for row in grid)

def shift_row_left(row):
    tmp = [tile for tile in row if tile]
    return tuple(tmp) + (0,) * (len(row) - len(tmp))

def merge_row_left(row):
    tmp = [tile for tile in row if tile]

    i = 0
    while i < len(tmp)-1:
        if tmp[i] == tmp[i+1]:
            tmp[i] *= 2
            del tmp[i+1]
        i += 1

    return tuple(tmp) + (0,) * (len(row) - len(tmp))

def merge_left(grid):
    return tuple(merge_row_left(row) for row in grid)

def merge_right(grid):
    return reverse(merge_left(reverse(grid)))

def merge_up(grid):
    return transpose(merge_left(transpose(grid)))

def merge_down(grid):
    return merge_up(grid[::-1])[::-1]

if __name__=='__main__':

    grid = (( 0, 0, 2, 2)
           ,( 0, 2, 4, 2)
           ,( 8, 4, 2, 2)
           ,(16,16, 8, 8))

    for row in grid:
        print row
    print

    for row in merge_left(grid):
        print row
    print

    for row in merge_right(grid):
        print row
    print

    for row in merge_up(grid):
        print row
    print

    for row in merge_down(grid):
        print row
    print
