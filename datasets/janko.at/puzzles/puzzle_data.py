import os
from bs4 import BeautifulSoup

# scrypt to extract puzzle data from a downloaded copy of janko.at

indir = 'www.janko.at/Raetsel'
outdir = 'puzzle_data'
os.mkdir(outdir)

# relpath excludes indir path
# this is to determine path in the output dir to keep the same structure

# extract the contents of the <script id="data" ..> tag
def processFile(file,relpath):
    global outdir
    bspage = BeautifulSoup(open(file,'r').read(),'html.parser')
    tag = bspage.find(id='data')
    if tag is None: print('no data:',file)
    else:
        name,ext = os.path.splitext(relpath)
        outfile = open(outdir+name+'.txt','w')
        outfile.write(tag.text.strip())
        outfile.write('\n')
        outfile.close()
        print('wrote:',outdir+name+'.txt')

def recursiveExplore(file,relpath):
    global outdir
    _,ext = os.path.splitext(file)
    if os.path.isfile(file): # process .htm and .html files
        if ext in ['.htm','.html']: # html to get data from
            try: processFile(file,relpath)
            except: print('error:',file)
        else: print('skip:',file)
    elif os.path.isdir(file): # explore subdirectory
        try: os.mkdir(outdir+relpath)
        except FileExistsError: print('dir exists:',file)
        for dirfile in sorted(os.listdir(file)):
            recursiveExplore(file+'/'+dirfile,relpath+'/'+dirfile)

assert os.path.isdir(indir)
recursiveExplore(indir,'')
