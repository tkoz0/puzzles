from bs4 import BeautifulSoup
from selenium import webdriver
import os

puzBaseUrl = 'https://www.janko.at/Raetsel/'

# creates directory from path
def makeDir(path):
    path = path.split('/')
    for i in range(1,len(path)):
        if not os.path.isdir('/'.join(path[:i])):
            os.mkdir('/'.join(path[:i]))

# build a dict mapping puzzle name to link names
inFile = open('puzzle_pages_lists.txt','r')
currentPuzzle = None
linkData = dict()
for line in inFile:
    if line.startswith('begin '):
        assert not currentPuzzle
        currentPuzzle = line[6:-1]
        assert not (currentPuzzle in linkData)
        linkData[currentPuzzle] = set()
    elif line.startswith('end '):
        assert line[4:-1] == currentPuzzle
        currentPuzzle = None
    else:
        assert currentPuzzle in linkData
        linkData[currentPuzzle].add(line[:-1])

driver = webdriver.Firefox()

def extractData(page,fdir,puz):
    assert page.endswith('.htm')
    fileName = page[:-4]+'.txt'
    if os.path.isfile(fdir+fileName):
        print('already downloaded: %s'%(fdir+fileName))
        return # already downloaded
    global driver,puzBaseUrl
    driver.get(puzBaseUrl+puz+'/'+page)
    bs4page = BeautifulSoup(driver.page_source,'html.parser')
    data = bs4page.find(id='data')
    if data: # found data, take contents
        outFile = open(fdir+fileName,'w')
        outFile.write(data.decode_contents())
        outFile.close()
        print('successfully downloaded: %s'%(fdir+fileName))
    else: # expect a page listing many puzzles
        print('download unsupported: %s'%(fdir+fileName))

for puz in linkData.keys():
    makeDir('puzzles/'+puz+'/') # make dir to story files
    for page in linkData[puz]:
        extractData(page,'puzzles/'+puz+'/',puz)

driver.close()
