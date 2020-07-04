'''
puzzle_solvers module

Each class here is intended to be used to construct a logic puzzle instance and
solve it. When creating an instance, the constructor runs the solver so the
puzzle instance has solution information available once the object is created.
'''

from itertools import chain

class ContradictionException(Exception):
    ''' Thrown when a contradiction occurs during the solving process '''

class InvalidPuzzleException(Exception):
    ''' Thrown when the provided puzzle parameters are invalid '''

class SolveSudoku:
    '''
    -- Solver for sudoku and some of its variants --
    Sudoku is a N*N grid of cells requiring the numbers 1..N exactly once in
    each row, column, and certain areas of N cells (dividing it into N areas).
    The areas may be rectangular (regular sudoku), irregularly shaped, or even
    disabled (making the puzzle a latin square).
    
    Solving will find all solutions with the current behavior. Each element of
    self.solutions (if any) will be N*N arrays of integers.
    
    Member variables:
    - self.N = grid side length parameter
    - self.solutions = list of solution grids found (N*N array of integers 1..N)
    - self._cells[i] = _Cell object at (row,col) = (i//N,i%N)
    - self._areas[i] = list of N cells (by index) in area i
    - self._areasof[i] = list of areas (by index) containing cell i
    Read only variables (after initialization): _areas, _areasof
    
    TODO: support a max solutions limit and terminate recursion after that
    TODO: support variants with nonstandard shapes (not a square)
    TODO (maybe): track change history for recursion instead of copying the grid
    before making a guess
    '''
    
    class _Cell:
        '''
        A representation of possible values for a cell during the solving
        process as possibilities get eliminated.
        Member variables:
        self.nums[n] = is n+1 a possible value in this cell
        self.count = how many values are possible in this cell
        '''
        def __init__(self,N):
            ''' N is the grid side length parameter '''
            self.nums = [True]*N
            self.count = N
        def possible(self,n):
            ''' True if n is marked as a possible value in this cell '''
            return self.nums[n-1]
        def __getitem__(self,n):
            ''' True if n is marked as a possible value in this cell '''
            return self.nums[n-1]
        def elim(self,n):
            ''' Eliminate a possibility, return True if the state changes '''
            n -= 1
            if self.nums[n]:
                self.nums[n] = False
                self.count -= 1
                return True
            return False
        def undo(self,n):
            ''' Undo an elimination, return True if the state changes '''
            n -= 1
            if not self.nums[n]:
                self.nums[n] = True
                self.count += 1
                return True
            return False
    
    def __init__(self,problem,areas=None,diagonals=False,customareas=None):
        '''
        Creates an instances of the solver and immediately runs
        Note that N >= 1 is required below
        
        Parameters for SolveSudoku:
        - problem = N*N grid of int, 0 for empty, 1..N for given clues
        - areas = one of the following 3 possibilities
          - None -> latin square (no areas)
          - (br,bc) -> rectangular br*bc areas, br,bc are positive integers and
                br*bc == N (if either are 1, it is the same as a latin square)
          - N*N array -> area division, must use N distinct symbols and contain
                         N instances of each (each symbol represents an area)
        - diagonals = whether or not to require 1..N in the diagonals
        - customareas = list of additional areas, currently not supported
        
        TODO: add support for (customareas)
        '''
        if customareas is not None:
            raise InvalidPuzzleException('customareas not supported yet')
        self.N = len(problem)
        if self.N < 1 or not SolveSudoku._check_givens(problem,self.N):
            raise InvalidPuzzleException('sudoku givens are invalid')
        self.solutions = []
        self._cells = [SolveSudoku._Cell(self.N) for _ in range(self.N**2)]
        # start by creating rows and cols as areas
        self._areas = [list(range(self.N*i,self.N*(i+1)))
                       for i in range(self.N)] \
                    + [list(range(i,self.N**2,self.N)) for i in range(self.N)]
        # make diagonal areas
        if diagonals and self.N > 1:
            self._areas.append(list(range(0,self.N**2,self.N+1)))
            self._areas.append(list(range(self.N-1,self.N**2-1,self.N-1)))
        # determine how to interpret areas parameter
        if areas is None: # latin square
            more_areas = []
        elif type(areas[0]) == int: # rectangular
            br,bc = areas
            assert type(bc) == int
            if br < 1 or bc < 1 or br*bc != self.N:
                raise InvalidPuzzleException('rectangular area parameter issue')
            if br > 1 and bc > 1:
                more_areas = SolveSudoku._rect_areas(self.N,br,bc)
            else: # areas will be the same as rows/cols so it is a latin square
                more_areas = []
        else:
            more_areas = SolveSudoku._get_areas(area,self.N)
        self._areas += more_areas
        # make a mapping of cells to their areas
        self._areasof = [[] for _ in range(self.N**2)]
        for i,area in enumerate(self._areas):
            for cell in area:
                self._areasof[cell].append(i)
        # run the solver
        try: self._solve(problem)
        except ContradictionException: pass # no solutions
    
    def _check_givens(grid,N):
        ''' Checks validity of a provided problem grid '''
        if len(grid) != N:
            return False
        for row in grid:
            if len(row) != N:
                return False
            for value in row:
                if type(value) != int or value < 0 or value > N:
                    return False
        return True
    
    def _rect_areas(N,br,bc):
        ''' Creates rectangular areas for a standard sudoku grid '''
        assert br > 1 and bc > 1 and br*bc == N
        # r,c are block coordinates, rr is row number
        return [sum([list(range(N*rr+bc*c,N*rr+bc*(c+1))) # cols in block
                      for rr in range(br*r,br*(r+1))],[]) # rows in block
                   for r in range(bc) for c in range(br)] # each block position
    
    def _get_areas(areas,N):
        ''' Constructs areas from the provided area grid, None if invalid '''
        if len(areas) != N: return None # fail
        area_map = dict() # symbol -> list of cell numbers
        for r,row in enumerate(grid):
            if len(row) != N: return None
            for c,symbol in enumerate(row):
                if symbol not in area_map:
                    area_map[symbol] = []
                area_map[symbol].append(N*r+c)
        if len(area_map) != N: return None
        for area_cells in area_map.values():
            if len(area_cells) != N: return None
        # sorted keys guarantee same area order
        return list(area_map[symbol] for symbol in sorted(area_map.keys()))
    
    def _copy_cells(cells,N):
        ''' Copies the cells data, used for backtracking '''
        newcells = [SolveSudoku._Cell(N) for _ in range(N**2)]
        for i,cell in enumerate(cells):
            newcells[i].nums = cell.nums[:]
            newcells[i].count = cell.count
        return newcells
    
    '''
    Sudoku solver (with 2 reasoning strategies)
    TODO: add more reasoning strategies
    
    To ensure recursion terminates, only call the 1 possibility cell propagator
    when a change occurs that leaves 1 possibility. This ensures that it is not
    called more than once for a cell. There is no more information propagation
    work to do after it is called so it is unnecessary to call it a 2nd time.
    
    Reasoning strategies:
    1. cell with 1 possibility must contain that number
    2. area with 1 possible cell for a number must contain that number there
    
    Contradictions (prune search tree when these are found):
    1. cell reaches 0 possible numbers
    2. area has not possible location for a cell
    
    _solve():
    1. put given numbers on the grid and from each, propagate information to
    cells in the same area (eliminate this number from their possibilities)
    2. call the position elimination reasoning until it makes no progress
    3. if the puzzle is not solved by these strategies alone, call _backtrack()
    
    _backtrack(), always terminate at the point a 2nd solution is found:
    1. check for grid completion
    2. if not solved, pick a cell with 2 (or minimum) possibilities
    3. for each possibility, use a copy of the cells data to assign the value
    and use constraint propagation before calling _backtrack()
    '''
    
    def _solve(self,problem):
        ''' Main solver function, parameter is the given numbers '''
        cellnum = -1
        # set the given values to their cells
        for row in problem:
            for n in row:
                cellnum += 1
                if n == 0: continue # blank cell
                cellobj = self._cells[cellnum]
                if not cellobj.possible(n): # n must be possible in this cell
                    raise ContradictionException(
                            f'given {n} impossible in cell {cellnum}')
                if cellobj.count == 1: continue # value already set
                # multiple possibilities, eliminate others
                for m in chain(range(1,n),range(n+1,self.N+1)):
                    cellobj.elim(m)
                self._singles_propagate(cellnum,n)
        # repeat position elimination until no progress
        while self._position_elimination(): pass
        # proceed to backtracking (which initially checks if it is solved)
        self._backtrack()
    
    def _backtrack(self):
        ''' Make a guess when logic strategies do not solve it '''
        # TODO add recursion terminator (after finding n of solutions maybe)
        # loop to find a cell with minimum possible values
        sindex,scell = -1,None
        for i,cell in enumerate(self._cells):
            # finding cell with multiple options and minimum posible value
            # scell is None -> set first selection with multiple options
            if cell.count > 1 and \
                (scell is None or cell.count < scell.count):
                sindex,scell = i,cell
        if scell is None: # every cell.count == 1 (puzzle solved)
            # make N*N grid, picking the only possible value for each cell
            self.solutions.append(
                [ [ [ i for i in range(1,self.N+1)
                      if self._cells[self.N*r+c].possible(i)][0]
                    for c in range(self.N)]
                  for r in range(self.N)] )
            return
        # save original cell data so a copy can be made for backtracking search
        original_cells = self._cells
        # track whether any backtracking finds a solution
        # recursion will either find a solution or terminate with contradiction
        any_solutions = False
        # try each possible value
        for n in range(1,self.N+1):
            if not scell.possible(n): continue
            self._cells = SolveSudoku._copy_cells(original_cells,self.N)
            newscell = self._cells[sindex] # reference cell in the copied data
            # eliminate other possibilities
            for m in chain(range(1,n),range(n+1,self.N+1)):
                newscell.elim(m)
            # try constraint propagation solving
            try:
                self._singles_propagate(sindex,n) # propagate guessed cell
                while self._position_elimination(): pass
                self._backtrack()
                any_solutions = True # no exception was raised
            except ContradictionException:
                pass # failed to find solution down this search subtree
        self._cells = original_cells # backtrack
        if not any_solutions:
            raise ContradictionException('no solution in this subtree')
    
    def _position_elimination(self):
        '''
        -- Number with 1 possible cell in an area must be put there --
        Raises ContradictionException if a contradiction occurs
        Returns True if any information changes, False if nothing changes
        '''
        changed = False
        for area in self._areas:
            for n in range(1,self.N+1):
                # find cells where n is possible
                cells = [cell for cell in area if self._cells[cell].possible(n)]
                if len(cells) == 0:
                    raise ContradictionException(
                            f'{n} impossible in area {area}')
                if len(cells) == 1:
                    cellobj = self._cells[cells[0]]
                    if cellobj.count == 1:
                        continue # already set value for this cell
                    # eliminate all other values to set cell value to n
                    for m in chain(range(1,n),range(n+1,self.N+1)):
                        cellobj.elim(m)
                    # may raise ContradictionException
                    self._singles_propagate(cells[0],n)
                    changed = True # at least 1 possibility was eliminated
        return changed
    
    def _singles_propagate(self,i,n):
        '''
        -- Cell with 1 possible number must contain that number --
        Only call after decreasing number of possibilities to 1 to ensure that
        recursion will terminate.
        Raises ContradictionException if a contradiction occurs
        Returns True if any information changes, False if nothing changes
        i = cell index, n = cell value
        '''
        icell = self._cells[i] # shorter reference to it
        changed = False
        for area in self._areasof[i]:
            for cell in self._areas[area]:
                if cell == i: continue
                cellobj = self._cells[cell] # shorter reference
                # eliminate n from cells sharing an area
                # recursively propagate if it only has 1 possibility
                if not cellobj.elim(n):
                    continue # possibility information did not change
                if cellobj.count == 0:
                    raise ContradictionException(f'no nums possible in {cell}')
                if cellobj.count == 1:
                    # find the possible value
                    celln = [i for i in range(1,self.N+1)
                             if cellobj.possible(i)][0]
                    # propagate further, may raise ContradictionException
                    self._singles_propagate(cell,celln)
                changed = True # propagated to eliminate a possibility
        return changed

