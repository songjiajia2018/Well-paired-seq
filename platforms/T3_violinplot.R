library(ggplot2)

url_23_1='/home/songjia/bigdisk/YK/9_0104/23-1/compare'
url_A23d='/home/songjia/bigdisk/YK/10_0126/A23_deep/compare'
url_seqwell='/home/songjia/bigdisk/YK/platforms/Seq-Well/compare'
url_ftd='/home/songjia/bigdisk/YK/platforms/scFTD-seq/compare'
url_dropseq11='/home/songjia/bigdisk/YK/platforms/Dropseq/11/compare'
url_dropseq12='/home/songjia/bigdisk/YK/platforms/Dropseq/12/compare'
url_dropseq77='/home/songjia/bigdisk/YK/platforms/Dropseq/77/compare'
url_10x_v2='/home/songjia/bigdisk/YK/platforms/10x_v2/merge/compare'
url_10x_v3_1='/home/songjia/bigdisk/YK/platforms/v3_10x/1/merge/compare'
url_10x_v3_2='/home/songjia/bigdisk/YK/platforms/v3_10x/2/merge/compare'
url1=c(url_A23d,url_10x_v2,url_10x_v3_1,url_10x_v3_2)
url2=c(url_A23d,url_seqwell,url_ftd,url_dropseq11,url_dropseq12,url_dropseq77)
url3=c(url_A23d,url_seqwell,url_dropseq11,url_dropseq12,url_dropseq77)

# 10x
depth='40'
mouse=paste('R1_mouse',depth,sep='_')
mouse=paste(mouse,'.txt',sep='')
data=data.frame()
for (i in 1:length(url1)){
  fm=paste(url1[i],mouse,sep='/')
  m=read.table(fm,header=T,row.names=1,sep='\t')
  data=rbind(data,m)
}
data$MOUSE_NUM_GENIC_READS=data$MOUSE_NUM_GENIC_READS/1000
data$MOUSE_NUM_TRANSCRIPTS=data$MOUSE_NUM_TRANSCRIPTS/1000
data$MOUSE_NUM_GENES=data$MOUSE_NUM_GENES/1000

pdf('R3_violin_10x_read_umi.pdf')
ggplot(data, aes(x=platforms, y=MOUSE_NUM_TRANSCRIPTS, fill=platforms)) + 
  geom_violin(trim=FALSE)+
  geom_boxplot(width=0.1, fill="white")+
  labs(y = "Number of transcripts (x10^3)")+
  scale_fill_brewer(palette="Blues")+
  theme_classic()+
  theme(axis.text.x=element_text(angle=45,hjust=1,vjust=1))
dev.off()

pdf('R3_violin_10x_read_gene.pdf')
ggplot(data, aes(x=platforms, y=MOUSE_NUM_GENES, fill=platforms)) +
  geom_violin(trim=FALSE)+
  geom_boxplot(width=0.1, fill="white")+
  labs(y = "Number of genes (x10^3)")+
  scale_fill_brewer(palette="Reds")+
  theme_classic()+
  theme(axis.text.x=element_text(angle=45,hjust=1,vjust=1))
dev.off()


# seqwell scFTDseq Dropseq
depth='150'
mouse=paste('R1_mouse',depth,sep='_')
mouse=paste(mouse,'.txt',sep='')
data=data.frame()
for (i in 1:length(url2)){
  fm=paste(url2[i],mouse,sep='/')
  m=read.table(fm,header=T,row.names=1,sep='\t')
  data=rbind(data,m)
}
data$MOUSE_NUM_GENIC_READS=data$MOUSE_NUM_GENIC_READS/1000
data$MOUSE_NUM_TRANSCRIPTS=data$MOUSE_NUM_TRANSCRIPTS/1000
data$MOUSE_NUM_GENES=data$MOUSE_NUM_GENES/1000

pdf('R3_violin_read_umi.pdf')
ggplot(data, aes(x=platforms, y=MOUSE_NUM_TRANSCRIPTS, fill=platforms)) +
  geom_violin(trim=FALSE)+
  geom_boxplot(width=0.1, fill="white")+
  labs(y = "Number of transcripts (x10^3)")+
  scale_fill_brewer(palette="Blues")+
  theme_classic()+
  theme(axis.text.x=element_text(angle=45,hjust=1,vjust=1))
dev.off()

pdf('R3_violin_read_gene.pdf')
ggplot(data, aes(x=platforms, y=MOUSE_NUM_GENES, fill=platforms)) +
  geom_violin(trim=FALSE)+
  geom_boxplot(width=0.1, fill="white")+
  labs(y = "Number of genes (x10^3)")+
  scale_fill_brewer(palette="Reds")+
  theme_classic()+
  theme(axis.text.x=element_text(angle=45,hjust=1,vjust=1))
dev.off()

# human mouse
depth='150'
human=paste('R1_human',depth,sep='_')
human=paste(human,'.txt',sep='')
mouse=paste('R1_mouse',depth,sep='_')
mouse=paste(mouse,'.txt',sep='')
datah=data.frame()
datam=data.frame()
for (i in 1:length(url3)){
  fh=paste(url3[i],human,sep='/')
  fm=paste(url3[i],mouse,sep='/')
  h=read.table(fh,header=T,row.names=1,sep='\t')
  m=read.table(fm,header=T,row.names=1,sep='\t')
  datah=rbind(datah,h)
  datam=rbind(datam,m)
}
datah$species=rep('human',dim(datah)[1])
datam$species=rep('mouse',dim(datam)[1])
datah$plot=paste('h',datah$platforms,sep='_')
datam$plot=paste('m',datam$platforms,sep='_')
names(datah)=c('READS','TRANSCRIPTS','GENES','platforms','species','anno')
names(datam)=c('READS','TRANSCRIPTS','GENES','platforms','species','anno')
data=rbind(datah,datam)
data$READS=data$READS/1000
data$TRANSCRIPTS=data$TRANSCRIPTS/1000
data$GENES=data$GENES/1000

pdf('R3_violin_hm_read_umi.pdf',width=10,height=8)
ggplot(data, aes(x=anno, y=TRANSCRIPTS, fill=species))+
  geom_violin(trim=FALSE)+
  geom_boxplot(width=0.1)+
  labs(y = "Number of transcripts (x10^3)")+
  scale_fill_brewer(palette="Blues")+
  scale_fill_manual(values=c("#E69F00", "#56B4E9"))+
  theme_classic()+
  theme(axis.text.x=element_text(angle=60,hjust=1,vjust=1))
dev.off()

pdf('R3_violin_hm_read_gene.pdf',width=10,height=8)
ggplot(data, aes(x=anno, y=GENES, fill=species))+
  geom_violin(trim=FALSE)+
  geom_boxplot(width=0.1)+
  labs(y = "Number of genes (x10^3)")+
  scale_fill_brewer(palette="Reds")+
  scale_fill_manual(values=c("#E69F00", "#56B4E9"))+
  theme_classic()+
  theme(axis.text.x=element_text(angle=60,hjust=1,vjust=1))
dev.off()

