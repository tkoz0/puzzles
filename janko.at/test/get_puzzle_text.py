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

# try to load list of links which the scraper couldnt find puzzle data
try:
    unsupFiles = set(line[:-1] for line in
                     open('puzzle_text_unsupported.txt','r'))
except:
    unsupFiles = set()
unsupOutput = open('puzzle_text_unsupported.txt','a',1)

driver = webdriver.Firefox()
driver_refreshes = 0
def getPageBs4(url):
    global driver,driver_refreshes
    if driver_refreshes >= 300:
        driver.close()
        driver = webdriver.Firefox()
        driver_refreshes = 0
    driver_refreshes += 1
    # try up to 5 times to download page
    successful = False
    for _ in range(5):
        try:
            driver.get(url)
            successful = True
            break
        except:
            continue
    return BeautifulSoup(driver.page_source,'html.parser') \
           if successful else None

def extractData(page,fdir,puz):
    global driver,puzBaseUrl,unsupFiles,unsupOutput
    assert page.endswith('.htm')
    fileName = page[:-4]+'.txt'
    print('download started: %s'%(puz+'/'+page))
    if os.path.isfile(fdir+fileName):
        print('- already downloaded')
        return
    elif (puz+'/'+page) in unsupFiles:
        print('- page unsupported')
        return
    bs4page = getPageBs4(puzBaseUrl+puz+'/'+page)
    if not bs4page:
        print('- download failed')
        return
    data = bs4page.find(id='data')
    if data: # found data, take contents
        outFile = open(fdir+fileName,'w')
        outFile.write(data.decode_contents())
        outFile.close()
        print('- successfully saved to: %s'%(fdir+fileName))
    else: # expect a page listing many puzzles
        unsupOutput.write(puz+'/'+page+'\n')
        unsupFiles.add(puz+'/'+page)
        print('- download unsupported')

for puz in sorted(linkData.keys()):
    makeDir('puzzles/'+puz+'/') # make dir to story files
    for page in sorted(linkData[puz]):
        extractData(page,'puzzles/'+puz+'/',puz)

driver.close()
