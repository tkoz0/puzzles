from bs4 import BeautifulSoup
from selenium import webdriver

puzBaseUrl = 'https://www.janko.at/Raetsel/'

# page in the iframe on the main page, displaying the full puzzle list
puzHomeUrl = puzBaseUrl + 'index-3.htm'

# grab the page content and use BeautifulSoup
driver = webdriver.Firefox()
driver.get(puzHomeUrl)
bs4page = BeautifulSoup(driver.page_source,'html.parser')
driver.quit()
# get divs that contain puzzle main page urls
puzGroups = bs4page.find_all('div',class_='index-c')

# get all the puzzle main page urls
# only interested in group indexes 0-3, 4 contains authors
urls = set()
for group in puzGroups[:4]:
    aTags = group.find_all('a')
    for aTag in aTags:
        urls.add(aTag['href']) # take url link

# save the links to puzzle_bases.txt
outFile = open('puzzle_bases.txt','w')
outFile2 = open('puzzle_bases_excluded.txt','w')
for url in sorted(urls):
    if url.endswith('index.htm'):
        outFile.write(puzBaseUrl+url+'\n')
    else: # urls without puzzle pages
        outFile2.write(puzBaseUrl+url+'\n')
outFile.close()
