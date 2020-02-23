
import sys
from functools import reduce

R, C = int(sys.argv[1]), int(sys.argv[2])
N = R*C # grid size
grid = []
for _ in range(R*C):
    grid.append(list(map(int,input().split()))) # read row of integers
    assert len(grid[-1]) == R*C # proper length, all in [0,R*C] range
    assert reduce(lambda x,y : x and y, [0 <= z <= R*C for z in grid[-1]])
solution = []

def solver(grid,pos):
    if pos == N*N:
        global solution
        solution = grid
        return True
    r = pos//N # cell coordinates
    c = pos%N
    if grid[r][c]: return solver(grid,pos+1)
    br = r//R # block coordinates
    bc = c//C
    allowed = [True]*(1+N)
    for cc in range(N): # eliminate row numbers
        allowed[grid[r][cc]] = False
    for rr in range(N): # eliminate column numbers
        allowed[grid[rr][c]] = False
    for rr in range(R*br,R*br+R):
        for cc in range(C*bc,C*bc+C):
            allowed[grid[rr][cc]] = False
    for n in range(1,1+N): # guess each
        if not allowed[n]: continue
        grid[r][c] = n
        if solver(grid,pos+1): return True
    grid[r][c] = 0 # backtrack
    return False

def checker(grid):
    nums = set(range(1,1+N))
    for row in grid: assert set(row) == nums
    for c in range(N): assert set(grid[r][c] for r in range(N)) == nums
    for br in range(C):
        for bc in range(R):
            assert set(sum([grid[r][bc*C:bc*C+C]
                            for r in range(br*R,br*R+R)],[])) == nums

if solver(grid,0):
    checker(grid)
    for row in solution: print(row)
