# sudoku

### todo

- sudoku variants

### features

- square board
- grid of rectangular areas
- equal size areas
- overlapping areas

### board

- size defined by R and C (R > 0, C > 0, dimension of sub blocks)
- grid is a C by R arrangement of sub blocks with total dimension R\*C by R\*C
- each row, column, or block is an area containing R\*C cells
- some cells are filled with numbers

### goals

- assign to each cell an integer in [1,R\*C]

### constraints

1. each area must contain each integer in [1,R\*C]
  - implies that every integer must occur exactly once in each area
  - duplicates --> cannot have each integer

### rules

1. cases: number in a cell
  - a cell may contain a number that does not appear in any area it the cell is
    contained in
  - cell must contain an integer in [1,R\*C] and if it is duplicated in a area,
    then it violates constraint 1
2. cases: number in an area
  - given a number n and an area, n must exist in one of the empty cells
  - if n did not exist in any empty cell, constraint 1 is violated
3. contradiction: no possible number for cell
  - violates constraint 1
4. contradiction: duplicate number in region
  - violates constraint 1
5. basic: last number for a cell
  - rule 3 with only 1 case
6. basic: last position for a number (in a region)
  - rule 2 with only 1 case
