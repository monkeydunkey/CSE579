import os
import time
import pickle
import shutil
import random
from urllib import urlopen
from utils import Config

timeout_secs = 10 # after this many seconds we give up on a paper
if not os.path.exists(Config.pdf_dir): os.makedirs(Config.pdf_dir)
have = set(os.listdir(Config.pdf_dir)) # get list of all pdfs we already have

numok = 0
numtot = 0
db = pickle.load(open(Config.db_path, 'rb'))

with open('listImpPaper.txt') as f:
        paper_titles = set([x.split('"')[1].strip().replace(".", "").lower() for x in f.readlines()])

for pid,j in db.items():
  cats = ['cs.cv', 'cs.cl', 'cs.ne', 'cs.lg', 'cs.ai']
  pdfs = [x['href'] for x in j['links'] if x['type'] == 'application/pdf']
  categoryPath = "None"
  for tag in j['tags']:
      if tag['term'].lower() in cats:
          categoryPath = tag['term']
          break
  assert len(pdfs) == 1
  pdf_url = pdfs[0] + '.pdf'
  basename = pdf_url.split('/')[-1]
  #IF the specific category path was not created creating it
  if not os.path.exists(os.path.join(Config.pdf_dir, categoryPath)): os.makedirs(os.path.join(Config.pdf_dir, categoryPath))
  fname = os.path.join(Config.pdf_dir, categoryPath, basename)

  # try retrieve the pdf
  numtot += 1
  try:
    if not basename in have and j['title'].strip().lower() in paper_titles:
      print('fetching %s into %s' % (pdf_url, fname))
      req = urlopen(pdf_url)#, None, timeout_secs)
      with open(fname, 'wb') as fp:
          #shutil.copyfileobj(req, fp)
          fp.write(req.read())
      time.sleep(0.05 + random.uniform(0,0.1))
    else:
      print('%s exists, skipping' % (fname, ))
    numok+=1
  except Exception as e:
    print('error downloading: ', pdf_url)
    print(e)

  print('%d/%d of %d downloaded ok.' % (numok, numtot, len(db)))

print('final number of papers downloaded okay: %d/%d' % (numok, len(db)))
