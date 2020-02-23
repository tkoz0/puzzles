
# expanded a bit for readability

if 0:
    def s(B,P):
        # base case
        if P == 81: return B
        # skip zeroes
        if B[P//9][P%9] != '0': return s(B,P+1)
        # digits that are allowed in this cell (P//9,P%9)
        # take digits 1-9, exclude row, column, and box
        allowed = set(list('123456789'))-(set(B[P//9])|set(B[r][P%9]for r in range(9))|set(B[r][c]for(r,c)in[(P//9//3*3+z//3,P%9//3*3+z%3)for z in range(9)]))
        # get results from all recursive calls
        solutions = [s([[n if r==P//9 and c==P%9 else B[r][c]for c in range(9)]for r in range(9)],P+1)for n in allowed]
        # sudoku board when solved, otherwise empty list
        return list(map(lambda x:x[0]if len(x)else[],[[z for z in solutions if z!=[]]]))[0]
    inpuzzle = [input().split() for _ in range(9)]
    print('\n'.join(' '.join(map(str,r))for r in s(inpuzzle,0)))

# condensed into the 1 liner

def s(B,P):return B if P==81 else s(B,P+1)if B[P//9][P%9]!='0'else list(map(lambda x:x[0]if len(x)else[],[[z for z in[s([[n if r==P//9 and c==P%9 else B[r][c]for c in range(9)]for r in range(9)],P+1)for n in set(list('123456789'))-(set(B[P//9])|set(B[r][P%9]for r in range(9))|set(B[r][c]for(r,c)in[(P//9//3*3+z//3,P%9//3*3+z%3)for z in range(9)]))]if z!=[]]]))[0]
print('\n'.join(' '.join(map(str,r))for r in s([input().split() for _ in range(9)],0)))

# test with project euler
if 0:
    import sys
    for line in sys.stdin:
        board = [list(input()) for _ in range(9)]
        print('puzzle')
        print('\n'.join(str(list(map(int,l))) for l in s(board,0)))
