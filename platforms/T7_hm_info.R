
summary=read.table('merge_gene_exon_tagged_h+m.dge.summary.txt',header=T,row.names=1)
human=summary[summary$SPECIES=='human',1:3]
mouse=summary[summary$SPECIES=='mouse',4:6]

human0=human[human$HUMAN_NUM_GENIC_READS<5000,]
human10=human[human$HUMAN_NUM_GENIC_READS>=5000,]
human10=human10[human10$HUMAN_NUM_GENIC_READS<15000,]
human20=human[human$HUMAN_NUM_GENIC_READS>=15000,]
human20=human20[human20$HUMAN_NUM_GENIC_READS<25000,]
human30=human[human$HUMAN_NUM_GENIC_READS>=25000,]
human30=human30[human30$HUMAN_NUM_GENIC_READS<35000,]
human40=human[human$HUMAN_NUM_GENIC_READS>=35000,]
human40=human40[human40$HUMAN_NUM_GENIC_READS<45000,]
human50=human[human$HUMAN_NUM_GENIC_READS>=45000,]
human50=human50[human50$HUMAN_NUM_GENIC_READS<55000,]
human60=human[human$HUMAN_NUM_GENIC_READS>=55000,]
human60=human60[human60$HUMAN_NUM_GENIC_READS<65000,]
human70=human[human$HUMAN_NUM_GENIC_READS>=65000,]
human70=human60[human60$HUMAN_NUM_GENIC_READS<75000,]
human80=human[human$HUMAN_NUM_GENIC_READS>=75000,]
human80=human80[human80$HUMAN_NUM_GENIC_READS<85000,]
h1=list()
h1[[1]]=human0
h1[[2]]=human10
h1[[3]]=human20
h1[[4]]=human30
h1[[5]]=human40
h1[[6]]=human50
h1[[7]]=human60
h1[[8]]=human70
h1[[9]]=human80

human0=human[human$HUMAN_NUM_GENIC_READS<25000,]
human25=human[human$HUMAN_NUM_GENIC_READS>=0,]
human25=human25[human25$HUMAN_NUM_GENIC_READS<50000,]
human50=human[human$HUMAN_NUM_GENIC_READS>=25000,]
human50=human50[human50$HUMAN_NUM_GENIC_READS<75000,]
human100=human[human$HUMAN_NUM_GENIC_READS>=75000,]
human100=human100[human100$HUMAN_NUM_GENIC_READS<125000,]
human150=human[human$HUMAN_NUM_GENIC_READS>=125000,]
human150=human150[human150$HUMAN_NUM_GENIC_READS<175000,]
human200=human[human$HUMAN_NUM_GENIC_READS>=175000,]
human200=human200[human200$HUMAN_NUM_GENIC_READS<225000,]
h2=list()
h2[[1]]=human0
h2[[2]]=human25
h2[[3]]=human50
h2[[4]]=human100
h2[[5]]=human150
h2[[6]]=human200

vhuman25=human[human$HUMAN_NUM_GENIC_READS>=5000,]
vhuman25=vhuman25[vhuman25$HUMAN_NUM_GENIC_READS<45000,]
vhuman30=human[human$HUMAN_NUM_GENIC_READS>=10000,]
vhuman30=vhuman30[vhuman30$HUMAN_NUM_GENIC_READS<50000,]
vhuman35=human[human$HUMAN_NUM_GENIC_READS>=15000,]
vhuman35=vhuman35[vhuman35$HUMAN_NUM_GENIC_READS<55000,]
vhuman40=human[human$HUMAN_NUM_GENIC_READS>=20000,]
vhuman40=vhuman40[vhuman40$HUMAN_NUM_GENIC_READS<60000,]
vhuman100=human[human$HUMAN_NUM_GENIC_READS>=75000,]
vhuman100=vhuman100[vhuman100$HUMAN_NUM_GENIC_READS<125000,]
vhuman150=human[human$HUMAN_NUM_GENIC_READS>=125000,]
vhuman150=vhuman150[vhuman150$HUMAN_NUM_GENIC_READS<175000,]
vhuman200=human[human$HUMAN_NUM_GENIC_READS>=175000,]
vhuman200=vhuman200[vhuman200$HUMAN_NUM_GENIC_READS<225000,]
vh=list()
vh[[1]]=vhuman25
vh[[2]]=vhuman30
vh[[3]]=vhuman35
vh[[4]]=vhuman40
vh[[5]]=vhuman100
vh[[6]]=vhuman150
vh[[7]]=vhuman200


mouse0=mouse[mouse$MOUSE_NUM_GENIC_READS<5000,]
mouse10=mouse[mouse$MOUSE_NUM_GENIC_READS>=5000,]
mouse10=mouse10[mouse10$MOUSE_NUM_GENIC_READS<15000,]
mouse20=mouse[mouse$MOUSE_NUM_GENIC_READS>=15000,]
mouse20=mouse20[mouse20$MOUSE_NUM_GENIC_READS<25000,]
mouse30=mouse[mouse$MOUSE_NUM_GENIC_READS>=25000,]
mouse30=mouse30[mouse30$MOUSE_NUM_GENIC_READS<35000,]
mouse40=mouse[mouse$MOUSE_NUM_GENIC_READS>=35000,]
mouse40=mouse40[mouse40$MOUSE_NUM_GENIC_READS<45000,]
mouse50=mouse[mouse$MOUSE_NUM_GENIC_READS>=45000,]
mouse50=mouse50[mouse50$MOUSE_NUM_GENIC_READS<55000,]
mouse60=mouse[mouse$MOUSE_NUM_GENIC_READS>=55000,]
mouse60=mouse60[mouse60$MOUSE_NUM_GENIC_READS<65000,]
mouse70=mouse[mouse$MOUSE_NUM_GENIC_READS>=65000,]
mouse70=mouse60[mouse60$MOUSE_NUM_GENIC_READS<75000,]
mouse80=mouse[mouse$MOUSE_NUM_GENIC_READS>=75000,]
mouse80=mouse80[mouse80$MOUSE_NUM_GENIC_READS<85000,]
m1=list()
m1[[1]]=mouse0
m1[[2]]=mouse10
m1[[3]]=mouse20
m1[[4]]=mouse30
m1[[5]]=mouse40
m1[[6]]=mouse50
m1[[7]]=mouse60
m1[[8]]=mouse70
m1[[9]]=mouse80

