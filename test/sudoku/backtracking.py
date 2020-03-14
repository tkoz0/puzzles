import sys

# i5-2540M benchmark, 1000000 puzzles, 756 seconds

solution = None
# grid is a 9x9 list of integers 0-9
# pos is 0-81, indicating position grid[pos//9][pos%9]
# function assumes that the clues do not violate sudoku constraints
def solve(grid,pos):
    global solution
    r,c = divmod(pos,9)
    if pos == 81: # completed grid
        solution = grid
        return True
    elif grid[r][c] == 0: # empty cell, try possible numbers
        br,bc = (r//3)*3,(c//3)*3
        nums = [True]*10 # possible numbers
        for n in grid[r]: nums[n] = False # row
        for rr in range(9): nums[grid[rr][c]] = False # column
        for rr in range(br,br+3): # block
            for cc in range(bc,bc+3):
                nums[grid[rr][cc]] = False
        for n in range(1,10): # recurse for each possible number
            if not nums[n]: continue
            grid[r][c] = n
            if solve(grid,pos+1): return True # propagate true up the stack
        grid[r][c] = 0
        return False # no solution
    else: return solve(grid,pos+1) # skip filled cell

# skip first line (containin headers)
# all other lines are the puzzle and solution separated by comma
# they are formatted as a 81 char string of digits

i = -1
for line in sys.stdin:
    i += 1
    if i == 0: continue # skip header line
    init,soln = [s.strip() for s in line.split(',')]
    solution = None
    assert len(init) == 81 and len(soln) == 81
    rows = [init[i:i+9] for i in range(0,81,9)]
    grid = [list(map(int,list(row))) for row in rows]
    if solve(grid,0):
        assert solution
        rows = [''.join(map(str,row)) for row in solution]
        solution = ''.join(rows)
        if solution == soln:
            print('puzzle %d success'%i)
        else:
            print('puzzle %d failure'%i)
    else:
        print('puzzle %d no solution'%i)
