
'''

Program to count the number of bands (top 3 rows) of a standard sudoku. The
search is optimized by fixing the numbers in the left block and reordering the
columns of the other 2 blocks as described below:

1 2 3 | a b c | d e f
4 5 6 | . . . | . . .
7 8 9 | . . . | . . .

Reorder columns so that a<b<c and d<e<f which results in a (3!)^2 reduction.
Then swap the 2 blocks to ensure a<d which is a reduction by a factor of 2. For
the remaining cases (10 of them), multiply the number of solutions by 72.

Note that a=4 is always guaranteed with this column reordering.

'''

grid = [[0]*9 for _ in range(3)]

# fix left block
grid[0][:3] = [1,2,3]
grid[1][:3] = [4,5,6]
grid[2][:3] = [7,8,9]

count,prevcount = 0,0

# i=0..5 for 2nd row, i=6..11 for 3rd row
def backtrack_count(i):
    global count,grid
    if i == 12: count += 1 # completed grid for a solution
    else:
        R,C = 1+i//6,3+i%6
        possible = [True]*10
        for c in range(C): # eliminate current row
            possible[grid[R][c]] = False
        # eliminate 3 in the top row that are in the same box
        if C < 6:
            possible[grid[0][3]] = False
            possible[grid[0][4]] = False
            possible[grid[0][5]] = False
        else:
            possible[grid[0][6]] = False
            possible[grid[0][7]] = False
            possible[grid[0][8]] = False
        # do the same for the 2nd row if R == 2
        if R == 2:
            if C < 6:
                possible[grid[1][3]] = False
                possible[grid[1][4]] = False
                possible[grid[1][5]] = False
            else:
                possible[grid[1][6]] = False
                possible[grid[1][7]] = False
                possible[grid[1][8]] = False
        # try all possibilities
        for n in [z for z in range(1,10) if possible[z]]:
            grid[R][C] = n
            backtrack_count(i+1)
        grid[R][C] = 0 # backtrack

# outer double loop picks values for b and c
for b in range(5,10):
    for c in range(b+1,10):
        d,e,f = sorted(set([5,6,7,8,9])-set([b,c]))
        grid[0][3:] = [4,b,c,d,e,f]
        print('toprow case: 4 %d %d | %d %d %d'%(b,c,d,e,f))
        backtrack_count(0)
        print('    counted:',count-prevcount)
        prevcount = count

print('total top bands with fixed left block:',72*count)
