# THIS IS SCRIPT TO COMPILE ALL SEPARATE RXN FILES INTO ONE FILE, GIVING A UNIQUE ID TO EACH REACTION

# FILE INFO
rootdir = "/home/indra/Documents/Projects/CRN_4TV/DATA/RXN_RESULTS/"
ID1 = ['O', 'W', 'R', 'F', 'V', 'X', 'S', 'E', 'N']
ID2 = 'R'

# output file
outfilename = rootdir + "nist_reactions.txt"
outhandle = open(outfilename, "w")
header = "|".join(["RXN_ID", "CASRN_RCT ", 
                   "RCT1 ", "RCT2 ", "RCT3 ",
                   "PRD1 ", "PRD2 ", "PRD3 ",
                   "SLV1 ", "SLV2 ", "SLV3 "])
outhandle.writelines(header+'\n')

for i in range(0,9):
  
   # input file 
   infilename = rootdir +  "nist_reactions_cas_" + str(i+1) + ".txt"
   inhandle = open(infilename, "r")

   linecnt = 0  

   for line in inhandle:
      fields = line.split('|')
      linecnt += 1
      row = []
      if(linecnt > 1):
         newID = ID1[i] + ID2 + str(linecnt-1)
         row = " | ".join([newID, fields[1], fields[2], 
                           fields[3], fields[4], fields[5], 
                           fields[6], fields[7], fields[8], 
                           fields[9], fields[10]])
      outhandle.writelines(row)

inhandle.close()
outhandle.close()








