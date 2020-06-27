# PuzzleParser class to provide functionality common to parsing most puzzles on
# janko.at. It is designed to produce JSON data that is convenient to use.

# Puzzle data usually looks like this:

# begin
# puzzle sudoku
# size 9
# problem
# - - 1 - - 2 - - 3
# ...
# end

# The PuzzleParser models this by parsing a parameter name and a value either
# on the same line or spanning lines after the line with the parameter name.

from itertools import chain

class PuzzleParser:
    
    # data types defined that can be parsed
    NONE        = 0 # property name only, no value
    STRING      = 1 # string on same line
    GRID        = 2 # grid of space-separated values
    LONG_STRING = 3 # string spanning multiple lines
    
    # constructor, parameter determines whether to expect the header and footer
    # lines "begin" and "end"
    def __init__(self,use_beg_end=True):
        self.params = dict() # name -> (TYPE,[parse_params...])
        self.use_beg_end = use_beg_end
    
    # functions to add data types
    def addNone(self,name):
        assert name not in self.params
        self.params[name] = (PuzzleParser.NONE,)
    def addString(self,name):
        assert name not in self.params
        self.params[name] = (PuzzleParser.STRING,)
    def addGrid(self,name,rowparam,colparam): # row/col can be str or int
        assert name not in self.params
        # should have already defined parameters to parse grid size
        if type(rowparam) == str:
            assert self.params[rowparam] == (PuzzleParser.STRING,)
        else:
            assert type(rowparam) == int and rowparam > 0
        if type(colparam) == str:
            assert self.params[colparam] == (PuzzleParser.STRING,)
        else:
            assert type(colparam) == int and colparam > 0
        self.params[name] = (PuzzleParser.GRID,rowparam,colparam)
    def addLongString(self,name,substr): # substr to find
        assert name not in self.params
        assert type(substr) == str
        self.params[name] = (PuzzleParser.LONG_STRING,substr)
    def removeParam(self,name):
        assert name in self.params
        self.params.pop(name)
    
    # function to parse a file with this parser
    # file should be an iterable of lines
    def parse(self,file):
        result = dict()
        itr = iter(line.strip() for line in file)
        if self.use_beg_end and next(itr) != 'begin':
            raise Exception('does not start with "begin" line')
        found_end = False
        while True:
            try:
                line = next(itr).split()
                if line == []: continue # skip blank lines
                if line == ['end']:
                    found_end = True
                    break # end marker
            except StopIteration:
                break
            if line[0] not in self.params:
                raise Exception('unknown parameter: '+line[0])
            if line[0] in result:
                raise Exception('duplicate parameter: '+line[0])
            type_ = self.params[line[0]]
            if type_[0] == PuzzleParser.NONE:
                result[line[0]] = None
            elif type_[0] == PuzzleParser.STRING:
                result[line[0]] = ' '.join(line[1:])
            elif type_[0] == PuzzleParser.GRID:
                rows,cols = type_[1],type_[2]
                # if row/col parameter is string, get from results
                try:
                    if type(rows) == str:
                        rows = int(result[rows])
                    if type(cols) == str:
                        cols = int(result[cols])
                except:
                    raise Exception('grid dimensions issue: '+line[0])
                grid = []
                for _ in range(rows):
                    try:
                        row = next(itr).split()
                    except:
                        raise Exception('grid not enough rows: '+line[0])
                    if len(row) != cols:
                        raise Exception('grid row length incorrect: '+line[0])
                    grid.append(row)
                result[line[0]] = grid
            elif type_[0] == PuzzleParser.LONG_STRING:
                substr = type_[1]
                longstr = ''
                while True:
                    try:
                        nextstr = next(itr)
                    except StopIteration:
                        break
                    if substr in nextstr:
                        longstr += nextstr
                    else: # put the peeked next line back into the itr stream
                        itr = chain([nextstr],itr)
                        break
                result[line[0]] = longstr
        if self.use_beg_end and not found_end:
            raise Exception('did not find "end" line')
        return result

