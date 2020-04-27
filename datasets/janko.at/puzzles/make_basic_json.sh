#!/bin/bash

# fix errors in txt files (straight from the <script id="data" ..> tags)
python3 puzzle_fixes.py puzzle_data/Heyawake Heyawake
python3 puzzle_fixes.py puzzle_data/Fillomino Fillomino
python3 puzzle_fixes.py puzzle_data/LITS LITS
python3 puzzle_fixes.py puzzle_data/Nurikabe Nurikabe

# convert the txt files into bulk basic json files
python3 puzzle_json.py puzzle_data/Sudoku Sudoku
python3 puzzle_json.py puzzle_data/Heyawake Heyawake
python3 puzzle_json.py puzzle_data/Akari Akari
python3 puzzle_json.py puzzle_data/Fillomino Fillomino
python3 puzzle_json.py puzzle_data/LITS LITS
python3 puzzle_json.py puzzle_data/Nurikabe Nurikabe
python3 puzzle_json.py puzzle_data/Slitherlink Slitherlink
