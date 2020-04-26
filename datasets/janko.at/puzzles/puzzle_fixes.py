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

def fixHeyawake(path):
    file1 = path+'/576.a.txt'
    if not os.path.isfile(file1+'.old'):
        lines = getLines(file1)
        assert lines[-1] == 'send\n'
        lines[-1] = 'end\n' # fix from 'send' to 'end'
        writeLines(file1,lines)
        print('fixed',file1)

funcs = {'Heyawake':fixHeyawake}

if __name__ == '__main__':
    indir = os.path.normpath(sys.argv[1])
    puzzle = os.path.normpath(sys.argv[2])
    funcs[puzzle](indir)
