args=commandArgs(T)

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
url1=c(url_18_23_1,url_18_3K_1,url_10x_v2,url_10x_v3_1,url_10x_v3_2)
url2=c(url_18_23_1,url_18_3K_1,url_seqwell,url_ftd,url_dropseq11,url_dropseq12,url_dropseq77)

# 10x
# low
depth=args[1]
mouse=paste('V1_vm',depth,sep='_')
mouse=paste(mouse,'.txt',sep='')
data=data.frame()
for (i in 1:length(url1)){
  fm=paste(url1[i],mouse,sep='/')
  m=read.table(fm,header=T,row.names=1,sep='\t')
  data=rbind(data,m)
}
data$mouse_reads=data$mouse_reads/1000
data$mouse_umis=data$mouse_umis/1000
data$mouse_genes=data$mouse_genes/1000

pdf('V3_violin_low_read_umi.pdf')
ggplot(data, aes(x=platforms, y=mouse_umis, fill=platforms)) + 
  geom_violin(trim=FALSE)+
  geom_boxplot(width=0.1, fill="white")+
  labs(y = "Number of transcripts (x10^3)")+
  scale_fill_brewer(palette="Blues")+
  theme_classic()+
  theme(axis.text.x=element_text(angle=45,hjust=1,vjust=1))
dev.off()

pdf('V3_violin_low_read_gene.pdf')
ggplot(data, aes(x=platforms, y=mouse_genes, fill=platforms)) +
  geom_violin(trim=FALSE)+
  geom_boxplot(width=0.1, fill="white")+
  labs(y = "Number of genes (x10^3)")+
  scale_fill_brewer(palette="Reds")+
  theme_classic()+
  theme(axis.text.x=element_text(angle=45,hjust=1,vjust=1))
dev.off()


# seqwell scFTDseq Dropseq
# high
depth=args[2]
mouse=paste('V1_vm',depth,sep='_')
mouse=paste(mouse,'.txt',sep='')
data=data.frame()
for (i in 1:length(url2)){
  fm=paste(url2[i],mouse,sep='/')
  m=read.table(fm,header=T,row.names=1,sep='\t')
  data=rbind(data,m)
}
data$mouse_reads=data$mouse_reads/1000
data$mouse_umis=data$mouse_umis/1000
data$mouse_genes=data$mouse_genes/1000

pdf('V3_violin_high_read_umi.pdf')
ggplot(data, aes(x=platforms, y=mouse_umis, fill=platforms)) +
  geom_violin(trim=FALSE)+
  geom_boxplot(width=0.1, fill="white")+
  labs(y = "Number of transcripts (x10^3)")+
  scale_fill_brewer(palette="Blues")+
  theme_classic()+
  theme(axis.text.x=element_text(angle=45,hjust=1,vjust=1))
dev.off()

pdf('V3_violin_high_read_gene.pdf')
ggplot(data, aes(x=platforms, y=mouse_genes, fill=platforms)) +
  geom_violin(trim=FALSE)+
  geom_boxplot(width=0.1, fill="white")+
  labs(y = "Number of genes (x10^3)")+
  scale_fill_brewer(palette="Reds")+
  theme_classic()+
  theme(axis.text.x=element_text(angle=45,hjust=1,vjust=1))
dev.off()

# human mouse
depth=args[2]
human=paste('V1_vh',depth,sep='_')
human=paste(human,'.txt',sep='')
mouse=paste('V1_vm',depth,sep='_')
mouse=paste(mouse,'.txt',sep='')
datah=data.frame()
datam=data.frame()
for (i in 1:length(url2)){
  fh=paste(url2[i],human,sep='/')
  fm=paste(url2[i],mouse,sep='/')
  h=read.table(fh,header=T,row.names=1,sep='\t')
  m=read.table(fm,header=T,row.names=1,sep='\t')
  datah=rbind(datah,h)
  datam=rbind(datam,m)
}
datah$species=rep('human',dim(datah)[1])
datam$species=rep('mouse',dim(datam)[1])
datah$plot=paste('h',datah$platforms,sep='_')
datam$plot=paste('m',datam$platforms,sep='_')
names(datah)=c('reads','umis','genes','platforms','species','anno')
names(datam)=c('reads','umis','genes','platforms','species','anno')
data=rbind(datah,datam)
data$reads=data$reads/1000
data$umis=data$umis/1000
data$genes=data$genes/1000

pdf('V3_violin_hm_read_umi.pdf',width=10,height=8)
ggplot(data, aes(x=anno, y=umis, fill=species))+
  geom_violin(trim=FALSE)+
  geom_boxplot(width=0.1)+
  labs(y = "Number of transcripts (x10^3)")+
  scale_fill_brewer(palette="Blues")+
  scale_fill_manual(values=c("#E69F00", "#56B4E9"))+
  theme_classic()+
  theme(axis.text.x=element_text(angle=60,hjust=1,vjust=1))
dev.off()

pdf('V3_violin_hm_read_gene.pdf',width=10,height=8)
ggplot(data, aes(x=anno, y=genes, fill=species))+
  geom_violin(trim=FALSE)+
  geom_boxplot(width=0.1)+
  labs(y = "Number of genes (x10^3)")+
  scale_fill_brewer(palette="Reds")+
  scale_fill_manual(values=c("#E69F00", "#56B4E9"))+
  theme_classic()+
  theme(axis.text.x=element_text(angle=60,hjust=1,vjust=1))
dev.off()

