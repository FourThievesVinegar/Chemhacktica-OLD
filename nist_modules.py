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
      # ... ensure there are reactants, products and solvents in the reaction info
      blocks = tree.xpath('(//b[text()="Name"]/preceding-sibling::b/font/text())')
      if(len(blocks)==3):
         print(blocks)
         # get reactant info 
         #rct_block = tree.xpath('//b/font[text()="Reactant details"]/preceding-sibling::*')
         #rct_block = tree.xpath('(//font[text()="Reactant details"]/following::*)[2]/text()')
         #rct_block = tree.xpath('//p/font[text()="Reactant Details"]')
         print(rct_block)

#        exit()     
      else:
         print("Incomplete reaction information")
         print(len(blocks))

      # restructure data if necessary

#   return rxns

# ============================================================================================

