from lxml import html
from lxml import etree 
import requests
import time 
import random
import sys

# output data file
datafile = open('/home/indra/Documents/Projects/CRN_4TV/DATA/CASRN/cas_data_8_216_to_257.txt', 'w')
logfile = open('/home/indra/Documents/Projects/CRN_4TV/DATA/CASRN/log_8_216_to_257.txt', 'w')
subpage = [4255, 1202, 1211, 1105, 1461, 2877, 1263, 3151, 1278]
dataset = []
delay = random.uniform(1,1.5)
#--~~--~~--~~--~~ MAIN LOOP OVER ALL PAGES --~~--~~--~~--~~--~~#
for i in range(0, 9):
   for j in range(1, subpage[i]):

      # 1.a PARSE IN WEBSITE 
      pagename = 'http://www.chemnet.com/cas/list/'+ str(i+1) + '-' + str(j) + '.html'
      print('==========================================')
      print('Scraping.....: ', pagename)
      logfile.writelines('==========================================\n')
      logfile.writelines('Scraping.....: '+pagename+'\n')
      sleepy_time = delay*19.19
      again=True
      while(again):
         try:
            page = requests.get(pagename, timeout=(9.05, 33.12))
            if(page.status_code==200):
               print(page.status_code)
               again=False
            else:
               print('Status not OK: ', page.status_code)        
               print('sleeping for', sleepy_time, 'seconds.....')
               logfile.writelines('Status not OK: '+str(page.status_code)+'\n')        
               logfile.writelines('sleeping for'+str(sleepy_time)+'seconds.....\n')
               time.sleep(sleepy_time)
         except Exception as e:
            print('Exception: ', e)
            print('sleeping for', sleepy_time, 'seconds.....')
            logfile.writelines('Exception: '+str(e)+'\n')
            logfile.writelines('sleeping for'+str(sleepy_time)+'seconds.....\n')
            time.sleep(sleepy_time)

      logfile.writelines('page parsed\n')
      # 2. GET CASRN AND FULL NAME
      # grab text from element <a>
      # which is a child of element <p>, 
      # which is also a grandchild of element <li>
      tree = html.fromstring(page.content)
      CAS_and_name = tree.xpath('//li/p/a/text()')
      print(len(CAS_and_name))

      count_while = 0
      # 3. TEST THAT PAGE WAS ACCESSED AND TEXT IN BODY GRABBED
      while(len(CAS_and_name)<200):
         count_while += 1
         if(count_while > 3):
            print('shit just got real..')
            print('sleeping for', sleepy_time*6, 'seconds.....')
            logfile.writelines('shit just got real..\n')
            logfile.writelines('sleeping for'+str(sleepy_time*6)+'seconds.....\n')
            time.sleep(sleepy_time*6)
            page = requests.get(pagename)
            tree = html.fromstring(page.content)
            CAS_and_name = tree.xpath('//li/p/a/text()')
         else:
            print('sleeping for', sleepy_time, 'seconds.....')
            logfile.writelines('sleeping for'+str(sleepy_time)+'seconds.....\n')
            time.sleep(sleepy_time)
            page = requests.get(pagename)
            tree = html.fromstring(page.content)
            CAS_and_name = tree.xpath('//li/p/a/text()')

      logfile.writelines('page scraped\n')
      # 4. SPLIT CAS AND NAME INTO SEPARATE LISTS 
      casrn = []
      name = []
      for n in range(0,len(CAS_and_name)):
         if n==0:
            casrn.append(CAS_and_name[n])
         elif n%2!=0:
            name.append(CAS_and_name[n])
         elif n%2==0:
            casrn.append(CAS_and_name[n])

      # 4. GET MOLECULAR FORMULA
      elements = tree.xpath('//li/p[@class="bw_line3"]')
      formulas = [] 
      for k in range(0,100):
         element_text = elements[k].itertext()
         single_formula = "" 
         for elt in element_text:
            single_formula += elt
         formulas.append(single_formula)
#         print(k) 

      # 5. WRITE CASRN, FULL NAME AND FORMULA TO PIPE-DELIMITED TEXT FILE
      for l in range(0,100):
         str_casrn = str(casrn[l]).replace('\r','').replace('\n','')
         str_name = str(name[l]).replace('\r','').replace('\n','')
         str_form = str(formulas[l]).replace('\r','').replace('\n','')
         row=[]
         row = "|".join([str_casrn, str_name, str_form])
#         row = "|".join([str_casrn, str_name])
         datafile.writelines(row+'\n')
      print("Scrape successful.")
      logfile.writelines('Scrape successful.\n')

datafile.close()
logfile.close()
   
