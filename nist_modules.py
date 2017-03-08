from lxml import html
import random
import time 
import re 

# ============================================================================================
def removeOthernames(stringlist):
   othnames_indices = [i for i,val in enumerate(stringlist) if val=="Other names"]
   # 1.  identify all indices where 'Other names' occur
   range_start = 'Other names'
   range_end = 'Name'
   list1 = [x for x in stringlist if not(range_start<=x<=range_end)]   
   #list1 = [x for x in stringlist print(x)]   
   print(list1)
   
   exit() 


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
         # separate into Reactants, Products, Solvents 
         prod_index = rxn_clean.index("Product details")
         solv_index = rxn_clean.index("Solvent details")
         rct_dirty = rxn_clean[:prod_index]
         prod_dirty = rxn_clean[prod_index : solv_index]
         solv_dirty = rxn_clean[solv_index : ]
         # remove 'Other names' 
         rct_dirty = removeOthernames(rct_dirty)
         exit()


         # insert missing CAS number placeholders



         # convert to storable format

         # rejoice!

         exit()     

      else:
         print("Incomplete reaction information - data not collected")
         print(len(blocks))

      # restructure data if necessary

#   return rxns

# ============================================================================================

