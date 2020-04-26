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

# usage: puzzle_json.py <puzzle .txt dir> <puzzle type>

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
                typ,sett = self.properties[prop]
                try: i,jobj[prop] = parseValue(lines,i,typ,sett,jobj)
                except Exception as ex: raise ex
                    #jobj[prop] = None # indicates failure
                    #log('error: '+prop)
                    #i += 1
            else: raise UnknownProp(prop)

# below are functions to add pretty standard property values to parsers
# these (are expected to) occur within several types of puzzles

def addInfos(parser): # standard puzzle info strings
    parser.addString('puzzle')
    parser.addString('variant')
    parser.addString('options')
    parser.addString('author')
    parser.addString('solver')
    parser.addString('source')
    parser.addString('title')
    parser.addString('info')
    parser.addMultiString('moves',';')

def addRCGrid(parser,areas=True): # grids specified by "rows" and "cols"
    parser.addInteger('unit')
    parser.addInteger('rows')
    parser.addInteger('cols')
    parser.addInteger('size')
    parser.addInteger('depth')
    parser.addGrid('problem','rows','cols')
    if areas: parser.addGrid('areas','rows','cols')
    parser.addGrid('solution','rows','cols')

def addSizeGrid(parser,areas=True): # grids specified by "size"
    parser.addInteger('unit')
    parser.addInteger('rows')
    parser.addInteger('cols')
    parser.addInteger('size')
    parser.addInteger('depth')
    parser.addGrid('problem','size','size')
    if areas: parser.addGrid('areas','size','size')
    parser.addGrid('solution','size','size')

def addPxPy(parser): # may be sudoku specific?
    parser.addInteger('pattern')
    parser.addInteger('patternx')
    parser.addInteger('patterny')

def makeStandardRCGridParser(areas=True):
    parser = PuzzleParser()
    addInfos(parser)
    addRCGrid(parser,areas)
    return parser

def makeStandardSizeGridParser(areas=True):
    parser = PuzzleParser()
    addInfos(parser)
    addSizeGrid(parser,areas)
    return parser

# map subdir -> (dict of parsers)
# a dict of parsers maps parsername -> PuzzleParser object
allparsers = dict()

# notes: the 'options' property only has the value 'diagonal'
def addSudokuParsers():
    sudokurc = makeStandardRCGridParser(False)
    addPxPy(sudokurc)
    sudokusize = makeStandardSizeGridParser(False)
    sudokusize.addEmpty('areas') # workaround for puzzles 1052-1060
    addPxPy(sudokusize)
    allparsers['Sudoku'] = {'sudokurc':sudokurc,
                            'sudokusize':sudokusize}

def addHeyawakeParsers():
    allparsers['Heyawake'] = {'heyawakerc':makeStandardRCGridParser(),
                              'heyawakesize':makeStandardSizeGridParser()}

def addAkariParsers():
    allparsers['Akari'] = {'akarirc':makeStandardRCGridParser(),
                           'akarisize':makeStandardSizeGridParser()}

def initParsers():
    addSudokuParsers()
    addHeyawakeParsers()
    addAkariParsers()

# given a directory and set of parsers, this will try parsers on each file until
# successful and write the result json objects on their own line to output.json
def parserLoop(path,parsers):
    path = os.path.normpath(path)
    assert os.path.isdir(path)
    files = [f for f in os.listdir(path) if f.endswith('.txt')]
    outf = open(path+'/'+'output.json','w')
    for f in sorted(files):
        print('processing: '+f)
        fname,fext = os.path.splitext(f)
        success = False
        for parsername in parsers:
            print('trying parser:',parsername)
            jobj = {'file':fname}
            try:
                parsers[parsername].parseFile(path+'/'+f,jobj)
                log(f+' : success '+parsername)
                success = True
                break
            except Exception as ex: pass
                #log('fail: parser = '+parsername+' message = '
                #    +'%s(%s)'%(type(ex).__name__,str(ex)))
        if success:
            outf.write(json.dumps(jobj))
            outf.write('\n')
        else:
            log(f+' : fail')
            outf.close()
            logfile.close()
            quit()
    outf.close()

# for writing info/error messages
logfile = None
def log(msg):
    print(msg)
    if logfile: logfile.write(msg+'\n')

def main(path,puzzle):
    global logfile
    assert os.path.isdir(path)
    logfile = open(os.path.normpath(path)+'/output.log','w')
    initParsers()
    if puzzle not in allparsers:
        print('invalid puzzle type')
        quit()
    parserLoop(path,allparsers[puzzle])
    logfile.close()

if __name__ == '__main__': main(sys.argv[1],sys.argv[2])