mouse0=mouse[mouse$MOUSE_NUM_GENIC_READS<25000,]
mouse25=mouse[mouse$MOUSE_NUM_GENIC_READS>=0,]
mouse25=mouse25[mouse25$MOUSE_NUM_GENIC_READS<50000,]
mouse50=mouse[mouse$MOUSE_NUM_GENIC_READS>=25000,]
mouse50=mouse50[mouse50$MOUSE_NUM_GENIC_READS<75000,]
mouse100=mouse[mouse$MOUSE_NUM_GENIC_READS>=75000,]
mouse100=mouse100[mouse100$MOUSE_NUM_GENIC_READS<125000,]
mouse150=mouse[mouse$MOUSE_NUM_GENIC_READS>=125000,]
mouse150=mouse150[mouse150$MOUSE_NUM_GENIC_READS<175000,]
mouse200=mouse[mouse$MOUSE_NUM_GENIC_READS>=175000,]
mouse200=mouse200[mouse200$MOUSE_NUM_GENIC_READS<225000,]
m2=list()
m2[[1]]=mouse0
m2[[2]]=mouse25
m2[[3]]=mouse50
m2[[4]]=mouse100
m2[[5]]=mouse150
m2[[6]]=mouse200

vmouse25=mouse[mouse$MOUSE_NUM_GENIC_READS>=5000,]
vmouse25=vmouse25[vmouse25$MOUSE_NUM_GENIC_READS<45000,]
vmouse30=mouse[mouse$MOUSE_NUM_GENIC_READS>=10000,]
vmouse30=vmouse30[vmouse30$MOUSE_NUM_GENIC_READS<50000,]
vmouse35=mouse[mouse$MOUSE_NUM_GENIC_READS>=15000,]
vmouse35=vmouse35[vmouse35$MOUSE_NUM_GENIC_READS<55000,]
vmouse40=mouse[mouse$MOUSE_NUM_GENIC_READS>=20000,]
vmouse40=vmouse40[vmouse40$MOUSE_NUM_GENIC_READS<60000,]
vmouse100=mouse[mouse$MOUSE_NUM_GENIC_READS>=75000,]
vmouse100=vmouse100[vmouse100$MOUSE_NUM_GENIC_READS<125000,]
vmouse150=mouse[mouse$MOUSE_NUM_GENIC_READS>=125000,]
vmouse150=vmouse150[vmouse150$MOUSE_NUM_GENIC_READS<175000,]
vmouse200=mouse[mouse$MOUSE_NUM_GENIC_READS>=175000,]
vmouse200=vmouse200[vmouse200$MOUSE_NUM_GENIC_READS<225000,]
vm=list()
vm[[1]]=vmouse25
vm[[2]]=vmouse30
vm[[3]]=vmouse35
vm[[4]]=vmouse40
vm[[5]]=vmouse100
vm[[6]]=vmouse150
vm[[7]]=vmouse200


label1=c('0','10','20','30','40','50','60','70','80')
label2=c('0','25','50','100','150','200')
vlabel=c('25','30','35','40','100','150','200')

# 1 or 2
h=h2
m=m2
label=label2

out=data.frame()
for (i in 1:length(m)){
    tmp=colMeans(m[[i]])
    out=rbind(out,tmp)
}
names(out)=c('MOUSE_NUM_GENIC_READS','MOUSE_NUM_TRANSCRIPTS','MOUSE_NUM_GENES')
out$platforms=rep(names(table(summary$SAMPLE_NAME)),length(m))
write.table(out,'R7_mouse_line.txt',col.names=T,row.names=F,sep='\t')

for (i in 1:length(h)){
    tmp2=h[[i]]
    tmp2$platforms=rep(names(table(summary$SAMPLE_NAME)),dim(tmp2)[1])
    oname=paste('R7_human_',label[i],sep='')
    oname=paste(oname,'.txt',sep='')
    write.table(tmp2,oname,row.names=T,col.names=T,sep='\t')
}
for (i in 1:length(m)){
    tmp2=m[[i]]
    tmp2$platforms=rep(names(table(summary$SAMPLE_NAME)),dim(tmp2)[1])
    oname=paste('R7_mouse_',label[i],sep='')
    oname=paste(oname,'.txt',sep='')
    write.table(tmp2,oname,row.names=T,col.names=T,sep='\t')
}

# v
for (i in 1:length(vh)){
    tmp2=vh[[i]]
    tmp2$platforms=rep(names(table(summary$SAMPLE_NAME)),dim(tmp2)[1])
    oname=paste('R7_vhuman_',vlabel[i],sep='')
    oname=paste(oname,'.txt',sep='')
    write.table(tmp2,oname,row.names=T,col.names=T,sep='\t')
}
for (i in 1:length(vm)){
    tmp2=vm[[i]]
    tmp2$platforms=rep(names(table(summary$SAMPLE_NAME)),dim(tmp2)[1])
    oname=paste('R7_vmouse_',vlabel[i],sep='')
    oname=paste(oname,'.txt',sep='')
    write.table(tmp2,oname,row.names=T,col.names=T,sep='\t')
}
