from puzzle_parser import PuzzleParser

# params that most puzzles will have
def addParamsCommon(parser):
    parser.addString('puzzle')
    parser.addString('author')
    parser.addString('solver')
    parser.addLongString('moves',';')
    parser.addString('source')
    parser.addString('unit')
    parser.addString('depth')
    parser.addString('info')
    parser.addString('title')
    parser.addString('variant')
    parser.addString('layout')
    parser.addString('options')
    parser.addString('mail')
    parser.addString('pid')

# params to parse typical grids defined by row x col
def addParamsRCGrid(parser,areas=True):
    parser.addString('rows')
    parser.addString('cols')
    parser.addGrid('problem','rows','cols')
    parser.addGrid('solution','rows','cols')
    if areas:
        parser.addGrid('areas','rows','cols')

# params to parse typical grids defined by size x size
def addParamsSizeGrid(parser,areas=True):
    parser.addString('size')
    parser.addGrid('problem','size','size')
    parser.addGrid('solution','size','size')
    if areas:
        parser.addGrid('areas','size','size')

# params to parse row/col labels for size x size grids
def addParamsRCLabelsSize(parser,count=1):
    parser.addGrid('rlabels',count,'size')
    parser.addGrid('clabels',count,'size')

# params to parse row/col labels for row x col grids
def addParamsRCLabelsRC(parser,count=1):
    parser.addGrid('rlabels',count,'rows')
    parser.addGrid('clabels',count,'cols')

# this may be sudoku specific
def addParamsPxPy(parser):
    parser.addString('pattern')
    parser.addString('patternx')
    parser.addString('patterny')

# common row x col grid parser that works for many puzzles
def makeParserRCGrid(areas=True):
    parser = PuzzleParser()
    addParamsCommon(parser)
    addParamsRCGrid(parser,areas)
    return parser

# common size x size grid parser that works for many puzzles
def makeParserSizeGrid(areas=True):
    parser = PuzzleParser()
    addParamsCommon(parser)
    addParamsSizeGrid(parser,areas)
    return parser

# common row x col grid with row/col labels
def makeParserRCGridLabels(areas=True,count=1):
    parser = makeParserRCGrid(areas)
    addParamsRCLabelsRC(parser,count)
    return parser

# common size x size grid with row/col labels
def makeParserSizeGridLabels(areas=True,count=1):
    parser = makeParserSizeGrid(areas)
    addParamsRCLabelsSize(parser,count)
    return parser

# common ready to use parsers, should not be modified
COMMON_RCGRID = makeParserRCGrid(areas=True)
COMMON_SIZEGRID = makeParserSizeGrid(areas=True)
COMMON_RCGRID_LABELS_1 = makeParserRCGridLabels(areas=True,count=1)
COMMON_RCGRID_LABELS_2 = makeParserRCGridLabels(areas=True,count=2)
COMMON_SIZEGRID_LABELS_1 = makeParserSizeGridLabels(areas=True,count=1)
COMMON_SIZEGRID_LABELS_2 = makeParserSizeGridLabels(areas=True,count=2)

