import os,sys,hashlib

# command enumeration
FILE = 0
MD5SUMS = 1
ADD_BEG = 2
ADD_END = 3
EDIT = 4
INSERT = 5
DELETE = 6
END = 7

datadir = 'puzzle_data'

def commandsGenerator(file):
    line_num = 0 # 1-indexed line numbers
    for line in open(file,'r'):
        line_num += 1
        line = line.strip()
        if line == '' or line.startswith('#'): continue # comment/whitespace
        terms = line.split()
        if terms[0] == 'file': yield (FILE,terms[1]) # assume no spaces
        elif terms[0] == 'md5sums': yield (MD5SUMS,terms[1],terms[2])
        elif terms[0] == 'add_begin_line': yield (ADD_BEG,)
        elif terms[0] == 'add_end_line': yield (ADD_END,)
        elif terms[0] == 'edit_line':
            yield (EDIT,int(terms[1]),' '.join(terms[2:]))
        elif terms[0] == 'insert_line':
            yield (INSERT,int(terms[1]),' '.join(terms[2:]))
        elif terms[0] == 'delete_line':
            indexes = []
            if ',' in terms[1]:
                iterms = terms[1].split(',')
                for iterm in iterms:
                    if ('-' in iterm) and iterm[0] != '-': # range
                        itermsplit = iterm.split('-')
                        a,b = map(int,itermsplit)
                        assert a <= b
                        indexes += list(range(a,b+1))
                    else: indexes.append(int(iterm))
            elif ('-' in terms[1]) and terms[1][0] != '-': # range
                itermsplit = terms[1].split('-')
                a,b = map(int,itermsplit)
                assert a <= b
                indexes += list(range(a,b+1))
            else: indexes.append(int(terms[1]))
            yield (DELETE,set(indexes))
        else:
            assert terms[0] == 'end'
            yield (END,)

# information about current file
current_file = None
file_data = None
lines = None
md5old = None
md5new = None
wait_for_end = False # wait for this line for skipped files

# if no file is opened, ignore commands
def runCommand(command):
    global current_file,file_data,lines,md5old,md5new,wait_for_end
    assert type(command) == tuple
    if wait_for_end:
        if command[0] == END: wait_for_end = False
        return
    wait_for_end = False
    if command[0] == FILE: # load file
        print('loading file:',command[1])
        current_file = command[1]
        if os.path.isfile(datadir+'/'+current_file+'.old'): # already edited
            print('skipping, already edited')
            wait_for_end = True
            return
        lines = open(datadir+'/'+current_file,'r').read().splitlines()
        file_data = open(datadir+'/'+current_file,'rb').read()
    elif command[0] == MD5SUMS: # verify old md5sum
        md5old, md5new = command[1], command[2]
        assert hashlib.md5(file_data).hexdigest() == md5old
    elif command[0] == ADD_BEG: lines.insert(0,'begin')
    elif command[0] == ADD_END: lines.append('end')
    elif command[0] == EDIT:
        index, content = command[1], command[2]
        lines[index] = content
    elif command[0] == INSERT:
        index, content = command[1], command[2]
        lines.insert(index,content)
    elif command[0] == DELETE:
        indexes = set(i if i >= 0 else len(lines)+i for i in command[1])
        newlines = []
        for i,line in enumerate(lines):
            if i not in indexes: newlines.append(line)
        lines = newlines
    elif command[0] == END: # verify new md5sum
        output_data = ''
        for line in lines: output_data += line + '\n'
        assert hashlib.md5(output_data.encode()).hexdigest() == md5new
        os.rename(datadir+'/'+current_file,datadir+'/'+current_file+'.old')
        outfile = open(datadir+'/'+current_file,'w')
        outfile.write(output_data)
        outfile.close()
        # reset
        current_file = None
        file_data = None
        lines = None
        md5old = None
        md5new = None
        print('changes saved')

def hardCodedSpecial(): # special cases that dont fit the commands above
    # Yajisan-Kazusan 2 puzzles in 1 file
    yk_l = datadir+'/Yajisan-Kazusan/Liar.txt'
    print('loading file:',yk_l)
    if os.path.isfile(datadir+'/Yajisan-Kazusan/Liar.1.txt'):
        print('skipping, already edited')
    else:
        assert hashlib.md5(open(yk_l,'rb').read()).hexdigest() == 'b3a4edbdc16be77966de7b152da01ae8'
        lines = open(yk_l,'r').read().splitlines()
        assert lines[3] == lines[39] == 'begin'
        assert lines[37] == lines[52] == 'end'
        lines1 = lines[3:38]
        lines2 = lines[39:53]
        output1 = ''
        output2 = ''
        for line in lines1: output1 += line + '\n'
        for line in lines2: output2 += line + '\n'
        assert hashlib.md5(output1.encode()).hexdigest() == '2b33c2bf360c532b423003aff0b0c02c'
        assert hashlib.md5(output2.encode()).hexdigest() == '43b73d21e0469bcbfe7515d58bf3e1e3'
        os.rename(yk_l,yk_l+'.old')
        outfile1 = open(datadir+'/Yajisan-Kazusan/Liar.1.txt','w')
        outfile2 = open(datadir+'/Yajisan-Kazusan/Liar.2.txt','w')
        outfile1.write(output1)
        outfile2.write(output2)
        outfile1.close()
        outfile2.close()
        print('changes saved')
    # Wolkenkratzer 2 puzzles in 1 file
    wk410 = datadir+'/Wolkenkratzer/410.a.txt'
    # for now, just removing the malformed puzzle (incomplete solution)
    # this is done in puzzle_fixes.txt

if __name__ == '__main__':
    for command in commandsGenerator(sys.argv[1]): runCommand(command)
    hardCodedSpecial()

