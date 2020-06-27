'''
Python3 scrypt for extracting the puzzle data from janko.at webpages and storing
them in txt files. Having the txt files in a middle step allows for editing them
in the case that there are formatting issues that complicates parsing them.

Usage: python3 htm2txt.py <input_dir> <output_dir>
Notes: does not recurse into subdirectories, input_dir/a.htm -> output_dir/a.txt
'''

if __name__ != '__main__': quit()

import os,sys
from bs4 import BeautifulSoup

input_dir = os.path.normpath(sys.argv[1])
output_dir = os.path.normpath(sys.argv[2])

assert os.path.isdir(input_dir)

if not os.path.isdir(output_dir):
    os.mkdir(output_dir)

assert os.path.isdir(output_dir)

files = os.listdir(input_dir)

# loop assumes nothing will go wrong with disk IO

count = 0
for file in sorted(files):
    count += 1
    infile = input_dir+'/'+file
    name,ext = os.path.splitext(file)
    if ext != '.htm': continue
    outfile = output_dir+'/'+name+'.txt'
    if os.path.isfile(outfile):
        print('already processed: %s (%d/%d files)'%(infile,count,len(files)))
        continue
    bs4page = BeautifulSoup(open(infile,'r').read(),'html.parser')
    datatag = bs4page.find(id='data')
    if datatag is None:
        print('ERROR cannot find data tag in: %s (%d/%d files)'
                %(infile,count,len(files)))
        continue
    lines = datatag.text.strip().splitlines()
    outfileobj = open(outfile,'w')
    for line in lines:
        outfileobj.write(line+'\n')
    outfileobj.close()
    print('success: %s -> %s (%d/%d files)'%(infile,outfile,count,len(files)))

