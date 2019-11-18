import random

# sudoku generator, uses a random row that gets shifted to generate a solved
# puzzle, then to eliminate the pattern, rows and columns are shuffled

# method is taken from this page
# https://gamedev.stackexchange.com/questions/56149/how-can-i-generate-sudoku-puzzles

def check_solved(grid,r,c): # r,c are sub block dimensions
    n = r*c
    nums = set(range(1,1+n))
    for rr in range(n): # each row contains all numbers
        assert set(grid[rr]) == nums
    for cc in range(n): # each column contains all numbers
        assert set(grid[rr][cc] for rr in range(n)) == nums
    for rr in range(c):
        for cc in range(r): # each sub block contains all numbers
#            print([grid[rrr][cc*c:cc*c+c] for rrr in range(rr*r,rr*r+r)])
            assert set(sum( [grid[rrr][cc*c:cc*c+c]
                             for rrr in range(rr*r,rr*r+r)],[])) == nums

def transpose(grid):
    n = len(grid)
    return [[grid[c][r] for c in range(n)] for r in range(n)]

# shift array
def shift(arr,amt):
    amt %= len(arr)
    return arr[amt:] + arr[:amt]

def make3x3():
    grid = [list(range(1,1+9))]
    random.shuffle(grid[0])
    for shamt in [3,3,1,3,3,1,3,3]: # shift amounts to generate solved grid
        grid.append(shift(grid[-1],shamt))
    check_solved(grid,3,3)
    for _ in range(3): # shuffle rows and columns 3 times
        for r in range(3): # shuffle rows
            tmp = grid[r*3:r*3+3]
            random.shuffle(tmp)
            grid[r*3:r*3+3] = tmp
        grid = transpose(grid)
        for c in range(3): # shuffle columns (rows in transposed grid)
            tmp = grid[c*3:c*3+3]
            random.shuffle(tmp)
            grid[c*3:c*3+3] = tmp
        grid = transpose(grid)
    check_solved(grid,3,3)
    return grid

def make_sudoku(R,C): # generalized from the function above
    N = R*C
    grid = [list(range(1,1+N))]
    random.shuffle(grid[0])
#    print([C]*(R-1)+([1]+[C]*(R-1))*(C-1))
    for shamt in [C]*(R-1)+([1]+[C]*(R-1))*(C-1):
        grid.append(shift(grid[-1],shamt))
#    for line in grid: print(line)
    check_solved(grid,R,C)
    for _ in range(max(R,C)): # shuffle rows and columns 3 times
        for r in range(R): # shuffle rows
            tmp = grid[r*R:r*R+R]
            random.shuffle(tmp)
            grid[r*R:r*R+R] = tmp
        grid = transpose(grid)
        for c in range(C): # shuffle columns (rows in transposed grid)
            tmp = grid[c*C:c*C+C]
            random.shuffle(tmp)
            grid[c*C:c*C+C] = tmp
        grid = transpose(grid)
    check_solved(grid,R,C)
    return grid

#for line in make3x3(): print(line)
import sys
for line in make_sudoku(int(sys.argv[1]),int(sys.argv[2])): print(line)
