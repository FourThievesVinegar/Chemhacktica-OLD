from lxml import html
import random
import time 

# ============================================================================================
def postpage(s, url, payload):

   # define time delays 
   delay = random.uniform(1,1.5)
   sleepy_time = delay*19.19

   again=True
   while(again):
      try:
         r = s.post(url, data = payload, timeout=(9,33.3))
         if(r.status_code==200):
            print('Status OK: ', r.status_code)
            again=False
         else:
            print('Status not OK: ', r.status_code)        
            print('sleeping for', sleepy_time, 'seconds.....')
            time.sleep(sleepy_time)
      except Exception as e:
         print('Exception: ', e)
         print('sleeping for', sleepy_time, 'seconds.....')
         time.sleep(sleepy_time)

   return r
# ============================================================================================
def getpage(s, url):

   # define time delays 
   delay = random.uniform(1,1.5)
   sleepy_time = delay*19.19

   again=True
   while(again):
      try:
         r = s.get(url, timeout=(9,33.3))
         if(r.status_code==200):
            print('Status OK: ', r.status_code)
            again=False
         else:
            print('Status not OK: ', r.status_code)        
            print('sleeping for', sleepy_time, 'seconds.....')
            time.sleep(sleepy_time)
      except Exception as e:
         print('Exception: ', e)
         print('sleeping for', sleepy_time, 'seconds.....')
         time.sleep(sleepy_time)

   return r
# ============================================================================================
def getrxns(s, tree):

   # get Details info
   details = tree.xpath('//td/a[contains(@href,"Detail")]/@href')

   # acess site using getpage
   for d in details:
      url = 'http://kinetics.nist.gov/solution/' +  d
      r = getpage(s, url)
      tree = html.fromstring(r.content)
      # reactant details
      # ... determine number of reactants
      # ... ... count # of times 'Name' appears
      # ... ... within each reactant block, test is 'CAS Number' is there, if not, give blank value
      #rct_block = tree.xpath('(//font[text()="Reactant details"]/following::*)')
      #rct_block = tree.xpath('(//font[text()="Reactant details"]/following::*)[2]/text()')
      #rct_block = tree.xpath('//font[text()="Reactant details"]/following-sibling::*')
      #rct_block = tree.xpath('//font[text()="Reactant Details"]/following-sibling::b[text()="Name"]/preceding-sibling::br/text()')
      #rct_block = tree.xpath('(//font[text()="Reactant Details"]/b[text()="Name"]/following::*)')
      #rct_block = tree.xpath('(//font[text()="Reactant Details"]/following-sibling::b[text()="Name"])')
      rct_block = tree.xpath('//p/font[text()="Reactant Details"]')
      print(rct_block)

      exit()     


      # restructure data if necessary

#   return rxns


# ============================================================================================

