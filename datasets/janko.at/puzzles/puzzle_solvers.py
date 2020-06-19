from itertools import chain

# solver for sudoku, including some extensions to support variants
# some implementation ideas from https://norvig.com/sudoku.html
# TODO custom areas not supported yet
class SolveSudoku:
    
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

