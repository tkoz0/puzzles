import os,sys

# scrypt to fix data issues in the puzzles that prevent proper parsing

# scrypt to extract puzzle data from a downloaded copy of janko.at
# usage: puzzle_data.py <Raetsel dir> <output dir>

# note: for this file, lines should always be terminated with '\n'
# hashes are used so file is not modified a 2nd time
# check for a file of the same name + '.old' to check if it was modified already
# writeLines() handles renaming the original file with the '.old'

def getLines(file): return [line for line in open(file,'r')]
def writeLines(file,lines):
    os.rename(file,file+'.old')
    outf = open(file,'w')
    for line in lines: outf.write(line)
    outf.close()
    print('fixed',file)

def fixHeyawake(path):
    file1 = path+'/576.a.txt'
    if not os.path.isfile(file1+'.old'):
        lines = getLines(file1)
        assert lines[-1] == 'send\n'
        lines[-1] = 'end\n' # fix from 'send' to 'end'
        writeLines(file1,lines)

def fixFillomino(path):
    file1 = path+'/020.a.txt'
    if not os.path.isfile(file1+'.old'):
        lines = getLines(file1)
        i = 0
        for j in range(len(lines)): # remove a single line causing issues
            if lines[j].startswith('m0'):
                i = j
                break
        lines.pop(i)
        writeLines(file1,lines)

def fixLITS(path):
    file1 = path+'/068.a.txt'
    if not os.path.isfile(file1+'.old'):
        lines = getLines(file1)
        lines.insert(0,'begin\n') # missing begin line
        writeLines(file1,lines)
    # files with the "areas" line repeated
    doublearea = [path+('/%d.a.txt'%p) for p in
        [281,282,284,285,286,287,288,289,290] ]
    for file in doublearea:
        if not os.path.isfile(file+'.old'):
            lines = getLines(file)
            assert lines[8] == 'areas\n' and lines[9] == 'areas\n'
            lines.pop(8)
            writeLines(file,lines)

def fixNurikabe(path):
    noend = [path+('/%d.a.txt'%p) for p in
        [232] ]
    for file in noend:
        if not os.path.isfile(file+'.old'):
            lines = getLines(file)
            assert lines[-1] != 'end\n'
            lines.append('end\n')
            writeLines(file,lines)

funcs = {'Heyawake':fixHeyawake,
         'Fillomino':fixFillomino,
         'LITS':fixLITS,
         'Nurikabe':fixNurikabe}

if __name__ == '__main__':
    puzzle = sys.argv[1]
    funcs[puzzle]('puzzle_data/'+puzzle)
