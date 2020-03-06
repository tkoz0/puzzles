# a 1 line python function that can solve standard sudoku puzzles
# written while i was bored in class one day

# expanded 1 line function for readability
# B = 9x9 list (the board) and P = position counting in row major order
# position P represents B[P//9][P%9]
def s(B,P):
    # P=81 indicates the end
    return ( B if P == 81 else
    # nonzero cell is filled so skip it
    s(B,P+1) if B[P//9][P%9] != '0' else
    # construct a list of solutions computed recursively
    list(
        # consider all possible numbers that can go in the current cell
        # generate a list of all the solution results that are nonempty
        # map is to: keep first solution if its nonempty, else keep empty list
        map(lambda x : x[0] if len(x) else [],
             # single element list containing the solutions list
             [
               # solution for a value of n (z = a solution found recursively)
               [z for z in
                 # list of solutions for all possible numbers in current cell
                 [s( # copy board except insert n for current cell
                     [ [n if r==P//9 and c==P%9 else B[r][c] for c in range(9)]
                       for r in range(9)], P+1
                   )
                  # possible values of n
                  for n in set(list('123456789'))
                    # values to exclude
                    -(  # row
                        set(B[P//9])
                        # column
                      | set(B[r][P%9] for r in range(9))
                        # block
                      | set(B[r][c] for (r,c) in
                            [(P//9//3*3+z//3,P%9//3*3+z%3) for z in range(9)])
                     )
                 ]
                 # exclude solution results that are empty
                 if z != []
               ]
             ]
           
           )
        # pick first solution if one was found, otherwise it will be []
        )[0])


# 1 line to solve standard sudoku
def s(B,P):return B if P==81 else s(B,P+1)if B[P//9][P%9]!='0'else list(map(lambda x:x[0]if len(x)else[],[[z for z in[s([[n if r==P//9 and c==P%9 else B[r][c]for c in range(9)]for r in range(9)],P+1)for n in set(list('123456789'))-(set(B[P//9])|set(B[r][P%9]for r in range(9))|set(B[r][c]for(r,c)in[(P//9//3*3+z//3,P%9//3*3+z%3)for z in range(9)]))]if z!=[]]]))[0]

# solve a puzzle from stdin
print('\n'.join(' '.join(map(str,r))for r in s([input().split() for _ in range(9)],0)))
