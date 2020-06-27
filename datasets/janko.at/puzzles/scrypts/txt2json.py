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
import puzzle_utils
from puzzle_solvers import SolveSudoku

def main(input_dir,output_dir,puzzle):
    ''' loops over all files to process '''
    input_dir = os.path.normpath(input_dir)
    output_dir = os.path.normpath(output_dir)
    assert os.path.isdir(input_dir)
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
        outfile = open(outfile,'w')
        outfile.write(json.dumps(outdata,separators=(',',':')))
        outfile.close()
        return True
    except Exception as e:
        print('ERROR:',type(e).__name__,str(e))
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
        try: parsed = parser2.parse(lines)
        except: pass
    if parsed is None:
        print('ERROR: parsers failed')
        return
    outdata = dict() # represent the sudoku object
    outdata['__file__'] = filename
    outdata['__data__'] = parsed
    diagonals = ('options' in parsed and result['options'] == 'diagonals') \
                or ('diagonals' in parsed['puzzle'])
    if not diagonals: outdata['puzzle'] = 'sudoku'
    else: outdata['puzzle'] = 'sudoku,diagonals'
    # lambda to convert digits from input grids
    str2int = lambda s : 0 if s in '-.' else int(s)
    # problem grid
    problem = [list(map(str2int,row)) for row in parsed['problem']]
    parsed['problem'] = problem
    outdata['problem'] = problem
    # determine block sizes
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
    outdata['blockrows'] = br
    outdata['blockcols'] = bc
    # solve puzzle
    solver = SolveSudoku(problem,(br,bc),diagonals)
    assert len(solver.solutions) == 1, 'solutions != 1'
    if 'solution' in parsed:
        solution = [list(map(str2int,row)) for row in parsed['solution']]
        assert solution == solver.solutions[0], 'parsed solution is wrong'
    outdata['solution'] = solver.solutions[0]
    return outdata

if __name__ == '__main__': main(sys.argv[1],sys.argv[2],sys.argv[3])
