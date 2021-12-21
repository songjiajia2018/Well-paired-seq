library(ggplot2)
library(plyr)

## read.table(umap_result_G1G2.txt)
  ## file_url
data1 <- read.table(file = "umap_result_G1G2.txt",  header = T, row.names= 1)

## Scatter plot
UMAP_1 <- data1$UMAP_1
UMAP_2 <- data1$UMAP_2
Log_G1G2 <- data1$Log_G1G2
data2 <- data.frame(umap_1 = UMAP_1, umap_2 = UMAP_2, Proliferation_Index = Log_G1G2)

pdf(file = "UMAP_sample_G1G2.pdf")
ggplot(data=data2,aes(x=umap_1,y=umap_2,color=Proliferation_Index))+geom_point(size=0.5)+scale_color_gradient(low="blue",high="#FEE357")+theme_bw()+theme(panel.border=element_blank(),panel.grid.major=element_blank(),panel.grid.minor=element_blank(),axis.line=element_line(color="black"))
dev.off()

