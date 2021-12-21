args=commandArgs(T)

# 最大深度
max_d=as.numeric(args[1])
## max_d=300000

# 折线图区间
l_by=as.numeric(args[2])
## l_by=10000
l_by=as.numeric(l_by)
l_s=l_by/2
l_e=max_d-l_by/2
seql=seq(l_s, max_d, l_by)
namel=seq(0, l_e, l_by)
namel=as.character(namel)

# 小提琴图区间
v_by=as.numeric(args[3])
v_low=as.numeric(args[4])
v_high=as.numeric(args[5])
## v_by=30000
## v_low=35000
## v_high=200000

v_by=as.numeric(v_by)
v_low_s=v_low-v_by/2
v_low_e=v_low+v_by/2
v_high_s=v_high-v_by/2
v_high_e=v_high+v_by/2
namev=c(v_low/1000, v_high/1000)
namev=as.character(namev)

# summary文件读入
summary_file = args[6]
## summary_file = 'merge_gene_exon_tagged_h+m.dge.summary.txt'
summary=read.table(summary_file,header=T,row.names=1)
human=summary[summary$SPECIES=='human',1:3]
mouse=summary[summary$SPECIES=='mouse',4:6]

# 折线图人鼠数据
hl=list()
for (i in 1:length(seql)){
  if (i==1){
    s = 0
    e = seql[i]
  }else{
    s = seql[(i-1)]
    e = seql[i]
  }
  human_tmp=human[human$HUMAN_NUM_GENIC_READS>=s,]
  human_tmp=human_tmp[human_tmp$HUMAN_NUM_GENIC_READS<e,]
  hl[[i]] = human_tmp
}

ml=list()
for (i in 1:length(seql)){
  if (i==1){
    s = 0
    e = seql[i]
  }else{
    s = seql[(i-1)]
    e = seql[i]
  }
  mouse_tmp=mouse[mouse$MOUSE_NUM_GENIC_READS>=s,]
  mouse_tmp=mouse_tmp[mouse_tmp$MOUSE_NUM_GENIC_READS<e,]
  ml[[i]] = mouse_tmp
}

# 输出折线图鼠数据
out=data.frame()
for (i in 1:length(ml)){
    tmp=colMeans(ml[[i]])
    out=rbind(out,tmp)
}
names(out)=c('mouse_reads','mouse_umis','mouse_genes')
out$depth=namel
out$platforms=rep(names(table(summary$SAMPLE_NAME)),length(ml))
write.table(out,'V1_mouse_line.txt',col.names=T,row.names=F,sep='\t')


# 小提琴图人鼠数据
human_low=human[human$HUMAN_NUM_GENIC_READS>=v_low_s,]
human_low=human_low[human_low$HUMAN_NUM_GENIC_READS<v_low_e,]
human_high=human[human$HUMAN_NUM_GENIC_READS>=v_high_s,]
human_high=human_high[human_high$HUMAN_NUM_GENIC_READS<v_high_e,]

mouse_low=mouse[mouse$MOUSE_NUM_GENIC_READS>=v_low_s,]
mouse_low=mouse_low[mouse_low$MOUSE_NUM_GENIC_READS<v_low_e,]
mouse_high=mouse[mouse$MOUSE_NUM_GENIC_READS>=v_high_s,]
mouse_high=mouse_high[mouse_high$MOUSE_NUM_GENIC_READS<v_high_e,]

vdata=list(human_low, human_high, mouse_low, mouse_high)

# 输出小提琴图人鼠数据
for (i in 1:length(vdata)){
    tmp2=vdata[[i]]
    names(tmp2)=c('mouse_reads','mouse_umis','mouse_genes')
    tmp2$platforms=rep(names(table(summary$SAMPLE_NAME)),dim(tmp2)[1])
    if (i == 1){
    oname=paste('V1_vh_',namev[1],sep='')
    }
    if (i == 2){
    oname=paste('V1_vh_',namev[2],sep='')
    }
    if (i == 3){
    oname=paste('V1_vm_',namev[1],sep='')
    }
    if (i == 4){
    oname=paste('V1_vm_',namev[2],sep='')
    }
    oname=paste(oname,'.txt',sep='')
    write.table(tmp2,oname,row.names=T,col.names=T,sep='\t')
}

