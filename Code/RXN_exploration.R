# BRINGING IN RXN DATA
filename = "/home/indra/Documents/Projects/CRN_4TV/DATA/RXN_RESULTS/nist_reactions.txt"
df.data <- read.table(filename, header=TRUE, sep="|")

# MOST FREQUENT REACTANTS
casrn_count <- as.data.frame(table(df.data$CASRN_RCT))

# DISTRIBUTION
hist(df.data$CASRN_RCT)