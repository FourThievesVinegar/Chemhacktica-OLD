from lxml import html
import requests
import re
#import random
#import time 
from nist_modules import postpage
from nist_modules import getrxns

# FILE INFO
filename = "/home/indra/Documents/Projects/CRN_4TV/DATA/CASRN/result_files/checked/FOR_NIST_CRAWL/cas_data_1.txt"
filehandle= open(filename, "r")
outfilename = "/home/indra/Documents/Projects/Chemhacktica/cas_nist_1.txt"
outhandle = open(outfilename, "w")
anomfilename = "/home/indra/Documents/Projects/Chemhacktica/anom_output.txt"
anomhandle = open(anomfilename, "w")

# create session for connection pooling as we are hitting the same database repeatedly
s = requests.Session()

# URL
url = 'http://kinetics.nist.gov/solution/SearchForm'

for line in filehandle:
   print('===============================')
   fields = line.split('|')
#   rct1 = fields[0] 
   rct1 = "100-00-5"
   payload = {"database":"solution",
              "REACTANT1":rct1, "REACTANT2":"", "REACTANT3":"", 
              "PRODUCT1":"", "PRODUCT2":"", "PRODUCT3":"", 
              "SOLVENT1":"", "SOLVENT2":"", "SOLVENT3":""}

   r = postpage(s, url, payload)
   tree = html.fromstring(r.content)
   text = tree.xpath('//td[@valign="TOP"][@width="100%"]/text()')
   text2 = [el.replace('\n', '') for el in text]
   text3 = list(filter(None, text2))
   try:
      text4 = re.findall('\d+', text3[0]) 
      if(len(text4)!=0 and text4[0]!='0'):
         print("There were", text4[0], "results.\n")
         rxn = getrxns(s, tree)
         row = []
         row = " | ".join([rct1, text4[0], fields[1], fields[2]])
         outhandle.writelines(row+'\n')
      elif(len(text4)==0):
         print("There were", len(text4), "results.\n")
   except IndexError:
      print("Anomalous CASRN: ", rct1)
      row = []
      row = " | ".join([rct1, fields[1], fields[2]])
      anomhandle.writelines(row+'\n')

   exit()
outhandle.close()
anomhandle.close()










