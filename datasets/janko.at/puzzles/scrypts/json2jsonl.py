'''
Python3 scrypt to combine individual JSON puzzle files into one JSONL file
(storing 1 valid JSON object per line).

Usage: python3 json2jsonl.py <input_dir> <output_file>

Files will be processed in sorted order. Does not recurse to subdirectories.
'''

if __name__ != '__main__': quit()

import os,sys,json

input_dir = os.path.normpath(sys.argv[1])
output_file = os.path.normpath(sys.argv[2])
assert os.path.isdir(input_dir)
output_file = open(output_file,'w')
files = os.listdir(input_dir)

count = 0
for file in sorted(files):
    name,ext = os.path.splitext(file)
    if ext != '.json': continue
    print('processing:',file)
    data = json.loads(open(input_dir+'/'+file,'r').read())
    output_file.write(json.dumps(data,separators=(',',':')))
    output_file.write('\n')

output_file.close()

