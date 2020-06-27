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
    
    Member variables (meant for external access):
    - self.N = grid side length parameter
    - self.solutions = list of solution grids found (N*N array of integers 1..N)
    Member variables (meant to be internal):
    - self._cells[i] = _Cell object at (row,col) = (i//N,i%N)
    - self._areas[i] = list of N cells (by index) in area i
    - self._areasof[i] = list of areas (by index) containing cell i
    Read only variables (after initialization): _areas, _areasof
    
    TODO: support a max solutions limit and terminate recursion after that
    TODO: support variants with nonstandard shapes (not a square)
    TODO (maybe): add completed numbers information for each area so that the
    positional elimination propagator can stop if n was already narrowed to 1
    cell in the area
    TODO (maybe): track change history for recursion instead of copying the grid
    before making a guess
    '''
    
    class _Cell:
        '''
        A representation of possible values for a cell during the solving
        process as possibilities get eliminated.
        Member variables:
        self.nums[n] = is N a possible value in this cell
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
        self._solve(problem)
    
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
    1. pick a cell with 2 (or minimum) possible numbers remaining
    2. for each possible number, assign it and propagate information so it is
    eliminated from possibilities of cells in the same area, then call the
    position elimination reasoning until it makes no progress
    3. if no solution is found, call _backtrack() recursively
    4. after the loop, backtrack (remove the guessed number) (this can be
    skipped if a 2nd solution is found)
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
                if cellobj.count == 1: # value already set
                    if not cellobj.possible(n):
                        raise ContradictionException(
                                f'cannot put given {n} in cell {cellnum}')
                    continue
                # multiple possibilities, eliminate others
                for m in chain(range(1,n),range(n+1,self.N+1)):
                    cellobj.elim(m)
                # should be able to remove this assert
                assert cellobj.count == 1 and cellobj.possible(n)
                try:
                    self._singles_propagate(cellnum,n)
                except ContradictionException:
                    return # cannot solve
        try:
            # repeat position elimination until no progress
            while self._position_elimination(): pass
            # proceed to backtracking (which initially checks if it is solved)
            self._backtrack()
        except ContradictionException:
            pass # cannot solve
    
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
            # should be able to remove this assert
            assert newscell.count == 1 and newscell.possible(n)
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
                    # should be able to remove this assert
                    assert cellobj.count == 1 and cellobj.possible(n)
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
        Returns True if any informatino changes, False if nothing changes
        i = cell index, n = cell value
        '''
        icell = self._cells[i] # shorter reference to it
        # should be able to remove this assert
        assert icell.count == 1 and icell.possible(n)
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

