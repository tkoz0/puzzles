# Python3 scrypt to convert the puzzle webpages from janko.at into verified
# json files representing puzzles with exactly 1 solution.
# Usage: python3 puzzle_verify.py <input_dir> <output_file> <puzzle>

import os,sys,math
from bs4 import BeautifulSoup
import puzzle_utils
from puzzle_solvers import SolveSudoku

def main(inputDir,outputFile,puzzle):
    inputDir = os.path.normpath(inputDir)
    if not os.path.isdir(inputDir):
        sys.stderr.write('Not a directory\n')
    else:
        for file in [inputDir+'/'+f for f in sorted(os.listdir(inputDir))]:
            result = verifyFile(file,puzzle)
            # TODO write results as json to file

def extractPuzzleData(webpage):
    bs4page = BeautifulSoup(open(webpage,'r').read(),'html.parser')
    tag = bs4page.find(id='data')
    assert tag is not None
    return tag.text.strip().splitlines()

def verifyFile(file,puzzle):
    print('verifying:',file)
    data = extractPuzzleData(file)
    # TODO use puzzle parameter to determine how to parse/verify
    # below is a temporary test
    parser1 = puzzle_utils.makeParserRCGrid(areas=False)
    parser2 = puzzle_utils.makeParserSizeGrid(areas=False)
    puzzle_utils.addParamsPxPy(parser1)
    puzzle_utils.addParamsPxPy(parser2)
    parser1.addNone('areas') # workaround for a few puzzles
    parser2.addNone('areas')
    try:
        result = parser1.parse(data)
    except Exception as e:
        try:
            result = parser2.parse(data)
        except Exception as e:
            print(e)
            print('failed:',file)
            print('\n'.join(data))
            quit()
    grid = result['problem']
    if 'size' in result:
        size = int(result['size'])
        assert int(math.sqrt(size))**2 == size
        br = bc = int(math.sqrt(size))
    else:
        assert result['rows'] == result['cols']
        size,sizeroot = int(result['rows']),int(math.sqrt(int(result['rows'])))
        assert sizeroot**2 == size
        br = bc = sizeroot
    for r in range(br*bc):
        for c in range(br*bc):
            if grid[r][c] == '-' or grid[r][c] == '.':
                grid[r][c] = 0
            else:
                grid[r][c] = int(grid[r][c])
                assert grid[r][c] > 0
    solver = SolveSudoku(grid,br,bc)
    solver.solveBacktrack()
    # TODO end temporary section

if __name__ == '__main__':
    main(sys.argv[1],sys.argv[2],sys.argv[3])
