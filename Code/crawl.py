from lxml import html
import requests
import re
from nist_modules import postpage
from nist_modules import getrxns

# FILE INFO
infilename = "/home/indra/Documents/Projects/CRN_4TV/DATA/CASRN/result_files/checked/FOR_NIST_CRAWL/cas_data_2.txt"
inhandle= open(infilename, "r")
outfilename = "/home/indra/Documents/Projects/CRN_4TV/DATA/RXN_RESULTS/nist_reactions_cas_2.txt"
outfile = open(outfilename, "w")
anomfilename = "/home/indra/Documents/Projects/CRN_4TV/DATA/RXN_RESULTS/anom_output_2.txt"
anomhandle = open(anomfilename, "w")

# create session for connection pooling as we are hitting the same database repeatedly
s = requests.Session()

# URL
url = 'http://kinetics.nist.gov/solution/SearchForm'
found = 0

# header for results file
header = "|".join(["RXN_NUMBER ", "CASRN_RCT ", 
                  "RCT1 ", "RCT2 ", "RCT3 ",
                  "PRD1 ", "PRD2 ", "PRD3 ",
                  "SLV1 ", "SLV2 ", "SLV3 "])
outfile.writelines(header+'\n')
found_place = False
for line in inhandle:
   fields = line.split('|')
   rct1 = fields[0] 
   print(rct1)
#   if '126783-63-9' in line:
#      found_place = True
   found_place = True
   if found_place:
      #rct1 = "100-00-5"
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
            rxn = getrxns(s, tree)
#            print(rxn)
            for item in rxn:
               found += 1
               row = "|".join([str(found), rct1, item])
               outfile.writelines(row+'\n') 
#            exit()
      except IndexError: 
         # put exit() here to test whats going on - i forgot
         print("Anomalous CASRN: ", rct1)
         row = []
         row = " | ".join([rct1, fields[1], fields[2]])
         anomhandle.writelines(row+'\n')

anomhandle.close()
outfile.close()









