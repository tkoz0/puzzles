import os,sys,json

# scrypt to convert puzzle data to json
# usage: puzzle_data.py <txt dir> <output dir>

indir = os.path.normpath(sys.argv[1])
outdir = os.path.normpath(sys.argv[2])

def getMultitokenRows(lines,start): # return (row_obj,last_row_index)
    row_obj = []
    row_index = start
    while row_index < len(lines):
        row_tokens = [s.strip() for s in lines[row_index].split()]
        if len(row_tokens) < 2: break
        row_obj.append(row_tokens)
        row_index += 1
    return (row_obj,row_index-1)

allTypes = set()

def makeJson(file):
    global allTypes
    # expected attributes: puzzle,author,solver,source,info,rows,cols,unit,size,
    #                      clabels,rlabels,problem,areas,solution,moves
    J = dict() # for json output
    lines = [line[:-1] for line in open(file,'r')]
    lines = [line for line in lines if line != ''] # exclude empty lines
    if lines == ['$X;']: print('specific skip:',file); return # workaround for 1 bad puzzle
    if lines[0] == 'begin': i = 1
    else: i = 0; print('warning: no begin line in',file)
    if lines[-1] != 'end': print('warning: no end line in',file)
    while i < len(lines):
        tokens = [s.strip() for s in lines[i].split()]
        if tokens[0] == 'puzzle':
            allTypes.add(lines[i][7:])
            J['puzzle'] = lines[i][7:].replace(' ','')
        elif tokens[0] == 'variant': J['variant'] = lines[i][8:] # Araf/Different-Neighbors.txt???
        elif tokens[0] == 'check': J['check'] = lines[i][6:] # Araf/Different-Neighbors.txt???
        elif tokens[0] == 'author': J['author'] = lines[i][7:] # name???
        elif tokens[0] == 'source': J['source'] = lines[i][7:] # url???
        elif tokens[0] == 'rights': J['rights'] = lines[i][7:] # copyright info???
        elif tokens[0] == 'title': J['title'] = lines[i][6:] # Akari/589.a.txt???
        elif tokens[0] == 'solver': J['solver'] = lines[i][7:] # name???
        elif tokens[0] == 'info': J['info'] = lines[i][5:] # string???
        elif tokens[0] == 'pid': J['pid'] = lines[i][4:] # Aisuban/044.a.txt???
        elif tokens[0] == 'rows': J['rows'] = int(lines[i][5:])
        elif tokens[0] == 'cols': J['cols'] = int(lines[i][5:])
        elif tokens[0] == 'unit': J['unit'] = int(lines[i][5:])
        elif tokens[0] == 'size': J['size'] = int(lines[i][5:])
        elif tokens[0] == 'depth': J['depth'] = int(lines[i][6:]) # ABC-End-View???
        elif tokens[0] == 'unitsize': J['unitsize'] = int(lines[i][9:]) # Abc-Kombi???
        elif tokens[0] == 'options': J['options'] = lines[i][8:] # ABC-End-View???
        elif tokens[0] == 'diagonals': J['diagonals'] = lines[i][10:] # ABC-End-View???
        elif tokens[0] == 'clabels':
            J['clabels'],i = getMultitokenRows(lines,i+1)
        elif tokens[0] == 'rlabels':
            J['rlabels'],i = getMultitokenRows(lines,i+1)
        elif tokens[0] == 'problem':
            J['problem'],i = getMultitokenRows(lines,i+1)
        elif tokens[0] == 'areas':
            J['areas'],i = getMultitokenRows(lines,i+1)
        elif tokens[0] == 'solution':
            J['solution'],i = getMultitokenRows(lines,i+1)
        elif tokens[0] == 'lines':
            J['lines'],i = getMultitokenRows(lines,i+1)
        elif tokens[0] == 'moves':
            J['moves'] = ''
            j = i+1
            while j < len(lines):
                if ';' not in lines[j]: break
                J['moves'] += lines[j]
                j += 1
            i = j-1
        elif tokens[0] == 'celltext': # Araf specific?
            J['celltext'] = ''
            j = i+1
            while j < len(lines):
                if ';' not in lines[j]: break
                J['celltext'] += lines[j]
                j += 1
            i = j-1
        elif tokens[0] == 'ships': # Battlemines specific?
            J['ships'] = list(map(int,tokens[1:]))
        elif tokens[0] == 'begin': pass # also ignore, multipuzzle issue in Araf puzzles
        elif tokens[0] == 'end': pass # ignore it, issue in Aisuban/037.a.txt
            #assert i == len(lines)-1, file
            #break # should be the end
        else: assert 0, 'unknown attribute '+tokens[0]+' in file '+file
        i += 1
    return J

# relpath excludes indir path
# this is to determine path in the output dir

def processFile(file,relpath):
    global outdir
    J = makeJson(file)
    return None
    name,ext = os.path.splitext(relpath)
    outfile = open(outdir+name+'.json','w')
    outfile.write(json.dumps(J))
    outfile.write('\n')
    outfile.close()
    print('wrote:',outdir+name+'.json')

def recursiveExplore(file,relpath):
    global outdir
    _,ext = os.path.splitext(file)
    if os.path.isfile(file): processFile(file,relpath)
    elif os.path.isdir(file):
        try: os.mkdir(outdir+relpath)
        except FileExistsError: print('dir exists:',file)
        for dirfile in sorted(os.listdir(file)):
            recursiveExplore(file+'/'+dirfile,relpath+'/'+dirfile)

assert os.path.isdir(indir)
recursiveExplore(indir,'')
print(allTypes)
