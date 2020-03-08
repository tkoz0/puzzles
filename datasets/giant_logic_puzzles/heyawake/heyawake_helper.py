# file to assist in generating heyawake text files
# while the main part is running
# q: quit
# u: undo last operation (supports full undo history)
# w: write to file when finished
# type "<r> <c> [n]" to make a rxc rectangle with the number n (optional)
# command line usage: heyawake_helper <r> <c> <file>

import curses
import sys

R = int(sys.argv[1])
C = int(sys.argv[2])
outfile = sys.argv[3]

def get_box_dims(stdscr,y,x):
    s = ''
    while True:
        c = stdscr.getch(y,x)
        if chr(c) == 'q': return ('q','q','q') # termination
        if chr(c) == 'u': return ('u','u','u') # undo last operation
        if chr(c) == 'w': return ('w','w','w') # write to file (when done)
        if chr(c) == '\n': break
        if chr(c) in ' 0123456789': s += chr(c)
    try:
        r,c = map(int,s.split())
        n = -1
    except:
        try: r,c,n = map(int,s.split())
        except: raise Exception()
    assert -1 <= n <= 9 # -1 for unspecified, 0-9 for numbers
    # does not support larger numbers, special cases were handled separately
    # the only exceptions were 11 and 12 (B and C) in the last puzzle
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
#    stdscr.start_color()

    stdscr.clear()
    
    # create color pairs to use
    curses.init_pair(10,curses.COLOR_BLACK,curses.COLOR_WHITE)
    curses.init_pair(1,curses.COLOR_BLACK,curses.COLOR_YELLOW)
    curses.init_pair(2,curses.COLOR_BLACK,curses.COLOR_CYAN)
    curses.init_pair(3,curses.COLOR_BLACK,curses.COLOR_MAGENTA)
    curses.init_pair(4,curses.COLOR_BLACK,curses.COLOR_GREEN)
    curses.init_pair(5,curses.COLOR_BLACK,curses.COLOR_BLUE)
    curses.init_pair(6,curses.COLOR_BLACK,curses.COLOR_RED)
    charcolor = {'@':1,'#':2,'$':3,'%':4,'&':5,'*':6}
    
    global R,C,outfile
    
    # make white background
    for r in range(R): stdscr.addstr(r,0,' '*C,curses.color_pair(10))
    stdscr.refresh()
    
    grid = [list(' '*C) for _ in range(R)]
    nums = [list(' '*C) for _ in range(R)]

    #pr,pc,pbr,pbc = None,None,None,None # prev operation position and size
    undo = [] # undo history
    r,c = 0,0
    while True: # entire board
        
        if r == R: # check for undo only, otherwise complete board
            try: br,bc,bn = get_box_dims(stdscr,r,c)
            except: continue
            if br == 'u': # undo
                if len(undo) > 0: # can undo
                    pr,pc,pbr,pbc = undo.pop()
                    for rr in range(pr,pr+pbr):
                        for cc in range(pc,pc+pbc):
                            grid[rr][cc] = ' '
                            stdscr.addstr(rr,cc,' ',curses.color_pair(10))
                    nums[pr][pc] = ' '
                    r,c = pr,pc # so next iteration goes to same place
                continue
            if br == 'q': return # quit
            if br == 'w': break # go on, write to file
            continue # try again
        
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
                            stdscr.addstr(rr,cc,' ',curses.color_pair(10))
                    nums[pr][pc] = ' '
                    r,c = pr,pc # so next iteration goes to same place
                continue
            
            if br == 'w': continue # only allow write command at end
            
            # try to place rectangle, otherwise retry input
            if valid_rect(grid,r,c,br,bc):
                fc = choose_fill(grid,r,c,br,bc) # fill character
                for rr in range(r,r+br):
                    for cc in range(c,c+bc):
                        grid[rr][cc] = fc
                        stdscr.addstr(rr,cc,' ',curses.color_pair(charcolor[fc]))
                nums[r][c] = ' ' if bn == -1 else str(bn)
                stdscr.addstr(r,c,' ' if bn == -1 else str(bn),
                             curses.color_pair(charcolor[fc]))
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
