######## OLD CODE ###########

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

def addBeginLine(file):
    if os.path.isfile(file+'.old'): return # already done
    lines = getLines(file)
    assert lines[0] != 'beg\n'
    lines.insert(0,'begin\n')
    writeLines(file,lines)

def addEndLine(file):
    if os.path.isfile(file+'.old'): return # already done
    lines = getLines(file)
    assert lines[-1] != 'end\n'
    lines.append('end\n')
    writeLines(file,lines)

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
    addBeginLine(path+'/068.a.txt')
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
    addEndLine(path+'/232.a.txt')
    file1 = path+'/080.a.txt'
    if not os.path.isfile(file1+'.old'):
        lines = getLines(file1)
        assert lines[30] == lines[31] == 'moves\n'
        lines.pop(30)
        writeLines(file1,lines)
    file2 = path+'/741.a.txt'
    if not os.path.isfile(file2+'.old'): # moves property repeated
        lines = getLines(file2)
        assert lines[-10] == 'moves\n' and (';' in lines[-2])
        lines[-10:-1] = []
        writeLines(file2,lines)

def fixZeltlager2(path):
    addBeginLine(path+'/321.a.txt')

def fixZahlenlabyrinth(path):
    file1 = path+'/001.a.txt'
    if not os.path.isfile(file1+'.old'):
        lines = getLines(file1)
        assert lines[10] == '- - - - -\n' == lines[15]
        assert lines[14] == '- - 3 - -\n' == lines[19]
        lines[15:20] = [] # remove duplicated board
        assert lines[16] == '5 6 7 8 9\n' == lines[21]
        assert lines[20] == '25 22 21 14 13\n' == lines[25]
        lines[21:26] = []
        assert lines[22] == '- 3 - 1 2\n' == lines[27]
        assert lines[26] == '- 1 3 2 -\n' == lines[31]
        lines[27:32] = []
        writeLines(file1,lines)

def fixZehnergitter(path):
    file1 = path+'/330.a.txt'
    if not os.path.isfile(file1+'.old'): # weird repetition
        lines = getLines(file1)
        assert lines[1] == 'puzzle tenner\n'
        assert lines[8] == '- 0 - 8 - - - - 3 - begin\n'
        lines[1:9] = []
        writeLines(file1,lines)

def fixSlitherlink(path):
    file1 = path+'/0032.a.txt'
    if not os.path.isfile(file1+'.old'): # repeated solver line
        lines = getLines(file1)
        assert lines[2].startswith('solver') and lines[3].startswith('solver')
        lines.pop(2)
        writeLines(file1,lines)

def fixUsoone(path):
    file1 = path+'/051.a.txt'
    if not os.path.isfile(file1+'.old'): # weird repetition
        lines = getLines(file1)
        assert lines[1] == 'puzzle usoone\n'
        assert lines[8] == 'problembegin\n'
        lines[1:9] = []
        writeLines(file1,lines)

def fixView(path):
    doublesource = [path+'/%03d.a.txt'%d for d in [1,2,3,4]]
    for file in doublesource:
        if not os.path.isfile(file+'.old'):
            lines = getLines(file)
            assert lines[3].startswith('source')
            assert lines[4].startswith('source')
            lines.pop(3)
            writeLines(file,lines)

def fixSuguru(path):
    doublesolver8 = [path+'/%03d.a.txt'%d for d in
        [3,4,5,6,8,9,10,15,18,19,20]]
    for file in doublesolver8: # line 8 repeated solver
        if not os.path.isfile(file+'.old'):
            lines = getLines(file)
            if file == path+'/003.a.txt': # special case
                assert lines[-1] == 'eend\n'
                lines[-1] = 'end\n'
            assert lines[8] == 'solver Otto Janko\n'
            lines.pop(8)
            writeLines(file,lines)

def fixSuraromu(path):
    file1 = path+'/080.a.txt'
    if not os.path.isfile(file1+'.old'): # double depth line
        lines = getLines(file1)
        assert lines[8].startswith('depth') and lines[9].startswith('depth')
        lines.pop(9)
        writeLines(file1,lines)

funcs = {'Heyawake':fixHeyawake,
         'Fillomino':fixFillomino,
         'LITS':fixLITS,
         'Nurikabe':fixNurikabe,
         'Zeltlager-2':fixZeltlager2,
         'Zahlenlabyrinth':fixZahlenlabyrinth,
         'Zehnergitter':fixZehnergitter,
         'Slitherlink':fixSlitherlink,
         'Usoone':fixUsoone,
         'View':fixView,
         'Suguru':fixSuguru,
         'Suraromu':fixSuraromu}

if __name__ == '__main__':
    puzzle = sys.argv[1]
    funcs[puzzle]('puzzle_data/'+puzzle)
