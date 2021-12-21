
a=read.table("out_cell_readcounts.txt.gz", header=F, stringsAsFactors=F)
x=cumsum(a$V1)
x=x/max(x)
plot(1:length(x), x, type='l', col="blue", xlab="cell barcodes sorted by number of reads [descending]",ylab="cumulative fraction of reads", xlim=c(1,5000))

