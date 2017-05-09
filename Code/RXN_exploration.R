library(ggplot2)

# BRINGING IN RXN DATA
filename = "/home/indra/Documents/Projects/CRN_4TV/DATA/RXN_RESULTS/nist_reactions.txt"
df.data <- read.table(filename, header=TRUE, sep="|")

# MOST FREQUENT REACTANTS
df.casfreq <- as.data.frame(table(df.data$CASRN_RCT))
colnames(df.casfreq) <- c("CASRN_RCT", "Freq")
df.kinfreq <- as.data.frame(table(df.casfreq$Freq))
x <- as.numeric(df.kinfreq$Var1)
y <- as.numeric(df.kinfreq$Freq)
d <- data.frame(x,y)
#plot(log(x),log(y))

#set.seed(5)
#d <- data.frame(x=1:100, y=rlnorm(100, meanlog=5, sdlog=3))

with(d, {
   plot(x, y, log="y", yaxt="n", xaxt="n", ylab="Number of Nodes", xlab="kin")
   y1 <- floor(log10(range(y)))
   x1 <- floor(log10(range(x)))
   powy <- seq(y1[1], y1[2]+1)
   powx <- seq(x1[1], x1[2]+1)
   ticksaty <- as.vector(sapply(powy, function(p) (1:10)*10^p))
   ticksatx <- as.vector(sapply(powy, function(p) (1:10)*10^p))
   axis(2, 10^powy)
   axis(2, ticksaty, labels=NA, tcl=-0.25, lwd=0, lwd.ticks=1)
   axis(1, 10^powx)
   axis(1, ticksatx, labels=NA, tcl=-0.25, lwd=0, lwd.ticks=1)
})


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