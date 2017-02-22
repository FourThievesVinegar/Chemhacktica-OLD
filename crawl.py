from lxml import html
#from lxml import etree 
import requests
import re
import random
import time 

# ============================================================================================
def getpage(url,payload):

   delay = random.uniform(1,1.5)
   sleepy_time = delay*19.19
   r = requests.post(url, data = payload)

   again=True
   while(again):
      try:
#         page = requests.get(pagename, timeout=(9.05, 33.12))
         r = requests.post(url, data = payload, timeout=(9,33.3))
         if(r.status_code==200):
            print('Status OK: ', r.status_code)
            again=False
         else:
            print('Status not OK: ', r.status_code)        
            print('sleeping for', sleepy_time, 'seconds.....')
            time.sleep(sleepy_time)
      except Exception as e1:
         print('Exception: ', e1)
         print('sleeping for', sleepy_time, 'seconds.....')
         time.sleep(sleepy_time)
      except socket.gaierror as e2:
         print('error: ', e2)
         print('sleeping for', sleepy_time, 'seconds.....')
         time.sleep(sleepy_time)

   return r

# ============================================================================================
# FILE INFO
filename = "/home/indra/Documents/Projects/CRN_4TV/DATA/CASRN/result_files/checked/cas_data_1.txt"
filehandle= open(filename, "r")
#outfilename = "/home/indra/Documents/Projects/CRN_4TV/DATA/CASRN/result_files/cas_nist_1.txt"
outfilename = "/home/indra/Documents/Projects/Chemhacktica/test_output.txt"
outhandle = open(outfilename, "w")

# URL
url = 'http://kinetics.nist.gov/solution/SearchForm'

for line in filehandle:
   print('===============================')
   fields = line.split('|')
   rct1 = fields[0] 
   print(rct1)
   #rct1 = "100-21-0"
   payload = {"database":"solution",
              "REACTANT1":rct1, "REACTANT2":"", "REACTANT3":"", 
              "PRODUCT1":"", "PRODUCT2":"", "PRODUCT3":"", 
              "SOLVENT1":"", "SOLVENT2":"", "SOLVENT3":""}

#   r = requests.post(url, data = payload)
   r = getpage(url, payload)
   tree = html.fromstring(r.content)
   text = tree.xpath('//td[@valign="TOP"][@width="100%"]/text()')
   text2 = [el.replace('\n', '') for el in text]
   text3 = list(filter(None, text2))
   text4 = re.findall('\d+', text3[0]) 

   if(len(text4)!=0 and text4[0]!='0'):
      print("There were", text4[0], "results.\n")
      # here i could put a function to grab rxn details
      row = []
      row = " | ".join([rct1, text4[0], fields[1], fields[2]])
      outhandle.writelines(row+'\n')
   elif(len(text4)==0):
      print("There were", len(text4), "results.\n")

outhandle.close()
