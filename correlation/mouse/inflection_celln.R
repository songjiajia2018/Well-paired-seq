data=read.table("out_gene_exon_tagged_3000.dge.txt",header=T,row.names=1)
my.counts=data
library("DropletUtils")
br.out <- barcodeRanks(my.counts)
o <- order(br.out$rank)
sum(!is.na(br.out$fitted[o]))
write(sum(!is.na(br.out$fitted[o])),'inflection_celln.txt')

#plot(br.out$rank, br.out$total, log="xy", xlab="Rank", ylab="Total")
#lines(br.out$rank[o], br.out$fitted[o], col="red")
#abline(h=metadata(br.out)$knee, col="dodgerblue", lty=2)
#abline(h=metadata(br.out)$inflection, col="forestgreen", lty=2)
#legend("bottomleft", lty=2, col=c("dodgerblue", "forestgreen"), legend=c("knee", "inflection"))

