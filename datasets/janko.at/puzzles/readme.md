
# Logic Puzzles JSON Schema

Each .jsonl file contains 1 JSON object per line. Each JSON object contains the
following keys:

| Key          | Description                                            |
| ------------ | ------------------------------------------------------ |
| \_\_file\_\_ | filename                                               |
| \_\_data\_\_ | JSON representation of the original data from janko.at |
| puzzle       | type of logic puzzle                                   |

They also contain other keys that specify the puzzle. See below for details.

TODO: include last update time and number of puzzles included

### Sudoku

Given a N*N grid with some numbers provided. Fill the empty cells such that each
row, column, and rectangular block contains each number in [1,N]. The diagonals
option additionally requires that each diagonal contains each number in [1,N].
The block dimensions are specified by "blockrows" and "blockcols" and they must
multiply to N.

| Key       | Description                              |
| --------- | ---------------------------------------- |
| puzzle    | "sudoku" or "sudoku,diagonals"           |
| problem   | N\*N grid of given integers, 0 for empty |
| blockrows | number of rows per block                 |
| blockcols | number of columns per block              |
| solution  | N\*N grid of integers in [1,N]           |

### Hakyuu (Ripple Effect)

Given a R*C grid with some numbers provided. Fill in empty cells such that each
area of size N contains each number in [1,N]. If a number M occurs twice in a
row or column, there must be at least M cells of separation between them.

| Key      | Description                                     |
| ---------| ----------------------------------------------- |
| puzzle   | "hakyuu"                                        |
| problem  | R\*C grid of given integers, 0 for empty        |
| areas    | R\*C grid of integers, each identifying an area |
| solution | R\*C grid of integers in [1,N]                  |
