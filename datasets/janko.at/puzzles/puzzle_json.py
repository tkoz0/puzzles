import json,sys,os

# puzzles from janko.at look something like:

# begin
# puzzle sudoku
# size 9
# problem
# - - 1 - - 2 - - 3
# ...

# this scrypt is for converting the files into easier to work with json files
# further postprocessing may be needed such as converting grid values to
# integers or standardizing the value names used to represent grid size
# this scrypt also provides no guarantee that the puzzles are valid (solvable
# with only 1 solution), it only (attempts to) convert to a convenient format
# the intention is to turn the data into json so that the postprocessing and
# puzzle correctness verification can be done more easily

# usage: puzzle_json.py <puzzle subdir>

# enumeration of value types
STRING = 0 # <prop> <value>
INTEGER = 1
FLOAT = 2
# grid
# 1,1 1,2 ...
# 2,1 2,2 ...
# ...
GRID = 10
MULTISTRING = 11
EMPTY = 100 # property as just the property name

class UnknownProp(Exception):
    def __init__(self,msg=''):
        super().__init__(msg)

class ParseGridError(Exception):
    def __init__(self,msg=''):
        super().__init__(msg)

class ParseError(Exception):
    def __init__(self,msg=''):
        super().__init__(msg)

# lines: array of strings
# i: line index where the property name string occurs
# type: from the enumeration above
# settings: additional parameters to read a value
# props: dict containing the values parsed so far
# not all exceptions may be handled properly
def parseValue(lines,i,valuetype,settings,props):
    if valuetype < 10: # value on same line, use right function to parse it
        typefunc = [str,int,float][valuetype]
        try: return (i+1,typefunc(lines[i][lines[i].find(' ')+1:].strip()))
        except Exception as ex: raise ParseError(typefunc.__name__)
    elif valuetype == GRID: # read following lines as a grid with ' ' separators
        rows,cols = settings
        if type(rows) == str: rows = props[rows]
        if type(cols) == str: cols = props[cols]
        assert type(rows) == int and type(cols) == int
        if rows <= 0 or cols <= 0: raise ParseGridError('rows<=0 or cols<=0')
        try: data = [ [s.strip() for s in line.split()]
                      for line in lines[i+1:i+1+rows] ]
        except Exception as ex: raise ParseGridError('not enough rows left')
        for row in data:
            if len(row) != cols: raise ParseGridError('row %d length'%len(row))
        return (i+rows+1,data)
    elif valuetype == MULTISTRING: # read following lines containing some string
        ch = settings
        j = i+1
        data = ''
        try:
            while ch in lines[j]:
                data += lines[j].strip()
                j += 1
        except Exception as ex: raise ParseError('reached eof (multistring)')
        return (j,data)
    elif valuetype == EMPTY: return (i+1,None) # skip line
    else: assert 0

# represents properties to find in a puzzle file
# supports string/integer/float values on the same line as the property name
# supports grids that use existing integers to specify their dimensions
# supports multiline strings that each contain a substring
# the multiline strings are probably only needed for the moves data
# the ignore argument for 
class PuzzleParser:
    def __init__(self):
        # maps property name --> (TYPE,settings)
        self.properties = dict()
        self.ignore = dict()
    def _hasProp(self,name):
        assert type(name) == str
        return (name in self.properties) or (name in self.ignore)
    def removeProp(self,name):
        if name in self.properties: self.properties.pop(name)
        if name in self.ignore: self.ignore.pop(name)
    def addString(self,name,ignore=False):
        assert not self._hasProp(name)
        if ignore: self.ignore[name] = (STRING,None)
        else: self.properties[name] = (STRING,None)
    def addInteger(self,name,ignore=False):
        assert not self._hasProp(name)
        if ignore: self.ignore[name] = (INTEGER,None)
        else: self.properties[name] = (INTEGER,None)
    def addFloat(self,name,ignore=False):
        assert not self._hasProp(name)
        if ignore: self.ignore[name] = (FLOAT,None)
        else: self.properties[name] = (FLOAT,None)
    def addGrid(self,name,rowprop,colprop,ignore=False):
        # gets dimensions from other properties
        # or can use fixed integers to get dimensions
        assert not self._hasProp(name)
        if type(rowprop) == str:
            assert self.properties[rowprop] == (INTEGER,None)
        elif type(rowprop) == int: assert rowprop > 0
        else: raise TypeError()
        if type(colprop) == str:
            assert self.properties[colprop] == (INTEGER,None)
        elif type(colprop) == int: assert colprop > 0
        else: raise TypeError()
        if ignore: self.ignore[name] = (GRID,(rowprop,colprop))
        else: self.properties[name] = (GRID,(rowprop,colprop))
    def addMultiString(self,name,ch,ignore=False):
        # ch is character to find in lines
        assert not self._hasProp(name)
        assert type(ch) == str
        if ignore: self.ignore[name] = (MULTISTRING,ch)
        else: self.properties[name] = (MULTISTRING,ch)
    def addEmpty(self,name,ignore=False):
        assert not self._hasProp(name)
        if ignore: self.ignore[name] = (EMPTY,None)
        else: self.properties[name] = (EMPTY,None)
    def parseFile(self,file,jobj): # jobj = object to add properties to
        assert type(jobj) == dict
        lines = [line.strip() for line in open(file,'r') if line != '\n']
        assert lines[0] == 'begin'
        assert lines[-1] == 'end'
        i = 0
        while i < len(lines):
            if lines[i] == 'begin': i += 1; continue
            if lines[i] == 'end': i += 1; continue
            si = lines[i].find(' ')
            if si == -1: si = len(lines[i])
            prop = lines[i][:si].strip()
            if prop in self.ignore:
                typ,sett = self.ignore[prop]
                try: i,_ = parseValue(lines,i,typ,sett,jobj)
                except Exception as ex: raise ex
                    #log('error: '+prop)
                    #i += 1
            elif prop in self.properties:
                #assert prop not in jobj # dont overwrite repeated property
                typ,sett = self.properties[prop]
                try:
                    i,value = parseValue(lines,i,typ,sett,jobj)
                    # check if value is repeated (happens in improper data)
                    # if it is, just ensure it is the same thing
                    if (prop in jobj) and (value != jobj[prop]):
                        raise ParseError('repeated prop = '+prop)
                    jobj[prop] = value
                except Exception as ex: raise ex
                    #jobj[prop] = None # indicates failure
                    #log('error: '+prop)
                    #i += 1
            else: raise UnknownProp(prop)

