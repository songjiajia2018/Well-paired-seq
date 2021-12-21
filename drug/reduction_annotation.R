library(ggplot2)
library(plyr)


## read.table(tsne_result_group_annotation.txt)
  ## file_url
data <- read.table(file = "tsne_result_group_annotation.txt",  header = T, row.names= 1 )

## Scatter plot
tSNE_1 <- data$tSNE_1
tSNE_2 <- data$tSNE_2
SAMPLE_NAME <- data$SAMPLE_NAME
data2 <- data.frame(tsne_1 = tSNE_1, tsne_2 = tSNE_2, sample_name = SAMPLE_NAME)

pdf(file = "tSNE_group.pdf")
ggplot(data=data2,aes(x=tsne_1,y=tsne_2,fill=sample_name,col=sample_name))+geom_point(size=0.5)+theme_bw()+theme(panel.border=element_blank(),panel.grid.major=element_blank(),panel.grid.minor=element_blank(),axis.line=element_line(color="black"))
dev.off()


## read.table(tsne_result_sample_annotation.txt)                                                                           ## file_url
data <- read.table(file = "tsne_result_sample_annotation.txt",  header = T, row.names= 1 )

## Scatter plot
tSNE_1 <- data$tSNE_1
tSNE_2 <- data$tSNE_2
SAMPLE_NAME <- data$SAMPLE_NAME
data2 <- data.frame(tsne_1 = tSNE_1, tsne_2 = tSNE_2, sample_name = SAMPLE_NAME)

pdf(file = "tSNE_sample.pdf")
ggplot(data=data2,aes(x=tsne_1,y=tsne_2,fill=sample_name,col=sample_name))+geom_point(size=0.5)+theme_bw()+theme(panel.border=element_blank(),panel.grid.major=element_blank(),panel.grid.minor=element_blank(),axis.line=element_line(color="black"))
dev.off()


## read.table(umap_result_group_annotation.txt)
  ## file_url
data3 <- read.table(file = "umap_result_group_annotation.txt",  header = T, row.names= 1 )

## Scatter plot
UMAP_1 <- data3$UMAP_1
UMAP_2 <- data3$UMAP_2
SAMPLE_NAME <- data3$SAMPLE_NAME
data4 <- data.frame(umap_1 = UMAP_1, umap_2 = UMAP_2, sample_name = SAMPLE_NAME)

pdf(file = "UMAP_group.pdf")
ggplot(data=data4,aes(x=umap_1,y=umap_2,fill=sample_name,col=sample_name))+geom_point(size=0.5)+theme_bw()+theme(panel.border=element_blank(),panel.grid.major=element_blank(),panel.grid.minor=element_blank(),axis.line=element_line(color="black"))
dev.off()


## read.table(umap_result_sample_annotation.txt)
  ## file_url
data3 <- read.table(file = "umap_result_sample_annotation.txt",  header = T, row.names= 1 )

## Scatter plot
UMAP_1 <- data3$UMAP_1
UMAP_2 <- data3$UMAP_2
SAMPLE_NAME <- data3$SAMPLE_NAME
data4 <- data.frame(umap_1 = UMAP_1, umap_2 = UMAP_2, sample_name = SAMPLE_NAME)

pdf(file = "UMAP_sample.pdf")
ggplot(data=data4,aes(x=umap_1,y=umap_2,fill=sample_name,col=sample_name))+geom_point(size=0.5)+theme_bw()+theme(panel.border=element_blank(),panel.grid.major=element_blank(),panel.grid.minor=element_blank(),axis.line=element_line(color="black"))
dev.off()
