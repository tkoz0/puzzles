# solver for standard sudoku puzzles
class SolveSudoku:
    
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

