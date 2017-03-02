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
      # ... ensure there are reactants, products and solvents in the reaction info
      blocks = tree.xpath('(//b[text()="Name"]/preceding-sibling::b/font/text())')
      if(len(blocks)==3):
         # get reactant info 
         xpath = '//p/b/font[text()="Reactant details"]/parent::*/parent::*/descendant-or-self::*/text()'
         rct_block = tree.xpath(xpath)
         rct_block2 = [el.replace('\n', '') for el in rct_block]
         rct_block3 = [el.replace('\xa0', '') for el in rct_block2]
         rct_block3 = [el.replace('\xa0', '') for el in rct_block2]
         rct_block4 = list(filter(None, rct_block3))
         print(rct_block4)
         exit()     
      else:
         print("Incomplete reaction information - data not collected")
         print(len(blocks))

      # restructure data if necessary

#   return rxns

# ============================================================================================

