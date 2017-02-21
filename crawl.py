from lxml import html
#from lxml import etree 
import requests
import re

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
   #rct1 = "100-21-0"
   print(rct1)
   payload = {"database":"solution",
              "REACTANT1":rct1, "REACTANT2":"", "REACTANT3":"", 
              "PRODUCT1":"", "PRODUCT2":"", "PRODUCT3":"", 
              "SOLVENT1":"", "SOLVENT2":"", "SOLVENT3":""}

   r = requests.post(url, data = payload)
   tree = html.fromstring(r.content)
   text = tree.xpath('//td[@valign="TOP"][@width="100%"]/text()')
   print(text)
   text2 = [el.replace('\n', '') for el in text]
   print(text2)
   text3 = list(filter(None, text2))
   print(text3)
   text4 = re.findall('\d+', text3[0]) 
   print(text4)
   if(len(text4)!=0 and text4[0]!='0'):
      print("There were", text4[0], "results.\n")
      # here i could put a function to grab rxn details
      row = []
      row = " | ".join([rct1, text4[0], fields[1], fields[2]])
      outhandle.writelines(row+'\n')
   elif(len(text4)==0):
      print("There were", len(text4), "results.\n")

#   exit()
outhandle.close()
