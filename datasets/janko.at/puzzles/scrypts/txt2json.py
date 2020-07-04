'''
Python3 scrypt for converting logic puzzle data from the txt files to a more
convenient JSON representation. The txt files may need to be edited if there are
formatting errors. Additionally, it verifies uniqueness of the solutions using
logic puzzle solvers.

Usage: python3 txt2json.py <input_dir> <output_dir> <puzzle_type>
Does not recurse into subdirectories: input_dir/a.txt -> output_dir/a.json

The JSON output will contain the following data:
"__file__": name of the input file (probably similar to 001.a.htm)
"__data__": the JSON object of data parsed directly from the page contents
There will also be the parameters which vary per puzzle. For details, see the
comment on the puzzle specific parser function.
'''

import os,sys,json,math

from puzzle_parser import PuzzleParser
from puzzle_parser import ParseException

import puzzle_utils

from puzzle_solvers import SolveSudoku
from puzzle_solvers import SolveHakyuu

class VerifyException(Exception):
    ''' Thrown when an issue occurs with verifying a puzzle '''

def main(input_dir,output_dir,puzzle):
    ''' loops over all files to process '''
    input_dir = os.path.normpath(input_dir)
    output_dir = os.path.normpath(output_dir)
    assert os.path.isdir(input_dir)
    # make output dir if not exist
    if not os.path.isdir(output_dir):
        os.mkdir(output_dir)
    assert os.path.isdir(output_dir)
    files = os.listdir(input_dir)
    count = 0
    for file in sorted(files):
        count += 1
        infile = input_dir+'/'+file
        name,ext = os.path.splitext(file)
        if ext != '.txt': continue
        outfile = output_dir+'/'+name+'.json'
        if os.path.isfile(outfile):
            print(f'already processed: {infile} ({count}/{len(files)})')
            continue
        if convert(infile,outfile,puzzle):
            print(f'success: {infile} -> {outfile} ({count}/{len(files)})')

def convert(infile,outfile,puzzle):
    ''' picks the appropriate puzzle parser and processes a single file '''
    print('converting:',infile)
    try: # find function to use based on puzzle name
        converter = globals()['convert_'+puzzle]
        outdata = converter(infile,list(open(infile,'r')))
        assert type(outdata) == dict, 'converter did not return dict type'
        outfile = open(outfile,'w')
        #outfile.write(json.dumps(outdata,separators=(',',':')))
        outfile.write(json.dumps(outdata,indent=4)) # for readability
        outfile.close()
        return True
    except VerifyException as e:
        print('failed to verify:',str(e))
    except ParseException as e:
        print('failed to parse:',str(e))
    return False

def convert_sudoku(filename,lines):
    '''
    Sudoku output format:
    "puzzle": "sudoku" or "sudoku,diagonals"
    "problem": N*N array of integers in [0,N]
    "blockrows": number of rows in a block
    "blockcols": number of cols in a block
    "solution": N*N array of integers in [1,N]
    '''
    # sudoku parameters are a bit different than most puzzles
    parser1 = puzzle_utils.makeParserRCGrid(False)
    parser2 = puzzle_utils.makeParserSizeGrid(False)
    parser1.addNone('areas')
    parser2.addNone('areas')
    puzzle_utils.addParamsPxPy(parser1)
    puzzle_utils.addParamsPxPy(parser2)
    parsed = None
    try: parsed = parser1.parse(lines)
    except:
        parsed = parser2.parse(lines)
    if parsed is None:
        raise ParseException('ERROR: parsers failed')
    outdata = dict() # represent the sudoku object
    outdata['__file__'] = filename
    outdata['__data__'] = parsed
    # parsing the puzzle from the text file data
    if 'puzzle' not in parsed:
        raise VerifyException('puzzle type not specified')
    diagonals = ('options' in parsed and parsed['options'] == 'diagonals') \
                or ('diagonals' in parsed['puzzle'])
    if not diagonals: outdata['puzzle'] = 'sudoku'
    else: outdata['puzzle'] = 'sudoku,diagonals'
    # lambda to convert digits from input grids
    str2int = lambda s : 0 if s in '-.' else int(s)
    # problem grid
    try: problem = [list(map(str2int,row)) for row in parsed['problem']]
    except: raise VerifyException('cannot convert problem grid to ints')
    outdata['problem'] = problem
    try: # determine block sizes
        if 'pattern' in parsed:
            br = bc = int(parsed['pattern'])
        elif 'patternx' in parsed:
            br,bc = int(parsed['patterny']),int(parsed['patternx'])
        elif 'size' in parsed:
            size = int(parsed['size'])
            br = bc = int(math.sqrt(size))
            assert br*bc == size, 'N is not perfect square'
        else:
            pr,pc = parsed['rows'],parsed['cols']
            assert pr == pc, 'not a square puzzle'
            size = int(pr)
            br = bc = int(math.sqrt(size))
            assert br*bc == size, 'N is not perfect square'
    except: raise VerifyException('cannot determine block sizes')
    outdata['blockrows'] = br
    outdata['blockcols'] = bc
    # solve puzzle
    solver = SolveSudoku(problem,(br,bc),diagonals)
    if len(solver.solutions) != 1: raise VerifyException('solutions != 1')
    if 'solution' in parsed:
        try:
            solution = [list(map(str2int,row)) for row in parsed['solution']]
            assert solution == solver.solutions[0]
        except: raise VerifyException('failed check against provided solution')
    outdata['solution'] = solver.solutions[0]
    return outdata

def convert_hakyuu(filename,lines):
    '''
    Hakyuu output format:
    "puzzle": "hakyuu"
    "problem": R*C array of integers [0,N] (N = max area size)
    "areas": R*C array of integers
    "solution": R*C array of integers [1,N] (N = max area size)
    '''
    parsed = None
    try: parsed = puzzle_utils.COMMON_RCGRID.parse(lines)
    except:
        parsed = puzzle_utils.COMMON_SIZEGRID.parse(lines)
    if parsed is None:
        raise ParseException('ERROR: parsers failed')
    outdata = dict()
    outdata['__file__'] = filename
    outdata['__data__'] = parsed
    outdata['puzzle'] = 'hakyuu'
    try:
        if 'size' in parsed: R = C = int(parsed['size'])
        else: R,C = int(parsed['rows']),int(parsed['cols'])
    except: raise VerifyException('error parsing grid size')
    str2int = lambda s : 0 if s in '-.' else int(s)
    try:
        problem = [list(map(str2int,row)) for row in parsed['problem']]
        areas = [list(map(int,row)) for row in parsed['areas']]
    except: raise VerifyException('error converting problem/area grid to ints')
    outdata['problem'] = problem
    outdata['areas'] = areas
    # solve puzzle
    solver = SolveHakyuu(problem,areas)
    try:
        solution = [list(map(int,row)) for row in parsed['solution']]
        assert len(solver.solutions) == 1, 'solutions != 1'
        assert solution == solver.solutions[0], 'parsed solution is wrong'
    except: raise VerifyException('failed check against provided solution')
    outdata['solution'] = solution
    return outdata

if __name__ == '__main__': main(sys.argv[1],sys.argv[2],sys.argv[3])
