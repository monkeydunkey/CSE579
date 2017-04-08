"""
Very simple script that simply iterates over all files data/pdf/f.pdf
and create a file data/txt/f.pdf.txt that contains the raw text, extracted
using the "pdftotext" command. If a pdf cannot be converted, this
script will not produce the output file.
"""

import os
import sys
import time
import shutil
import pickle

from utils import Config

from pdfminer.pdfinterp import PDFResourceManager, PDFPageInterpreter
from pdfminer.converter import TextConverter
from pdfminer.layout import LAParams
from pdfminer.pdfpage import PDFPage
from cStringIO import StringIO

def convert_pdf_to_txt(path):
    print ('parsing file', path)
    rsrcmgr = PDFResourceManager()
    retstr = StringIO()
    codec = 'utf-8'
    laparams = LAParams()
    device = TextConverter(rsrcmgr, retstr, codec=codec, laparams=laparams)
    fp = file(path, 'rb')
    interpreter = PDFPageInterpreter(rsrcmgr, device)
    password = ""
    maxpages = 0
    caching = True
    pagenos=set()

    for page in PDFPage.get_pages(fp, pagenos, maxpages=maxpages, password=password,caching=caching, check_extractable=True):
        interpreter.process_page(page)

    text = retstr.getvalue()

    fp.close()
    device.close()
    retstr.close()
    return text

'''
# make sure pdftotext is installed
if not shutil.which('pdftotext'): # needs Python 3.3+
  print('ERROR: you don\'t have pdftotext installed. Install it first before calling this script')
  sys.exit()
'''
if not os.path.exists(Config.txt_dir):
  print('creating ', Config.txt_dir)
  os.makedirs(Config.txt_dir)

have = set(os.listdir(Config.txt_dir))
files = os.listdir(Config.pdf_dir)
for i,f in enumerate(files): # there was a ,start=1 here that I removed, can't remember why it would be there. shouldn't be, i think.

  txt_basename = f + '.txt'
  if txt_basename in have:
    print('%d/%d skipping %s, already exists.' % (i, len(files), txt_basename, ))
    continue

  pdf_path = os.path.join(Config.pdf_dir, f)
  txt_path = os.path.join(Config.txt_dir, txt_basename)
  try:
    textData = convert_pdf_to_txt(pdf_path)
    ##cmd = "pdftotext %s %s" % (pdf_path, txt_path)
    ##os.system(cmd)
    with open(txt_path, 'wb') as fp:
        fp.write(textData)
    print('%d/%d' % (i, len(files)))

    # check output was made
    if not os.path.isfile(txt_path):
        # there was an error with converting the pdf
        print('there was a problem with parsing %s to text, creating an empty text file.' % (pdf_path, ))
        os.system('touch ' + txt_path) # create empty file, but it's a record of having tried to convert
  except Exception as e:
      print ('There was an exception in parsing file', f)
  time.sleep(0.01) # silly way for allowing for ctrl+c termination
