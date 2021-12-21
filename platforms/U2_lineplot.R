library(ggplot2)

# url_23_1='./23-1'
# url_A23d='./A23d'
url_18_23_1='./18_23-1'
url_18_3K_1='./18_3K-1'
url_seqwell='./SeqWell'
url_ftd='./scFTDseq'
url_dropseq11='./Dropseq11'
url_dropseq12='./Dropseq12'
url_dropseq77='./Dropseq77'
url_10x_v2='./10x_v2'
url_10x_v3_1='./v3_10x_1'
url_10x_v3_2='./v3_10x_2'
url=c(url_18_23_1,url_18_3K_1,url_seqwell,url_ftd,url_dropseq11, url_dropseq12,url_dropseq77,url_10x_v2,url_10x_v3_1, url_10x_v3_2)
file=paste(url,'/V1_mouse_line.txt',sep='')

data=data.frame()
for (i in 1:length(file)){
    tmp=read.table(file[i],header=T,sep='\t')
    data=rbind(data,tmp)
}
data=na.omit(data)
data$mouse_reads=data$mouse_reads/1000
data$mouse_umis=data$mouse_umis/1000
data$mouse_genes=data$mouse_genes/1000


pdf('V2_read_umi.pdf',width=6,height=3.5)
ggplot(data, aes(x=mouse_reads, y=mouse_umis, group=platforms))+
  geom_line(aes(color=platforms))+
  geom_point(aes(color=platforms))+
  xlab("Reads per cell (x10^3)") + ylab("Average number of transcripts per cell (x10^3)")+
  theme_bw()
dev.off()

pdf('V2read_gene.pdf',width=6,height=3.5)
ggplot(data, aes(x=mouse_reads, y=mouse_genes, group=platforms))+
  geom_line(aes(color=platforms))+
  geom_point(aes(color=platforms))+
  xlab("Reads per cell (x10^3)") + ylab("Average number of genes per cell (x10^3)")+
  theme_bw()
dev.off()

