import os

# groups the subdirectories of puzzle_data/ into 3:
# - done (successful conversion to json, when output.success file is present)
# - not done (directory was skipped or json parsing failed)
# - no txts (no puzzles available or it isnt the desired type of puzzle)

def hasTxt(files):
    for f in files:
        if f.endswith('.txt'): return True
    return False

results = [] # list of (status,dir)

def explore(path):
    global results
    if not os.path.isdir(path): return
    files = os.listdir(path)
    if hasTxt(files): # has puzzle data, show status
        if os.path.isfile(path+'/output.ignore'):
            results.append(('ignore',path))
        else:
            done = os.path.isfile(path+'/output.success')
            results.append(('done' if done else 'notdone',path))
    else: results.append(('notxt',path))
    for f in sorted(files):
        explore(path+'/'+f)

explore('puzzle_data')

done = [x[1] for x in results if x[0] == 'done']
notdone = [x[1] for x in results if x[0] == 'notdone']
notxt = [x[1] for x in results if x[0] == 'notxt']
ignore = [x[1] for x in results if x[0] == 'ignore']

print('-- DONE --')
for dir in done: print(dir)
print()
print('-- NO TXT --')
for dir in notxt: print(dir)
print()
print('-- IGNORED --')
for dir in ignore: print(dir)
print()
print('-- NOT DONE --')
for dir in notdone: print(dir)
print()
