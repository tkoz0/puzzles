
'''

All solutions can be relabeled to have the top left block look like this
Thus, the number of solutions is 6! times how many solutions this grid has

1 2 3 | . . .
4 5 6 | . . .
------+------
. . . | . . .
. . . | . . .
------+------
. . . | . . .
. . . | . . .

6x6 puzzles are small so not much optimization is needed for a reasonable time
This code runs in ~11 sec on a i5-2540M

'''

# use a 6x6 array for the grid and set the top left box
grid = [[0]*6 for _ in range(6)]
grid[0][0:3] = [1,2,3]
grid[1][0:3] = [4,5,6]

# count number of solutions
count = 0

# i is cell number, corresponding to index (i//6,i%6)
def backtrack(i):
    global count,grid
    if i == 36: # solution found
        count += 1
        return
    R,C = divmod(i,6)
    if grid[R][C] != 0: # skip filled cell
        backtrack(i+1)
        return
    # determine possible values for this cell
    possible = [True]*7
    for i in range(6):
        possible[grid[R][i]] = False
        possible[grid[i][C]] = False
    br,bc = R-(R%2),C-(C%3) # top left position of its block
    for r in range(2):
        for c in range(3):
            possible[grid[br+r][bc+c]] = False
    # for each possible value, set value, recurse, unset value
    for n in range(1,7):
        if not possible[n]: continue
        grid[R][C] = n
        backtrack(i+1)
    grid[R][C] = 0 # can unset at end

# run brute force recursive solver
backtrack(0)

# 6! times amount counted for above grid
print(720*count)
