from lxml import html
import random
import time 
import re 

def getCASnumbers(stringlist):
   cas_numbers = []
   cas_indices = [i for i,x in enumerate(stringlist) if x=='CAS Number']
   for ind in cas_indices:
      cas_numbers.append(stringlist[ind+1]) 
   # make sure there are three items in list to be returned
   while(len(cas_numbers) < 3):
      cas_numbers.append('NA')

   return cas_numbers
# ============================================================================================
# potentially not useful..side burner for now
# if we wanted more than just CAS number this would need to be revisited
#=============================================================================================
def removeOthernames(stringlist):
   othnames_indices = [i for i,val in enumerate(stringlist) if val=="Other names"]
   print(stringlist)
   # 1.  identify all indices where 'Other names' occur
   range_start = 'Name'
   range_end = 'Other names'

#   for el in stringlist:
#      print("-----------------")
#      print("el in outer: ", el)
#      if(range_start<=el<=range_end):
#         print("el in inner: ", el)
##      print(el)

   list1 = [x for x in stringlist if not(range_start<=x<=range_end)]   
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
#            print('Status OK: ', r.status_code)
            again=False
         else:
#            print('Status not OK: ', r.status_code)        
#            print('sleeping for', sleepy_time, 'seconds.....')
            time.sleep(sleepy_time)
      except Exception as e:
#         print('Exception: ', e)
#         print('sleeping for', sleepy_time, 'seconds.....')
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
#            print('Status OK: ', r.status_code)
            again=False
         else:
#            print('Status not OK: ', r.status_code)        
#            print('sleeping for', sleepy_time, 'seconds.....')
            time.sleep(sleepy_time)
      except Exception as e:
#         print('Exception: ', e)
#         print('sleeping for', sleepy_time, 'seconds.....')
         time.sleep(sleepy_time)

   return r
# ============================================================================================
def getrxns(s, tree):

   # get Details info
   details = tree.xpath('//td/a[contains(@href,"Detail")]/@href')

   rxn_cas_nums = []
   # access site using getpage
   for d in details:
#      print("~~~~~~~~~~~~~~~~~~~")
#      print("d = ", d)
      url = 'http://kinetics.nist.gov/solution/' +  d
      r = getpage(s, url)
      tree = html.fromstring(r.content)
      # ensure there are reactant, product and solvent blocks in the reaction info
      blocks = tree.xpath('(//b[text()="Name"]/preceding-sibling::b/font/text())')
      if(len(blocks)==3):
         # rxn_dirty is full block of reaction info
         body_path = '//body/descendant-or-self::*/text()'
         body_text = tree.xpath(body_path)
         start_index = body_text.index("Reactant details")
         rxn_dirty = body_text[start_index : ]
         # rxn_clean is cleaned up block of reaction info
         rxn_clean = [el.replace('\n', '') for el in rxn_dirty]
         rxn_clean = [el.replace('\xa0', '') for el in rxn_clean]
         rxn_clean = [el.replace(':', '') for el in rxn_clean]
         rxn_clean = [el.replace('%', '') for el in rxn_clean]
         rxn_clean = list(filter(None, rxn_clean))
         # separate block  into reactants, products, and solvents 
         prod_index = rxn_clean.index("Product details")
         solv_index = rxn_clean.index("Solvent details")
         reactants  = rxn_clean[:prod_index]
         products   = rxn_clean[prod_index : solv_index]
         solvents   = rxn_clean[solv_index : ]
         # grab CAS numbers of reactants, products and solvents
         rct_cas_nums = getCASnumbers(reactants)
         prd_cas_nums = getCASnumbers(products)
         slv_cas_nums = getCASnumbers(solvents)
         # convert to storable format
         single_rxn_cas_nums = "|".join([rct_cas_nums[0], rct_cas_nums[1], rct_cas_nums[2],
                                         prd_cas_nums[0], prd_cas_nums[1], prd_cas_nums[2],
                                         slv_cas_nums[0], slv_cas_nums[1], slv_cas_nums[2]])
         # max list of all reactions 
         rxn_cas_nums.append(single_rxn_cas_nums)
#         print(rxn_cas_nums)

      else:
#         print("Incomplete reaction information - data not collected")
#         print(len(blocks))
          x = 1

#       exit()
   return rxn_cas_nums

# ============================================================================================

