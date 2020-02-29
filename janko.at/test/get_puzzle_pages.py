from bs4 import BeautifulSoup
from selenium import webdriver
import sys
import os

puzBaseUrl = 'https://www.janko.at/Raetsel/'
driver = webdriver.Firefox()

outNoFile = open('puzzle_pages_error.txt','w')
outYesFile = open('puzzle_pages_lists.txt','w')

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
    # should be a div with a list of all the puzzles
    puzElement = bs4page.find(id='index-1')
    
    if not puzElement: # cannot find link list to extract
        outNoFile.write(line)
    else: # collect all puzzle links
        puzLinks = [x['href'] for x in puzElement.find_all('a')]
        outYesFile.write('base_url %s\n'%puzName)
        for url in puzLinks:
            outYesFile.write('page_url %s\n'%url)

driver.quit()
