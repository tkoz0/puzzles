# file to assist in generating heyawake text files
# first, input the rows, cols, and output file name as prompted
# while the main part is running
# q: quit
# u: undo last operation (supports full undo history)
# type "<r> <c> [n]" to make a rxc rectangle with the number n (optional)

import curses

print('rows: ',end='')
R = int(input())
print('cols: ',end='')
C = int(input())
print('outfile: ',end='')
outfile = input()

def get_box_dims(stdscr,y,x):
    s = ''
    while True:
        c = stdscr.getch(y,x)
        if chr(c) == 'q': return ('q','q','q') # termination
        if chr(c) == 'u': return ('u','u','u') # undo last operation
        if chr(c) == '\n': break
        if chr(c) in ' 0123456789': s += chr(c)
    try:
        r,c = map(int,s.split())
        n = -1
    except:
        try: r,c,n = map(int,s.split())
        except: raise Exception()
    assert -1 <= n <= 9 # -1 for unspecified, 0-9 for numbers, no larger appear
    assert r > 0 and c > 0
    return (r,c,n)

def valid_rect(grid,r,c,br,bc): # rectangle fits in blank space available
    global R,C
    if r+br > R or c+bc > C: return False
    for rr in range(r,r+br):
        for cc in range(c,c+bc):
            if grid[rr][cc] != ' ': return False
    return True

def choose_fill(grid,r,c,br,bc): # pick fill char not used by adjacent region
    global R,C
    adj_chars = set()
    if r-1 >= 0:
        for cc in range(c,c+bc): adj_chars.add(grid[r-1][cc])
    if r+br < R:
        for cc in range(c,c+bc): adj_chars.add(grid[r+br][cc])
    if c-1 >= 0:
        for rr in range(r,r+br): adj_chars.add(grid[rr][c-1])
    if c+bc < C:
        for rr in range(r,r+br): adj_chars.add(grid[rr][c+bc])
    for c in '@#$%&*': # try to 4 color, but allow 2 extras just in case
        if not (c in adj_chars): return c
    raise Exception()

def main(stdscr): # wrapper handles initialization

#    stdscr = curses.initscr()
#    curses.noecho()
#    curses.cbreak()
#    stdscr.keypad(True)

    stdscr.clear()
    global R,C,outfile
    
    grid = [list(' '*C) for _ in range(R)]
    nums = [list(' '*C) for _ in range(R)]

    #pr,pc,pbr,pbc = None,None,None,None # prev operation position and size
    undo = [] # undo history
    r,c = 0,0
    while r < R: # entire board
        
        if grid[r][c] == ' ': # find blank space
            try: br,bc,bn = get_box_dims(stdscr,r,c)
            except: continue # try again for this space
            
            if br == 'q': return # end program
            
            if br == 'u': # undo
                if len(undo) > 0: # can undo
                    pr,pc,pbr,pbc = undo.pop()
                    for rr in range(pr,pr+pbr):
                        for cc in range(pc,pc+pbc):
                            grid[rr][cc] = ' '
                            stdscr.addch(rr,cc,' ')
                    nums[pr][pc] = ' '
                    r,c = pr,pc # so next iteration goes to same place
                continue
            
            # try to place rectangle, otherwise retry input
            if valid_rect(grid,r,c,br,bc):
                fillch = choose_fill(grid,r,c,br,bc)
                for rr in range(r,r+br):
                    for cc in range(c,c+bc):
                        grid[rr][cc] = fillch
                        stdscr.addch(rr,cc,fillch)
                nums[r][c] = ' ' if bn == -1 else str(bn)
                stdscr.addch(r,c,nums[r][c])
                undo.append((r,c,br,bc)) # save undo data
                #pr,pc,pbr,pbc = r,c,br,bc # save undo data
            else: continue # fail, try again
        
        c += 1
        if c == C: r,c = r+1,0
     
    # done, write to file
    with open(outfile,"w") as outf:
        for row in grid: outf.write(''.join(row)+'\n')
        outf.write('-'*C+'\n')
        for row in nums: outf.write(''.join(row)+'\n')
        outf.close()

#    curses.nocbreak()
#    stdscr.keypad(False)
#    curses.echo()
#    curses.endwin()

curses.wrapper(main)