# below are functions to add pretty standard property values to parsers
# these (are expected to) occur within several types of puzzles

def addInfos(parser): # standard puzzle info strings
    parser.addString('puzzle')
    parser.addString('variant') # may not be present
    parser.addString('layout') # may not be present
    parser.addString('options') # may not be present
    parser.addString('author')
    parser.addString('solver') # may not be present
    parser.addString('source') # url
    parser.addString('title')
    parser.addString('info') # unknown
    parser.addString('mail') # email adddress
    parser.addString('pid') # problem id?
    parser.addMultiString('moves',';') # should be present iff solver is present
    parser.addInteger('unit') # pixel dimensions of cells?
    parser.addInteger('unitsize')

def addRCGrid(parser,areas=True): # grids specified by "rows" and "cols"
    parser.addInteger('rows')
    parser.addInteger('cols')
    parser.addInteger('size')
    parser.addInteger('depth')
    parser.addGrid('problem','rows','cols')
    if areas: parser.addGrid('areas','rows','cols')
    parser.addGrid('solution','rows','cols')

def addSizeGrid(parser,areas=True): # grids specified by "size"
    #parser.addInteger('rows')
    #parser.addInteger('cols')
    parser.addInteger('size')
    parser.addInteger('depth')
    parser.addGrid('problem','size','size')
    if areas: parser.addGrid('areas','size','size')
    parser.addGrid('solution','size','size')

def addPxPy(parser): # may be sudoku specific?
    parser.addInteger('pattern')
    parser.addInteger('patternx')
    parser.addInteger('patterny')

# row/col labels, how many rows to expect, use size property for number of cols
def addRCLabelsSize(parser,count=1):
    parser.addGrid('rlabels',count,'size')
    parser.addGrid('clabels',count,'size')

def makeRCGridParser(areas=True): # areas=True was added for a Sudoku workaround
    parser = PuzzleParser()
    addInfos(parser)
    addRCGrid(parser,areas)
    return parser

def makeSizeGridParser(areas=True):
    parser = PuzzleParser()
    addInfos(parser)
    addSizeGrid(parser,areas)
    return parser

# map subdir -> (dict of parsers)
# a dict of parsers maps parsername -> PuzzleParser object
allparsers = dict()

PARSER_RCGRID = makeRCGridParser()
PARSER_SIZEGRID = makeSizeGridParser()

def addBasicGridParsers(puzzle):
    allparsers[puzzle] = { puzzle.lower()+'-rc': PARSER_RCGRID,
                           puzzle.lower()+'-size': PARSER_SIZEGRID }

# notes: the 'options' property only has the value 'diagonal'
def addSudokuParsers():
    sudokurc = makeRCGridParser(False)
    addPxPy(sudokurc)
    sudokusize = makeSizeGridParser(False)
    sudokusize.addEmpty('areas') # workaround for puzzles 1052-1060
    addPxPy(sudokusize)
    allparsers['Sudoku'] = {'sudoku-rc':sudokurc,
                            'sudoku-size':sudokusize}

def addAbcEndViewParsers():
    abcendview = makeSizeGridParser()
    addRCLabelsSize(abcendview,2)
    abcendview.addString('diagonals')
    allparsers['Abc-End-View'] = {'abcendview':abcendview}

def addAbcKombiParsers():
    abckombirc = makeRCGridParser()
    abckombirc.addGrid('rlabels','depth','rows')
    abckombirc.addGrid('clabels','depth','cols')
    allparsers['Abc-Kombi'] = {'abckombi':abckombirc}

