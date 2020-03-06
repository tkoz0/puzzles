from bs4 import BeautifulSoup
import os
import sys

# usage: place the Spiele/ dir from the website in the same dir as the py file

# the following is extracted:
# - list of scripts used on each page
# - list of applets used on each page

# this program writes to the files "scripts.txt","applets.txt","filelist.txt",
# "download.txt"

scripts = [] # list of (page_path,[{script_attrs},...])
applets = [] # list of (page_path,[{applet_attrs},...])

dataMap = dict() # directory --> file list (both scripts and applets)

spieleDir = 'Spiele'
#while spieleDir[-1] == '/': spieleDir = spieleDir[:-1]

# recursively searches the file system for html files
def fsSearch(path,depth):
    global scripts,applets,dataMap
    if os.path.isdir(path):
        for file in sorted(os.listdir(path)):
            fsSearch(path+'/'+file,depth+1)
    else:
        assert os.path.isfile(path)
        # html files only, exclude the leaderboard ones (contain "level=")
        if (path.endswith('.html') or path.endswith('.htm')) \
            and not ('level=' in path):
            print(path)
            page = BeautifulSoup(open(path,'rb').read(),'html.parser')
            scriptTags = page.find_all('script')
            appletTags = page.find_all('applet')
            scripts.append((path,[tag.attrs for tag in scriptTags]))
            applets.append((path,[tag.attrs for tag in appletTags]))
            while path[-1] != '/': path = path[:-1]
            if not (path in dataMap): dataMap[path] = set()
            for tag in scriptTags:
                if tag.has_attr('src'): dataMap[path].add(tag['src'])
            for tag in appletTags:
                if tag.has_attr('code'): dataMap[path].add(tag['code'])
                if tag.has_attr('archive'): dataMap[path].add(tag['archive'])

# search all files recursively
fsSearch(spieleDir,0)

# writes a data file in a simple format
def writeData(file,data):
    file = open(file,'w')
    for page,tagAttrList in data:
        if len(tagAttrList) == 0: continue # none found so exclude
        file.write(page+'\n')
        for tagAttr in tagAttrList:
            file.write('    '+str(tagAttr)+'\n')
    file.close()

writeData('scripts.txt',scripts)
writeData('applets.txt',applets)

dataFile = open('filelist.txt','w')
downloadFile = open('download.txt','w')

for dir in sorted(dataMap.keys()):
    dataFile.write(dir+'\n')
    if len(dataMap[dir]) > 0:
        for file in sorted(dataMap[dir]):
            dataFile.write('    '+file+'\n')
            if file.startswith('http'): downloadFile.write(file+'\n')
            else:
                downloadFile.write('https://www.janko.at/'+dir+file+'\n')

dataFile.close()
downloadFile.close()
