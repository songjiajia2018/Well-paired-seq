
summary=read.table('merge_gene_exon_tagged_h+m.dge.summary.txt',header=T,row.names=1)
human=summary[summary$SPECIES=='human',1:3]
mouse=summary[summary$SPECIES=='mouse',4:6]

human0=human[human$HUMAN_NUM_GENIC_READS<10000,]
human20=human[human$HUMAN_NUM_GENIC_READS>=10000,]
human20=human20[human20$HUMAN_NUM_GENIC_READS<30000,]
human40=human[human$HUMAN_NUM_GENIC_READS>=30000,]
human40=human40[human40$HUMAN_NUM_GENIC_READS<50000,]
human60=human[human$HUMAN_NUM_GENIC_READS>=50000,]
human60=human60[human60$HUMAN_NUM_GENIC_READS<70000,]
human80=human[human$HUMAN_NUM_GENIC_READS>=70000,]
human80=human80[human80$HUMAN_NUM_GENIC_READS<90000,]
human100=human[human$HUMAN_NUM_GENIC_READS>=90000,]
human100=human100[human100$HUMAN_NUM_GENIC_READS<110000,]
human150=human[human$HUMAN_NUM_GENIC_READS>=140000,]
human150=human150[human150$HUMAN_NUM_GENIC_READS<160000,]
human200=human[human$HUMAN_NUM_GENIC_READS>=190000,]
human200=human200[human200$HUMAN_NUM_GENIC_READS<210000,]
h1=list()
h1[[1]]=human0
h1[[2]]=human20
h1[[3]]=human40
h1[[4]]=human60
h1[[5]]=human80
h1[[6]]=human100
h1[[7]]=human150
h1[[8]]=human200

mouse0=mouse[mouse$MOUSE_NUM_GENIC_READS<10000,]
mouse20=mouse[mouse$MOUSE_NUM_GENIC_READS>=10000,]
mouse20=mouse20[mouse20$MOUSE_NUM_GENIC_READS<30000,]
mouse40=mouse[mouse$MOUSE_NUM_GENIC_READS>=30000,]
mouse40=mouse40[mouse40$MOUSE_NUM_GENIC_READS<50000,]
mouse60=mouse[mouse$MOUSE_NUM_GENIC_READS>=50000,]
mouse60=mouse60[mouse60$MOUSE_NUM_GENIC_READS<70000,]
mouse80=mouse[mouse$MOUSE_NUM_GENIC_READS>=70000,]
mouse80=mouse80[mouse80$MOUSE_NUM_GENIC_READS<90000,]
mouse100=mouse[mouse$MOUSE_NUM_GENIC_READS>=90000,]
mouse100=mouse100[mouse100$MOUSE_NUM_GENIC_READS<110000,]
mouse150=mouse[mouse$MOUSE_NUM_GENIC_READS>=140000,]
mouse150=mouse150[mouse150$MOUSE_NUM_GENIC_READS<160000,]
mouse200=mouse[mouse$MOUSE_NUM_GENIC_READS>=190000,]
mouse200=mouse200[mouse200$MOUSE_NUM_GENIC_READS<210000,]
m1=list()
m1[[1]]=mouse0
m1[[2]]=mouse20
m1[[3]]=mouse40
m1[[4]]=mouse60
m1[[5]]=mouse80
m1[[6]]=mouse100
m1[[7]]=mouse150
m1[[8]]=mouse200

m=m1
out=data.frame()
for (i in 1:length(m)){
    tmp=colMeans(m[[i]])
    out=rbind(out,tmp)
}
names(out)=c('MOUSE_NUM_GENIC_READS','MOUSE_NUM_TRANSCRIPTS','MOUSE_NUM_GENES')
out$platforms=rep(names(table(summary$SAMPLE_NAME)),length(m))
write.table(out,'R1_mouse_line.txt',col.names=T,row.names=F,sep='\t')

label=c('0','20','40','60','80','100','150','200')
for (i in 1:length(h1)){
    tmp2=h1[[i]]
    tmp2$platforms=rep(names(table(summary$SAMPLE_NAME)),dim(tmp2)[1])
    oname=paste('R1_human_',label[i],sep='')
    oname=paste(oname,'.txt',sep='')
    write.table(tmp2,oname,row.names=T,col.names=T,sep='\t')
}
for (i in 1:length(m1)){
    tmp2=m1[[i]]
    tmp2$platforms=rep(names(table(summary$SAMPLE_NAME)),dim(tmp2)[1])
    oname=paste('R1_mouse_',label[i],sep='')
    oname=paste(oname,'.txt',sep='')
    write.table(tmp2,oname,row.names=T,col.names=T,sep='\t')
}

