library(ggplot2)

# BRINGING IN RXN DATA
filename = "/home/indra/Documents/Projects/CRN_4TV/DATA/RXN_RESULTS/nist_reactions.txt"
df.data <- read.table(filename, header=TRUE, sep="|")

# MOST FREQUENT REACTANTS
casrn_count <- as.data.frame(table(df.data$CASRN_RCT))
summary(casrn_count$Freq)
plot(casrn_count$Freq)

# DISTRIBUTION
hist(df.data$CASRN_RCT)

barplot(casrn_count[,2], names.arg=casrn_count[,1])


ggplot(casrn_count, aex(x=reorder()))


library("ggplot2")
num <- casrn_count$Freq
cat <- casrn_count$Var1
data <- data.frame(num, cat)    
ggplot(data,aes( x=reorder(cat,-num) ,num)   )+geom_bar(stat ="identity")

x=reorder(cat,-num)