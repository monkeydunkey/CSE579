#this file is to check whether given papers are present in the dataset or not
import pickle
from utils import Config

db = pickle.load(open(Config.db_path, 'rb'))
#Probably could add this to the config itself
paper_titles = set(['Autonomous Fault Detection in Self-Healing Systems using Restricted\n  Boltzmann Machines'])


for pid,j in db.items():
    if len(paper_titles) <= 0:
        break
    if j['title'] in paper_titles:
        paper_titles.remove(j['title'])

if len(paper_titles) == 0:
    print 'All the papers were found'
else:
    print 'Following are the papers that were not found', list(paper_titles)