class SolveHakyuu:
    '''
    -- Solver for hakyuu (ripple effect) --
    Hakyuu is a R*C grid of cells divided into several areas. Each area of size
    N must contain the numbers 1..N. If the number M occurs twice in the same
    row/column, then there must be at least M cells between them.
    
    Member variables:
    - self.R = number of rows
    - self.C = number of columns
    - self.solutions = list of solution grids (R*C arrays)
    - self._cells[i] = _Cell object at (row,col) = (i//C,i%C)
    - self._areas[i] = list of cells in area i (not always the same length)
    '''
    
    class _Cell:
        '''
        A representation of possible values for a cell during the solving
        process as possibilities are eliminated.
        self.nums[n] = is n+1 a possible value in this cell
        self.count = how many values are possible in this cell
        self.area = the index of the area this cell belongs to
        Note: self.nums will not always have the same length, its length will
        vary depending on the size of the area it is part of.
        '''
        def __init__(self,N,area):
            ''' N is area size parameter '''
            self.nums = [True]*N
            self.count = N
            self.area = area
        def possible(self,n):
            ''' is n possible in this cell '''
            if n > len(self.nums): # larger than the size of its area
                return False
            return self.nums[n-1]
        def __getitem__(self,n):
            return self.possible(n)
        def elim(self,n):
            ''' Eliminates a possibility, returns True if the state changes '''
            if n > len(self.nums): # larger than the size of its area
                return False
            n -= 1
            if self.nums[n]:
                self.nums[n] = False
                self.count -= 1
                return True
            return False
        def undo(self,n):
            ''' Undo an elimination, return True if the state changes '''
            if n > len(self.nums):
                return False
            n -= 1
            if not self.nums[n]:
                self.nums[n] = True
                self.count += 1
                return True
            return False
    
    def __init__(self,problem,areas):
        '''
        Creates an instance of the solver.
        
        Parameter for SolveHakyuu:
        - problem = R*C grid of int, 0 for empty, positive for given clues
        - areas = R*C grid of symbols, a unique symbol fo reach area
        '''
        if not SolveHakyuu._check_givens(problem):
            raise InvalidPuzzleException('problem grid invalid')
        self.R = len(problem)
        self.C = len(problem[0])
        self.solutions = []
        if not self._make_areas(areas):
            raise InvalidPuzzleException('problem areas invalid')
        # create _Cell objects based on the size of their area
        self._cells = [None]*(self.R*self.C)
        for i,area in enumerate(self._areas):
            for cell in area:
                self._cells[cell] = SolveHakyuu._Cell(len(area),i)
        try: self._solve(problem)
        except ContradictionException: pass # no solutions
    
    def _check_givens(grid):
        ''' Checks input grid validity '''
        if len(grid) == 0:
            return False
        C = len(grid[0])
        if C == 0:
            return False
        for row in grid:
            if len(row) != C:
                return False
            for value in row:
                if type(value) != int or value < 0:
                    return False
        return True
    
    def _make_areas(self,areas):
        ''' Creates the areas data, returns False if error occurs '''
        if len(areas) != self.R:
            return False
        i = 0 # cell number
        mapping = dict() # symbol -> list of cells
        for row in areas:
            if len(row) != self.C:
                return False
            for symbol in row:
                if symbol not in mapping:
                    mapping[symbol] = []
                mapping[symbol].append(i)
                i += 1
        self._areas = [mapping[k] for k in sorted(mapping.keys())]
        return True
    
    def _copy_cells(cells):
        ''' Copies the cells data '''
        newcells = [SolveHakyuu._Cell(len(cell.nums),cell.area)
                    for cell in cells]
        for i,cell in enumerate(cells):
            newcells[i].nums = cell.nums[:]
            newcells[i].count = cell.count
        return newcells
    
    '''
    Hakyuu solver (with 2 reasoning strategies)
    TODO: add more reasoning strategies
    
    Similar to the sudoku solver
    1. cell with 1 possibility must contain that number
    2. area with 1 possible cell for a number must contain the number there
    
    Contradictions:
    1. cell reaches 0 possible numbers
    2. area has no possible location for a cell
    
    _solve():
    1. assign given numbers, propagate
    2. run position elimination until no progress
    3. call backtracker
    
    _backtrack():
    1. check for grid completion
    2. if not solved, pick cell with 2 (or minumum) possibilities
    3. for each possibility, assign value on a copy of cells data, propagate
    constraints, call _backtrack()
    '''
    
    def _solve(self,problem):
        ''' Main solver function '''
        cellnum = -1
        for row in problem:
            for n in row:
                cellnum += 1
                cellobj = self._cells[cellnum]
                area = self._areas[cellobj.area]
                if n == 0: # blank
                    if len(area) == 1: n = 1 # set the required 1
                    else: continue
                if not cellobj.possible(n): # n must be possible here
                    raise ContradictionException(
                            f'given {n} impossible in cell {cellnum}')
                # eliminate other possible values
                for m in chain(range(1,n),range(n+1,len(area)+1)):
                    cellobj.elim(m)
                self._singles_propagate(cellnum,n)
        while self._position_elimination(): pass # use other propagator
        for r in range(self.R):
            ce=self._cells[r*self.C:(r+1)*self.C]
            lambd = lambda cel : '%8s'%(''.join(str(i) for i in range(1,8) if cel.possible(i)))
            print(' '.join(lambd(cel) for cel in ce))
        self._backtrack()
    
    def _backtrack(self):
        ''' Make a guess when constraint propagation fails '''
        # find cell with minimum minimum possibilities and check for completion
        sindex,scell = -1,None
        for i,cell in enumerate(self._cells):
            # scell set to None when finding a cell with > 1 possibility
            if cell.count > 1 and \
                (scell is None or cell.count < scell.count):
                sindex,scell = i,cell
        if scell is None: # every cell.count == 1 (solved)
            # make R*C grid, use only possible value in each cell
            self.solutions.append(
                [ [ [ i for i in range(1,len(self._cells[self.C*r+c].nums)+1)
                      if self._cells[self.C*r+c].possible(i)][0]
                    for c in range(self.C)]
                  for r in range(self.R)] )
            return
        # try possible values
        original_cells = self._cells
        any_solutions = False
        area = self._areas[scell.area]
        for n in range(1,len(area)+1):
            if not scell.possible(n): continue
            self._cells = SolveHakyuu._copy_cells(original_cells)
            newscell = self._cells[sindex] # reference in copied data
            for m in chain(range(1,n),range(n+1,len(area)+1)):
                newscell.elim(m) # eliminate other values
            try:
                self._singles_propagate(sindex,n) # guessed cell propagate
                while self._position_elimination(): pass
                self._backtrack()
                any_solutions = True
            except ContradictionException:
                pass # did not find solution in subtree
        self._cells = original_cells # undo changes to backtrack
        if not any_solutions:
            raise ContradictionException('no solution in this subtree')
    
    def _position_elimination(self):
        '''
        -- If a number has 1 possible position in an area, it must go there --
        Raises ContradictionException if an area has no position for a required
        number
        Returns True if any progress is made, False otherwise
        '''
        changed = False
        for area in self._areas:
            for n in range(1,len(area)+1): # 1..N (N = area size)
                cells = [cell for cell in area if self._cells[cell].possible(n)]
                if len(cells) == 0:
                    raise ContradictionException(
                            f'{n} impossible in area {area}')
                if len(cells) == 1:
                    cellobj = self._cells[cells[0]]
                    if cellobj.count == 1:
                        continue # already set value for this cell
                    for m in chain(range(1,n),range(n+1,len(area)+1)):
                        cellobj.elim(m)
                    # this is where ContradictionException may come from
                    self._singles_propagate(cells[0],n)
                    changed = True
        return changed
    
    def _singles_propagate(self,i,n):
        '''
        -- Cell with 1 possibility must use that number --
        Should only call when the number of possibilities decreases to 1 (or
        during initial setup to handle areas with only 1 cell), otherwise
        recursion may not terminate.
        Raises ContradictionException if a cell reaches 0 possibilities
        Returns True if any possibility information changes, False otherwise
        i = cell index, n = cell value
        '''
        icell = self._cells[i] # convenient reference
        changed = False # are any numbers eliminated from possibilities
        # determine cells along the row/col to eliminate possible values in
        C = self.C # used a lot below
        r,c = divmod(i,C) # cell coordinates
        rmin,rmax = r*C,(r+1)*C # boundaries of the row
        # extend up to n cells away from cell i, staying within the row
        # the min and max ensure the ranges stay on the row
        rowcells = range(max(i-n,rmin),min(i+1+n,rmax))
        colcells = range(max(i-n*C,c),min(i+(n+1)*C,self.R*C),C)
        # loop over the relevant cells in same area/row/col
        for cell in chain(self._areas[icell.area],rowcells,colcells):
            if cell == i: continue # skip self
            cellobj = self._cells[cell]
            if not cellobj.elim(n): continue # information doesnt change
            if cellobj.count == 0:
                raise ContradictionException(f'no nums possible in {cell}')
            if cellobj.count == 1:
                # call _singles_propagate recursively when down to 1 possibility
                celln = [i for i in range(1,len(cellobj.nums)+1)
                         if cellobj.possible(i)][0]
                self._singles_propagate(cell,celln)
            changed = True
        return changed

