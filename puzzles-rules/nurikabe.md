# nurikabe

### todo

- clean up rules
- non-rectangular boards?

### features

- connectedness (orthogonal)

### board

- R by C grid
- some cells contain numbers
- numbered cells are white

### goals

- assign a color (black or white) to each cell not containing a number

### constraints

1. every orthogonally connected area of white (island) contains exactly 1 number
2. the number of cells in each island is equal to its number
3. all black cells form an orthogonally connected area
4. no 2x2 block of cells is completely black

### rules

1. cases: cell color
  - a cell not containing a number may by black or white
2. contradiction: enclosed island without a number
  - violates constraint 1
3. contradiction: island contains multiple numbers
  - violates constraint 1
4. contradiction: enclosed island too small (or cant expand to be large enough)
  - violates constraint 2
5. contradiction: island too large
  - violates constraint 2
6. contradiction: 2 black cells cannot be connected (by black)
  - violates constraint 3
7. contradiction: 2x2 block of black cells
  - violates constraint 4
8. basic: area surrounded by black not containing a number must be black
  - if any were white, it would lead to contradiction 2
9. basic: white bottleneck
  - if an island (white area) is unnumbered or too small for its number, and is
    surrounded by black or board edge except at 1 edge, then the cell next to
    its open edge must be white
  - the cell at the opening is either black or white, black leads to either
    contradiction 2 or 4
10. basic: black between regions
  - cells adjacent to a region are either black or white
  - they must be black if contradictions 3 or 5 arise
11. basic: close a properly sized island
  - bordering cells must be black or white, white leads to contradiction 5
12. basic: corner black
  - island with 1 open corner needing 1 more white must have black diagonally
    from this corner
  - this cell must be black or white, white would lead to contradiction 5
13. basic: black bottleneck
  - black area with 1 open edge, must have black next to that open edge
  - the bordering cell must be black or white, white leads to contradiction 6
  - this applies when there exists another disconnected black cell
14. basic: area surrounded by white must be white
  - if a black was contained, it would lead to contradiction 6
  - requires that there is a black cell outside of the white border
15. basic: avoid 2x2 black pool
  - if 3 of the cells in a 2x2 area are black, the last one must be white
  - last cell is either black or white, black leads to contradiction 7
16. basic: unreachable cell
  - cell must be black if no numbered islands can be extended to it with white
    cells (using shortest path)
  - if it is white, then it must extend to a numbered island, so this rule
    applies if all shortest path extensions lead to contradiction 5
17. contradiction: unnumbered island cannot extend to numbered island (using any
    shortest path)
  - in all cases, contradiction 2 or 5 arises
18. cases: an island that is too small or unnumbered must have a white cell next
    to one of its edges
  - if all cells bordering the edge were black, then contradiction 2 or 4
19. cases: an area of black must have a black cell at one of its edges
  - applies when another disconnected area of black exists
  - if all cells around the edge were white, then contradiction 6
20. basic: if an area containing 1 number is surrounded by black and the size is
    equal to the number, fill the area with white
  - if any of the cells were black, contradiction 4 arises
21. contradiction: numbered island is constrained by black and cells adjacent to
    other numbered islands
  - cannot expand to become large enough
