from lxml import html
import requests
import re
from nist_modules import postpage
from nist_modules import getrxns

# FILE INFO
infilename = "/home/indra/Documents/Projects/CRN_4TV/DATA/CASRN/result_files/checked/FOR_NIST_CRAWL/cas_data_1.txt"
inhandle= open(infilename, "r")
anomfilename = "/home/indra/Documents/Projects/Chemhacktica/anom_output.txt"
anomhandle = open(anomfilename, "w")

# create session for connection pooling as we are hitting the same database repeatedly
s = requests.Session()

# URL
url = 'http://kinetics.nist.gov/solution/SearchForm'

found = 0
for line in inhandle:
   fields = line.split('|')
   #rct1 = fields[0] 
   rct1 = "100-00-5"
   payload = {"database":"solution",
              "REACTANT1":rct1, "REACTANT2":"", "REACTANT3":"", 
              "PRODUCT1":"", "PRODUCT2":"", "PRODUCT3":"", 
              "SOLVENT1":"", "SOLVENT2":"", "SOLVENT3":""}

   r = postpage(s, url, payload)
   tree = html.fromstring(r.content)
   nresult = tree.xpath('//td[@valign="TOP"][@width="100%"]/text()')
   nresult = [el.replace('\n', '') for el in nresult]
   nresult = list(filter(None, nresult))
   try:
      nresult = re.findall('\d+', nresult[0]) 
      if(len(nresult)!=0 and nresult[0]!='0'):
         found += 1
         rxn = getrxns(s, tree)
         print(rxn)
         exit()
#         row = []
#         row = " | ".join([rct1, nresult[0], fields[1], fields[2]])
#         if(found==3):
#            print('==============================================================')
#            print('**************************************************************')
#            print('==============================================================')
#            print("Found reaction: ", found)
#            print(rct1)
#            print("There were", nresult[0], "results.\n")
#            print(rxn)
#            exit()
   except IndexError: 
      # put exit() here to test whats going on - i forgot
      print("Anomalous CASRN: ", rct1)
      row = []
      row = " | ".join([rct1, fields[1], fields[2]])
      anomhandle.writelines(row+'\n')

anomhandle.close()










