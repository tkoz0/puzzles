#!/bin/bash

# fix errors in txt files (straight from the <script id="data" ..> tags)
python3 puzzle_fixes.py puzzle_fixes.txt

# convert the txt files into bulk basic json files
python3 puzzle_json.py Abc-End-View
python3 puzzle_json.py Abc-Kombi
python3 puzzle_json.py Abc-Pfad
python3 puzzle_json.py Akari
python3 puzzle_json.py Fillomino
python3 puzzle_json.py Heyawake
python3 puzzle_json.py LITS
python3 puzzle_json.py Nurikabe
python3 puzzle_json.py Slitherlink
python3 puzzle_json.py Sikaku
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
python3 puzzle_json.py Suguru
python3 puzzle_json.py Sukoro
python3 puzzle_json.py Sukrokuro
python3 puzzle_json.py Sumdoku
python3 puzzle_json.py Suraromu
python3 puzzle_json.py Usoone
python3 puzzle_json.py Usotatami
python3 puzzle_json.py Vier-Winde
python3 puzzle_json.py View
python3 puzzle_json.py Wolkenkratzer
python3 puzzle_json.py Wolkenkratzer-2
python3 puzzle_json.py Yagit
python3 puzzle_json.py Yajilin
python3 puzzle_json.py Yajisan-Kazusan
python3 puzzle_json.py Yakuso
python3 puzzle_json.py Yin-Yang
python3 puzzle_json.py Yonmasu
python3 puzzle_json.py Yosenabe
python3 puzzle_json.py Zahlenkreuz
python3 puzzle_json.py Zahlenlabyrinth
python3 puzzle_json.py Zahlenschlange
python3 puzzle_json.py Zehnergitter
python3 puzzle_json.py Zeltlager
python3 puzzle_json.py Zeltlager-2
python3 puzzle_json.py Ziegelmauer
python3 puzzle_json.py Zipline

# puzzles to ignore, such as language based puzzles

# special variants, provided as images
touch puzzle_data/Varianten/output.ignore
# language based
touch puzzle_data/Zitatemix/output.ignore
