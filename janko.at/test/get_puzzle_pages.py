from bs4 import BeautifulSoup
from selenium import webdriver
import sys
import os

puzBaseUrl = 'https://www.janko.at/Raetsel/'
driver = webdriver.Firefox()

outNoFile = open('puzzle_pages_error.txt','w')
outYesFile = open('puzzle_pages_lists.txt','w')

def getPageLinks(base_page):
    puzElement = base_page.find(id='index-1')
    if not puzElement: # cannot extract
        return None
    else: # find href of all a tags
        links = [x['href'] for x in puzElement.find_all('a')]
        return None if links == [] else links

for line in open('puzzle_bases.txt'): # each line should have a url

    sys.stderr.write(line)
    # sanity checks, extract puzzle name
    assert line.startswith(puzBaseUrl)
    # this assertion may not be appropriate
    assert line.endswith('/index.htm\n')
    puzName = line[len(puzBaseUrl):-1]
    i = len(puzName)-1 # start at end, find /
    while i >= 0 and puzName[i] != '/': i -= 1
    assert i != -1
    assert puzName[i:] == '/index.htm'
    puzName = puzName[:i]
    puzName = puzName[:i] # note, may contain a /
    sys.stderr.write('downloading '+puzName+'\n')
    
    # load page and extract the urls
    driver.get(line[:-1])
    bs4page = BeautifulSoup(driver.page_source,'html.parser')
    links = getPageLinks(bs4page)
    if links:
        outYesFile.write('begin %s\n'%puzName)
        for url in links:
            outYesFile.write(url+'\n')
        outYesFile.write('end %s\n'%puzName)
    else: outNoFile.write(line)

driver.quit()