# problem is given as (size+2)^2 grid, use the fixed 7x7 as a workaround
def addAbcPfadParsers():
    abcpfad = PuzzleParser()
    addInfos(abcpfad)
    abcpfad.addInteger('size')
    abcpfad.addGrid('problem',7,7)
    abcpfad.addGrid('solution',5,5)
    allparsers['Abc-Pfad'] = {'abcpfad':abcpfad}

def addZiegelmauerParsers():
    ziegelmauer = makeSizeGridParser()
    ziegelmauer.removeProp('areas')
    ziegelmauer.addString('areas') # observed to be "single" or "double"
    allparsers['Ziegelmauer'] = {'ziegelmauer':ziegelmauer}

def addZahlenkreuzParsers():
    zahlenkreuz = makeSizeGridParser()
    addRCLabelsSize(zahlenkreuz)
    allparsers['Zahlenkreuz'] = {'zahlenkreuz':zahlenkreuz}

def addZahlenlabyrinthParsers():
    zahlenlabyrinth = makeSizeGridParser()
    zahlenlabyrinth.addGrid('lines','size','size')
    allparsers['Zahlenlabyrinth'] = {'zahlenlabyrinth':zahlenlabyrinth}

def addWolkenkratzerParsers():
    wolkenkratzer = makeSizeGridParser()
    addRCLabelsSize(wolkenkratzer,2)
    allparsers['Wolkenkratzer'] = {'wolkenkratzer':wolkenkratzer}
    allparsers['Wolkenkratzer-2'] = {'wolkenkratzer':wolkenkratzer}

def initParsers():
    addSudokuParsers() # adds "area" as empty for a workaround
    # many puzzles are similar and can be parsed with common parsers
    basicGridPuzzles = ['Heyawake','Akari','Fillomino','LITS','Nurikabe',
        'Slitherlink','Sudoku/2D','Sudoku/Butterfly','Sudoku/Chaos',
        'Sudoku/Clueless-1','Sudoku/Clueless-2','Sudoku/Flower',
        'Sudoku/Gattai-8','Sudoku/Samurai','Sudoku/Shogun','Sudoku/Sohei',
        'Sudoku/Sumo','Sudoku/Windmill','Zipline','Zeltlager','Zeltlager-2',
        'Zahlenschlange','Zehnergitter','Usoone','Usotatami','Vier-Winde',
        'View','Sikaku','Suguru','Sukoro','Sumdoku','Sukrokuro','Suraromu',
        'Yagit','Yajilin','Yajisan-Kazusan','Yin-Yang','Yonmasu','Yosenabe',
        'Yakuso','Tueren','Tripletts','Trinudo','Trace-Numbers','Toichika',
        'Tohu-Wa-Vohu']
    for bgp in basicGridPuzzles:
        addBasicGridParsers(bgp)
    addAbcEndViewParsers()
    addAbcKombiParsers()
    addAbcPfadParsers()
    addZiegelmauerParsers()
    addZahlenkreuzParsers()
    addZahlenlabyrinthParsers()
    addWolkenkratzerParsers() # also adds Wolkenkratzer-2

# given a directory and set of parsers, this will try parsers on each file until
# successful and write the result json objects on their own line to output.json
def parserLoop(path,parsers):
    assert len(parsers) > 0
    path = os.path.normpath(path)
    assert os.path.isdir(path)
    if os.path.isfile(path+'/output.success'):
        print('already completed:',path)
        return
    else: print('processing dir:',path)
    files = [f for f in os.listdir(path) if f.endswith('.txt')]
    outf = open(path+'/'+'output.json','w')
    for f in sorted(files):
        #print('processing: '+f)
        fname,fext = os.path.splitext(f)
        success = False
        for parsername in parsers:
            #print('trying parser:',parsername)
            # keep original file name available, should not be named the same
            # as any of the properties in the puzzle files
            jobj = {'__file__':fname}
            try:
                parsers[parsername].parseFile(path+'/'+f,jobj)
                print('success:',path+'/'+f)
                log(path+'/'+f+' : success '+parsername)
                success = True
                break
            except Exception as ex: err = ex
                #log('fail: parser = '+parsername+' message = '
                #    +'%s(%s)'%(type(ex).__name__,str(ex)))
        if success:
            outf.write(json.dumps(jobj,separators=(',', ':'))) # compact
            outf.write('\n')
        else:
            print('failed:',path+'/'+f,':',str(err))
            log(path+'/'+f+' : fail : '+str(err))
            outf.close()
            logfile.close()
            quit()
    # use a file to mark that parsing was successful
    successfile = open(path+'/output.success','w')
    successfile.write('success\n')
    successfile.close()
    outf.close()

# for writing info/error messages
logfile = None
def log(msg):
    #print(msg)
    if logfile: logfile.write(msg+'\n')

def main(puzzle):
    global logfile
    path = 'puzzle_data/'+puzzle
    assert os.path.isdir(path)
    logfile = open(os.path.normpath(path)+'/output.log','w')
    initParsers()
    if puzzle not in allparsers:
        print('invalid puzzle type')
        quit()
    parserLoop(path,allparsers[puzzle])
    logfile.close()

if __name__ == '__main__': main(sys.argv[1])
