from lxml import html
import random
import time 
import re 

# ============================================================================================
def mult_repl(text, adict):
   rx = re.compile('|'.join(map(re.escape, adict)))
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
      # ensure there are reactant, product and solvent blocks in the reaction info
      blocks = tree.xpath('(//b[text()="Name"]/preceding-sibling::b/font/text())')
      if(len(blocks)==3):
          # go about isolating reaction info (all three blocks mentioned above)
          # so beautiful i dont want to delete it............
#         body_xpath = '//p/b/font[text()="Reactant details"]/parent::*/parent::*/parent::*/descendant-or-self::*/text()'
         body_path = '//body/descendant-or-self::*/text()'
         body_text = tree.xpath(body_path)
         start_index = body_text.index("Reactant details")
         rxn_dirty = body_text[start_index : ]
         # next clean up using multiple replacements
         rxn_clean = [el.replace('\n', '') for el in rxn_dirty]
         rxn_clean = [el.replace('\xa0', '') for el in rxn_clean]
         rxn_clean = [el.replace(':', '') for el in rxn_clean]
         rxn_clean = [el.replace('%', '') for el in rxn_clean]
         rxn_clean = list(filter(None, rxn_clean))
         print(rxn_clean)

         # keep only Name, Formula, CAS number - remove everything between 'Other names' and 'Name'/end of list


         # insert missing CAS number placeholders


         # separate into Reactants, Products, Solvents

         # convert to storable format

         # rejoice!

         exit()     

      else:
         print("Incomplete reaction information - data not collected")
         print(len(blocks))

      # restructure data if necessary

#   return rxns

# ============================================================================================

