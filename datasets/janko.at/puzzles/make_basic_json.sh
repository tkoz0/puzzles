#!/bin/bash

# fix errors in txt files (straight from the <script id="data" ..> tags)
python3 puzzle_fixes.py Fillomino
python3 puzzle_fixes.py Heyawake
python3 puzzle_fixes.py LITS
python3 puzzle_fixes.py Nurikabe

# convert the txt files into bulk basic json files
python3 puzzle_json.py Akari
python3 puzzle_json.py Fillomino
python3 puzzle_json.py Heyawake
python3 puzzle_json.py LITS
python3 puzzle_json.py Nurikabe
python3 puzzle_json.py Slitherlink
python3 puzzle_json.py Sudoku
python3 puzzle_json.py Sudoku/2D
python3 puzzle_json.py Sudoku/Butterfly
python3 puzzle_json.py Sudoku/Chaos
python3 puzzle_json.py Sudoku/Clueless-1
python3 puzzle_json.py Sudoku/Clueless-2
python3 puzzle_json.py Sudoku/Flower
python3 puzzle_json.py Sudoku/Gattai-8
python3 puzzle_json.py Sudoku/Samurai
python3 puzzle_json.py Sudoku/Shogun
python3 puzzle_json.py Sudoku/Sohei
python3 puzzle_json.py Sudoku/Sumo
python3 puzzle_json.py Sudoku/Windmill
