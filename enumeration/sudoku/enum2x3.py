
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

For further analysis, look at the top right block

1 2 3 | a b c
4 5 6 | d e f
------+------
. . . | . . .
. . . | . . .
------+------
. . . | . . .
. . . | . . .

{a,b,c} must have the values {4,5,6} and {d,e,f} must have the values {1,2,3}.
The columns can be reordered so that a = 4, b = 5, and c = 6 which divides the
number of possibilities to search by 6.

Furthermore, the left column can be analyzed to reduce the enumeration problem
even more. The left column will contain {2,3,5,6} in various orders.

1 2 3 | 4 5 6
4 5 6 | d e f
------+------
w . . | . . .
x . . | . . .
------+------
y . . | . . .
z . . | . . .

The bottom 4 rows cannot simply be shuffled because that can mix contents of
blocks and possibly result in duplicate numbers within blocks afterward. What
can be done is swapping rows within the 2nd and 3rd rows of blocks so that the
numbers are reordered with w < x and y < z. This reduces the enumeration problem
by a factor of 4. Furthermore, the bottom 2 rows of blocks can be swapped to
make w < y.

This guarantees that w = 2 is always achieved. Then there are 3 possibilities
for x (3,5,6). y and z take the 2 remaining values such that y < z. This creates
3 possible left columns to search, multiplying each result by 8.

The 3 orders for w,x,y,z to use are:
1. 2,3,5,6
2. 2,5,3,6
3. 2,6,3,5

6x6 puzzles are small so not much optimization is needed for a reasonable time,
but further reductions improve the runtime noticeably.
The solution is 28,200,960

Analysis of run time with further addition of reductions:
Top left block reduction only: ~11 sec on a i5-2540M
Adding top right block reduction: ~1.5 sec on a i5-2540M
Adding left column reduction: ~0.25 sec on a i5-2540M

The runtime reduction factors are pretty close to the reduction factor of the
number of possibilities to count, ~6x for the right block and ~8x for the left
column.

One thing to note is that for each of the 3 cases of left column reduction, a
different number of solutions is counted (328, 168, and 320). If the left
column were reducible to the 1 order to reduce the enumeration problem by a
factor of 24, then the number of solutions counted for any order of the left
column would be the same, however, this is not the case. This shows that having
the 3 distinct left column cases is necessary.

'''

import math

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

# top right block reduction
grid[0][3:6] = [4,5,6] # reshuffle columns to order the top row

# left column reduction
grid[2][0] = 2 # guaranteed 2
# save original before the modifications below
original_grid = [row[:] for row in grid]

# 3 possibilities, hardcoding them because there are so few

# case 1: 2,3 in middle left block
grid[3][0] = 3
grid[4][0] = 5
grid[5][0] = 6
backtrack(0)
print('left column case 1 counted:',count)
prevcount = count

# case 2: 2,5 in middle left block
grid = [row[:] for row in original_grid]
grid[3][0] = 5
grid[4][0] = 3
grid[5][0] = 6
backtrack(0)
print('left column case 2 counted:',count-prevcount)
prevcount = count

# case 3: 2,6 in middle left block
grid = [row[:] for row in original_grid]
grid[3][0] = 6
grid[4][0] = 3
grid[5][0] = 5
backtrack(0)
print('left column case 3 counted:',count-prevcount)

# 6! for top left box, 3! for top right box
# 8 for left column reduction
multiplier = math.factorial(6) * math.factorial(3) * 8

# multiply based on the reductions that were made
print('total 6x6 sudokus with 2x3 blocks:',multiplier*count)
