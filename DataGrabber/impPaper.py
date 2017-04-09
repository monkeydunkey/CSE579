import urllib
from bs4 import BeautifulSoup as bs

page = urllib.urlopen('https://github.com/songrotek/Deep-Learning-Papers-Reading-Roadmap')
page = page.read()
soup = bs(page)
para = soup.select('p')
impPapFile = open('listImpPaper.txt', 'w')
for p in para:
    link = p.select('a')
    if len(link) >0 and 'arxiv' in link[0].get('href'):
        impPapFile.write(p.text.encode('utf8') + "\n")
impPapFile.close()
