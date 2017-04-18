#this file is to check whether given papers are present in the dataset or not
import pickle
from utils import Config

db = pickle.load(open(Config.db_path, 'rb'))
#Probably could add this to the config itself
with open('listImpPaper.txt') as f:
    paper_titles = set([x.split('"')[1].strip().replace(".", "").lower() for x in f.readlines()])

print len(paper_titles)

#paper_titles = set(['Autonomous Fault Detection in Self-Healing Systems using Restricted\n  Boltzmann Machines', 'Very deep convolutional networks for large-scale image recognition'])


for pid,j in db.items():
    if len(paper_titles) <= 0:
        break
    if j['title'].strip().lower() in paper_titles:
        print 'found', j['title']
        paper_titles.remove(j['title'].strip().lower())

if len(paper_titles) == 0:
    print 'All the papers were found'
else:
    print 'Following are the papers that were not found', paper_titles

print len(paper_titles)
