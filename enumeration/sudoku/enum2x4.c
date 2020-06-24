/*

Following 2x3 code to perform reductions, enumerate 8x8 sudokus with 2x4 blocks.

Factor of 8! for top left block

1 2 3 4 | a b c d
5 6 7 8 | e f g h
--------+--------

Order a,b,c,d columns to 5,6,7,8 (4! reduction)

1 2 3 4 | 5 6 7 8
5 6 7 8 | e f g h
--------+--------
u . . . | . . . .
v . . . | . . . .
--------+--------
w . . . | . . . .
x . . . | . . . .
--------+--------
y . . . | . . . .
z . . . | . . . .

6! orders for u,v,w,x,y,z, but similar reductions reduce by a factor of 2*3!=12
to get u=2, then reduce by 2*2=4 for w<x and y<z, total reduction factor of 48
for each of 15 different cases

constraints: u < w < y (factor 6 reduction)
u < v, w < x, and y < z (factor 8 reduction)

Leaves enumeration of about 600 million solution grids, so using C to program
this one.

Compiled with gcc -O3 and runtime was 8m40s on a i5-2540M
Answer is 29,136,487,207,403,520

*/

#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>

// only need 1 grid, backtracking will clear the grid after each case
uint8_t grid[8][8];
// uint32_t turns out to be enough bits given the knowledge of how many
// solutions will need to be counted with the reductions used
uint32_t count = 0;

// position counts in row major order
void backtrack(uint32_t position)
{
    if (position == 64) // found solution
    {
        ++count;
        return;
    }
    uint32_t row = position >> 3; // divide by 8
    uint32_t col = position & 0x7; // modulus by 8
    if (grid[row][col])
        backtrack(position+1); // cell is filled
    else // empty cell (0 on grid)
    {
        // find possibilities, set [row][col], recurse, backtrack
        uint8_t nums[9] = {1,1,1,1,1,1,1,1,1};
        for (uint32_t i = 0; i < 8; ++i) // same row/col
        {
            nums[grid[row][i]] = 0;
            nums[grid[i][col]] = 0;
        }
        // block top left coordinates
        uint32_t br = row&6, bc = col&4; // bit operation to subtract modulus
        for (uint32_t r = 0; r < 2; ++r)
            for (uint32_t c = 0; c < 4; ++c)
            {
                nums[grid[br+r][bc+c]] = 0;
            }
        for (uint32_t n = 1; n <= 8; ++n) // for each number, set and search
        {
            if (!nums[n]) continue; // impossible number
            grid[row][col] = (uint8_t)(n);
            backtrack(position+1);
        }
        grid[row][col] = 0; // backtrack
    }
}

int main(int argc, char **argv)
{
    // simultaneously zero both grids and set top row in original_grid
    for (uint32_t i = 0; i < 8; ++i)
    {
        for (uint32_t j = 0; j < 8; ++j)
            grid[i][j] = 0;
        grid[0][i] = i+1;
    }
    // complete top left block
    grid[1][0] = 5;
    grid[1][1] = 6;
    grid[1][2] = 7;
    grid[1][3] = 8;
    // next cell in left column (u) is guaranteed to be 2
    grid[2][0] = 2;
    // arrays for remaining numbers and which were used
    uint8_t nums[5] = {3,4,6,7,8};
    uint8_t used[5] = {0,0,0,0,0};
    // 5 nested loops to generate the 15 left column cases
    // the variables indicate an index in the nums array
    uint8_t v,w,x,y,z;
    uint32_t case_num = 0, prev_count = 0;
    for (v = 0; v < 5; ++v)
    {
        // v is the first so it is guaranteed unused
        used[v] = 1;
        grid[3][0] = nums[v];
        for (w = 0; w < 5; ++w)
        {
            if (used[w]) continue;
            used[w] = 1;
            grid[4][0] = nums[w];
            for (x = w+1; x < 5; ++x) // guarantee w < x
            {
                if (used[x]) continue;
                used[x] = 1;
                grid[5][0] = nums[x];
                for (y = w+1; y < 5; ++y) // guarantete w < y
                {
                    if (used[y]) continue;
                    used[y] = 1;
                    grid[6][0] = nums[y];
                    for (z = y+1; z < 5; ++z) // guarantee y < z
                    {
                        if (used[z]) continue;
                        // dont bother marking used[z]
                        grid[7][0] = nums[z];
                        printf("case #%u:\n",++case_num);
                        printf("    u = %u\n",2);
                        printf("    v = %u\n",nums[v]);
                        printf("    w = %u\n",nums[w]);
                        printf("    x = %u\n",nums[x]);
                        printf("    y = %u\n",nums[y]);
                        printf("    z = %u\n",nums[z]);
                        // know which is first empty cell so start there
                        backtrack(12);
                        printf("    solutions = %u\n",count-prev_count);
                        prev_count = count;
                    }
                    used[y] = 0;
                }
                used[x] = 0;
            }
            used[w] = 0;
        }
        used[v] = 0;
    }
    // compute total by considering reductions
    uint64_t total = count;
    total *= 8*7*6*5*4*3*2*1; // top left block
    total *= 4*3*2*1; // top right block
    total *= 6*8; // left column
    printf("total 8x8 sudokus with 2x4 blocks: %lu\n",total);
    return 0;
}

