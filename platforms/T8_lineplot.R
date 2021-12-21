library(ggplot2)

#url_23_1='/home/songjia/bigdisk/YK/9_0104/23-1/compare'
#url_A23d='/home/songjia/bigdisk/YK/10_0126/A23_deep/compare'
#url_seqwell='/home/songjia/bigdisk/YK/platforms/Seq-Well/compare'
#url_ftd='/home/songjia/bigdisk/YK/platforms/scFTD-seq/compare'
#url_dropseq11='/home/songjia/bigdisk/YK/platforms/Dropseq/11/compare'
#url_dropseq12='/home/songjia/bigdisk/YK/platforms/Dropseq/12/compare'
#url_dropseq77='/home/songjia/bigdisk/YK/platforms/Dropseq/77/compare'
#url_10x_v2='/home/songjia/bigdisk/YK/platforms/10x_v2/merge/compare'
#url_10x_v3_1='/home/songjia/bigdisk/YK/platforms/v3_10x/1/merge/compare'
#url_10x_v3_2='/home/songjia/bigdisk/YK/platforms/v3_10x/2/merge/compare'
url_23_1='./23-1'
url_A23d='./A23d'
url_seqwell='./SeqWell'
url_ftd='./scFTDseq'
url_dropseq11='./Dropseq11'
url_dropseq12='./Dropseq12'
url_dropseq77='./Dropseq77'
url_10x_v2='./10x_v2'
url_10x_v3_1='./v3_10x_1'
url_10x_v3_2='./v3_10x_2'
url=list(url_23_1,url_A23d,url_seqwell,url_ftd,url_dropseq12,url_dropseq77,url_10x_v2,url_10x_v3_2)
file=paste(url,'/R7_mouse_line.txt',sep='')

data=data.frame()
for (i in 1:length(file)){
    tmp=read.table(file[i],header=T,sep='\t')
    data=rbind(data,tmp)
}
data=na.omit(data)
data$MOUSE_NUM_GENIC_READS=data$MOUSE_NUM_GENIC_READS/1000
data$MOUSE_NUM_TRANSCRIPTS=data$MOUSE_NUM_TRANSCRIPTS/1000
data$MOUSE_NUM_GENES=data$MOUSE_NUM_GENES/1000


pdf('R8_plot_read_umi.pdf',width=6,height=3.5)
ggplot(data, aes(x=MOUSE_NUM_GENIC_READS, y=MOUSE_NUM_TRANSCRIPTS, group=platforms))+
  geom_line(aes(color=platforms))+
  geom_point(aes(color=platforms))+
  xlab("Reads per cell (x10^3)") + ylab("Average number of transcripts per cell (x10^3)")+
  theme_bw()
dev.off()

pdf('R8_plot_read_gene.pdf',width=6,height=3.5)
ggplot(data, aes(x=MOUSE_NUM_GENIC_READS, y=MOUSE_NUM_GENES, group=platforms))+
  geom_line(aes(color=platforms))+
  geom_point(aes(color=platforms))+
  xlab("Reads per cell (x10^3)") + ylab("Average number of genes per cell (x10^3)")+
  theme_bw()
dev.off()

