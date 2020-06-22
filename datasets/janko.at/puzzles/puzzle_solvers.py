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
    
    Solving will set self.solution to a N*N array of integers, or leave it as
    None if there is no solution. Additionally, self.ambiguous is set to true if
    multiple solutions are found, False otherwise.
    
    Member variables (meant for external access):
    - self.N = grid side length parameter
    - self.solution = first solution grid found (N*N array of integers 1..N)
    - self.ambiguous = True if a 2nd solution is found
    Member variables (meant to be internal):
    - self._cells[i] = _Cell object at (row,col) = (i//N,i%N)
    - self._areas[i] = list of N cells (by index) in area i
    - self._areasof[i] = list of areas (by index) containing cell i
    Read only variables (after initialization): _areas, _areasof
    
    TODO: support variants with nonstandard shapes (not a square)
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
        self.solution = None
        self.ambiguous = False
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
#DEBUG                print(f'assigning given {n} to cell {cellnum}')
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
                # may raise ContradictionException
                self._singles_propagate(cellnum,n)
        # repeat position elimination until no progress
        while self._position_elimination(): pass
        
        # TODO enabled backtracking
    
    def _backtrack(self):
        ''' Make a guess when logic strategies do not solve it '''
    
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
        # should be able to remove these asserts
        assert icell.count == 1
        assert icell.possible(n)
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





# solver for sudoku, including some extensions to support variants
# some implementation ideas from https://norvig.com/sudoku.html
# TODO custom areas not supported yet
class __Old2__SolveSudoku:
    
    # represents a structure for solving, which numbers are possible
    # TODO might be better without bookkeeping for self.count (unsure)
    class _Cell:
        
        def __init__(self,N):
            self.nums = [True]*N # represents 1,2,..,N indexed as 0,1,..,N-1
            self.count = N # how many are possible
        
        # is n possible in this cell
        def possible(self,n):
            return self.nums[n-1]
        
        # eliminate value, return True on success
        def elim(self,n):
            n -= 1 # offset by 1
            if self.nums[n]:
                self.nums[n] = False
                self.count -= 1
                return True
            return False
        
        # undo previous elimination, return True on success (not used currently)
        def undo(self,n):
            n -= 1 # offset by 1
            if not self.nums[n]:
                self.nums[n] = True
                self.count += 1
                return True
            return False
    
    # solving grid representation: N*N length list of cells (as defined above)
    # maintain a list of areas (the areas that must contain 1..N)
    # rows/cols need not be stored, they can be computed easily
    # variables:
    # self.givens = original provided grid (copied), 0 = empty, 1..N = filled
    # self.areas = original provided areas
    # self.N = side length (in cells) of the puzzle
    # self._grid[i] = _Cell object at position (i//N,i%N)
    # self._areas[i] = list of N cells (by index), constrained to contain 1..N
    # self._areasof[i] = list of areas (by index) containing cell i
    # self.solution = first solution grid found (N*N array of 1..N)
    
    # __init__ parameters (raises AssertionError for invalid arguments)
    # grid = N*N array of givens (0 = empty, 1..N = filled)
    # areas =
    #    None = latin square
    #    (br,bc) = dimensions of rectangular blocks, must have br*bc==N
    #    N*N array = each cell contains a symbol for which area it belongs to
    #        (each area must contain N cells)
    # diagonals = whether to add areas requiring the diagonals to contain 1..N
    # otherareas = list of areas in same format for
    def __init__(self,grid,areas=None,diagonals=False,otherareas=None):
        
        # check dimensions and data types, copy grid of the givens (clues)
        N = len(grid)
        self.N = N
        assert N > 0 and SolveSudoku._check_grid(grid,N)
        self.givens = [row[:] for row in grid] # copy
        self.solution = None # for storing solution
        self.multiple_solutions = False
        
        # determine what to do with areas based on type, create grid_areas var
        if areas is None: # latin square
            grid_areas = []
        elif type(areas[0]) == int: # rectangular blocks
            br,bc = areas # should be length 2 iterable of ints
            assert type(bc) == int # type(br)==int was already checked
            assert br >= 1 and bc >= 1 and br*bc == N # validity
            if br > 1 and bc > 1:
                grid_areas = SolveSudoku._rect_areas(N,br,bc)
            else:
                grid_areas = [] # will be same as the rows or columns
        else: # provided areas
            grid_areas = SolveSudoku._get_areas(areas,N)
            assert grid_areas is not None
        
        # make structures for solving procedure
        # cell (r,c) at index N*r+c, initially all values allowed
        self._grid = [SolveSudoku._Cell(N) for _ in range(N*N)]
        self._areas = []
        # areas are the rows, cols, areas (if any), and possibly more below
        self._areas += [list(range(N*i,N*i+N)) for i in range(N)] # rows
        self._areas += [list(range(i,N*N,N)) for i in range(N)] # cols
        self._areas += grid_areas
        
        # additional areas that must conatin 1..N
        if diagonals and N > 1: # N>1 prevents fail in corner case
            self._areas += list(range(0,N*N,N+1)) # 0,N+1,..,N*N-1
            self._areas += list(range(N-1,N*N-1,N-1)) # N-1,2*N-2,...,(N-1)*N
        if otherareas is not None:
            assert 0 # TODO not supported yet
        
        # create mapping of cell to areas containing it
        self._areasof = [[] for _ in range(N*N)]
        for i,area in enumerate(self._areas):
            for cell in area:
                self._areasof[cell].append(i)
    
    # check basic grid validity (N*N and contains integers 0..N)
    def _check_grid(grid,N):
        if len(grid) != N:
            return False
        for row in grid:
            if len(row) != N:
                return False
            for value in row:
                if type(value) != int or value < 0 or value > N:
                    return False
        return True
    
    # checks area validity and returns them as a list
    # should provide a N*N array with symbols (can be any hashable type)
    # there should be N symbols and N instances of each
    # result is a list of N areas (each a list of N cell indexes)
    def _get_areas(areas,N):
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
    
    # creates lists of cells for standard rectangular areas
    # done by list comprehension with indexing the cells
    def _rect_areas(N,br,bc):
        assert br > 1 and bc > 1 and br*bc == N
        return [sum([list(range(N*r+c*bc,N*r+c*bc+bc)) # cols in the block
                     for r in range(r*br,r*br+br)],[]) # rows in the block
                for r in range(bc) for c in range(br)] # for each block
    
    def solve(self):
        self.solution = None
        self.multiple_solutions = False
        cell = 0
        # assign given cell values
        for r in range(self.N):
            for c in range(self.N):
                n = self.givens[r][c]
                if n != 0 and not self._cell_assign(cell,n):
                    return False # contradiction on assignment
                cell += 1
        return self._backtracker()
    
    def _backtracker(self):
        if self.multiple_solutions: return False # dont find all solutions
        if not self._propagate():
            return False # propagation leads to contradiction
        if self._uncertain_cells() == 0:
            if self.solution is None:
                self._set_solution()
            else:
                self.multiple_solutions = True
            return True
        return False#TODO temp debug
        count,cell = min(((c.count,c) for c in self._grid))
        any_solutions = False
        original_grid = self._grid # save original grid for backtracking
        for n in range(1,self.N+1):
            self._grid = SolveSudoku.grid_copy(original_grid,self.N)
            if self._backtracker():
                any_solutions = True
        self._grid = original_grid
    
    def grid_copy(grid,N):
        newgrid = []
        for cell in grid:
            newcell = SolveSudoku._Cell(N)
            newcell.nums = cell.nums[:]
            newcell.count = cell.count
            newgrid.append(newcell)
        return newgrid
    
    # TODO this method has issues and infinite loops
    def _propagate(self):
        assignment = True
        while assignment:
            assignment = False # was any value was deduced on this iteration
            # only possible value for cell
            for cell in range(self.N*self.N):
                cellobj = self._grid[cell]
                if cellobj.count == 1:
                    assignment = True
                    n = 0
                    for i in range(1,self.N+1):
                        if cellobj.possible(i):
                            n = i
                            break
                    if not self._cell_assign(cell,n):
                        return False
            # areas having number with only 1 possible cell
            for area,areacells in enumerate(self._areas):
                break#TODO tmp
                for n in range(1,self.N+1):
                    cells = [cell for cell in areacells
                             if self._grid[cell].possible(n)]
                    if len(cells) == 0:
                        return False # no cell for n in this area
                    # if n was not already 
                    # place n where it must go, return False if contradiction
                    if len(cells) == 1:
                        assignment = True
                        if not self._cell_assign(cells[0],n):
                            return False
    
    def _cell_assign(self,cell,n):
        cellobj = self._grid[cell]
        if not cellobj.possible(n):
            return False # cannot assign n to this cell
        for i in chain(range(1,n),range(n+1,self.N+1)):
            cellobj.elim(i)
        for area in self._areasof[cell]:
            for othercell in self._areas[area]:
                if othercell == cell: continue
                othercellobj = self._grid[othercell]
                othercellobj.elim(n)
                if othercellobj.count == 0:
                    return False # no possible value contradiction
        return True
    
    # counts how many cells are uncertain
    # assume possible value count never gets to zero for cells
    # ending with contradiction when possible value count reaches 0 is done for
    # performance reasons
    def _uncertain_cells(self):
        return sum(cell.count > 1 for cell in self._grid)
    
    # creates solution from self._grid (assumes no cells are uncertain)
    def _set_solution(self):
        self.solution = [ [ [ i for i in range(self.N) # take the 1 possibility
                              if self._grid[r*self.N+c].possible(i)][0]
                            for c in range(self.N)]
                          for r in range(self.N)]
    
    
    ########### TODO _some_ of below might be scrapped ##########
    
    # solving method: begin with constraint propagation
    # when a cell c is assigned a number n:
    # - n must be a possible value in c
    # - n is no longer possible in cells sharing an area with c
    # - cells sharing an area could possibly be reduced to 1 possible value
    # - units containing c may have a number with fewer possible positions
    # when a guess needs to be made, options are:
    # - pick a cell with 2 (or smallest) possible values
    # - pick an area and number with 2 (or smallest) possible positions
    
    # main solver function, fails if no solution or multiple solutions
    def solve_old(self):
        self.solution = None
        # visited array for the DFS of _set_cell() so recursion is well defined
        # when a cell is set, its information is propagated to affected cells
        # this process does not need to be repeated, if more information will
        # deduce cell values, it will come from assigning a value to a new cell
        self._visited = [False]*(self.N**2)
        # fill in the given cells
        for cell in range(self.N**2):
            n = self.givens[cell//self.N][cell%self.N]
            if n == 0: continue # empty
            if not self._set_cell(cell,n):
                return False # contradiction with given
        remaining = sum(cell.count > 1 for cell in self._grid)
        if remaining == 0:
            self._set_solution() # generates the solution from self._grid
            return True
        else:
            return False # TODO use backtrack+propagate solver
    
    # set cell value and remove it from allowed values in same area cells
    # returns False if a contradiction is found
    def _set_cell(self,cell,n):
        cellobj = self._grid[cell]
        if not cellobj.possible(n):
            return False # assignment not possible
#        if not self.tmp[cell]:#TODO tmp remove
#            self.tmp2+=1;print('%02d'%self.tmp2,'[%d,%d] ->'%divmod(cell,self.N),n);self.tmp[cell]=True
        # already called _set_cell() during the current propagation
        if self._visited[cell]:
            return True
        self._visited[cell] = True # avoid visiting 2nd time so recursion ends
        
        # remove other numbers from current cell possibilities
        for i in chain(range(1,n),range(n+1,self.N+1)):
            cellobj.elim(i)
        # keep track of areas that might be affected by the number assignment
        # (every area containing a cell that gets updated by propagation)
        affected_areas = [False]*len(self._areas)
        # cannot put same number in same area cells, propagate this information
        for area in self._areasof[cell]:
            for other in self._areas[area]:
                # add areas whose available possibility information changes
                for otherarea in self._areasof[other]:
                    affected_areas[otherarea] = True
                if other == cell: continue
                othercell = self._grid[other]
                if not othercell.elim(n):
                    continue # do not recurse on cell if no information changes
                if othercell.count == 0:
                    return False # no possible values is a contradiction
                if othercell.count == 1:
                    # recursively set the must have value for a cell
                    values = [i for i in range(1,self.N+1)
                                 if othercell.possible(i)]
                    if not self._set_cell(other,values[0]):
                        return False
        for area,affected in enumerate(affected_areas):
            if affected and not self._area_helper(area):
                return False
        return True # no contradiction
    
    # find numbers that only have 1 possible position and assign them
    # returns False if a contradiction is found
    def _area_helper(self,area):
        for n in range(1,self.N+1):
            cells = [cell for cell in self._areas[area]
                       if self._grid[cell].possible(n)]
            if len(cells) == 0:
                return False # no cell for n in this area
            # if n was not already 
            # place n where it must go, return False if contradiction is found
            if len(cells) == 1 and not self._set_cell(cells[0],n):
                return False
        return True # no contradiction




# solver for standard sudoku puzzles
class __Old__SolveSudoku:
    
    # standard sudoku is defined by a grid containing numbers 0..N, 0 for empty
    # br and bc are for the block dimensions, note that br*bc == N
    def __init__(self,grid,br,bc):
        self.grid = [r[:] for r in grid]
        self.br = br
        self.bc = bc
        self.N = br*bc
        self.solution = None
        self._emptycells = []
        self._checkValidity()
    
    # asserts validity of grid state (possibly unsolved)
    def _checkValidity(self):
        assert self.br > 0 and self.bc > 0
        assert len(self.grid) == self.N
        # check rows length and no duplicates
        for r in range(self.N):
            assert len(self.grid[r]) == self.N
            nums = [False]*(self.N+1)
            for n in self.grid[r]:
                if n == 0: continue
                assert not nums[n]
                nums[n] = True
        # check cols for no duplicates
        for c in range(self.N):
            nums = [False]*(self.N+1)
            for r in range(self.N):
                if self.grid[r][c] == 0: continue
                assert not nums[self.grid[r][c]]
                nums[self.grid[r][c]] = True
        # check blocks for no duplicates
        for bri in range(self.bc):
            for bci in range(self.br):
                nums = [False]*(self.N+1)
                for r in range(bri*self.br,(bri+1)*self.br):
                    for c in range(bci*self.bc,(bci+1)*self.bc):
                        if self.grid[r][c] == 0: continue
                        assert not nums[self.grid[r][c]]
                        nums[self.grid[r][c]] = True
    
    # backtracking helper, searches for all solutions
    def _backtrack(self,i):
        if i == len(self._emptycells):
            assert self.solution is None
            self.solution = [r[:] for r in self.grid]
        else:
            r,c = self._emptycells[i]
            nums = [True]*(1+self.N)
            # find numbers that are not allowed in this cell
            for n in self.grid[r]:
                nums[n] = False
            for rr in range(self.N):
                nums[self.grid[rr][c]] = False
            br,bc = r-(r%self.br),c-(c%self.bc)
            for rr in range(br,br+self.br):
                for cc in range(bc,bc+self.bc):
                    nums[self.grid[rr][cc]] = False
            for n in range(1,1+self.N):
                if nums[n]:
                    self.grid[r][c] = n
                    self._backtrack(i+1)
                    self.grid[r][c] = 0
    
    # solve with backtracking, fails if more than 1 solution
    def solveBacktrack(self):
        self.solution = None
        if len(self._emptycells) == 0:
            for r in range(self.N):
                for c in range(self.N):
                    if self.grid[r][c] == 0:
                        self._emptycells.append((r,c))
        self._backtrack(0)
        assert self.solution is not None

