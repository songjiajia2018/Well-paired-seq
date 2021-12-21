library(ggplot2)
library(plyr)

##read.table(h+m.dge.summary.txt)
  ##file_url, lim_y
data <- read.table(file = "merge_gene_exon_tagged_h+m.dge.summary.txt",  header = T, row.names= 1 )

##gene_violin.pdf
GENES <- data$HUMAN_NUM_GENES + data$MOUSE_NUM_GENES
SAMPLE <- data$SAMPLE_NAME
lim_y <- max(GENES) + 100
data2 <- data.frame(sample = SAMPLE, genes = GENES)

  ##file_name, title, x, ylim()
pdf(file = "YK007_gene_violin.pdf")
ggplot(data2, aes(x=sample, y=genes, fill=sample)) +  
  geom_violin(adjust =1, trim=TRUE, color="black", size = 0.75) + 
  scale_fill_manual(values = c("#F8766D"))+ 
  geom_jitter(size = 2.5)+
  labs(title = "YK007", x = "YK007", y = "genes", fill = NULL)+
  ylim(100,lim_y)+
  theme_bw()+ 
  theme(plot.title = element_text(size = 18, face = "plain", hjust = 0.5, colour = "black"),
        axis.line = element_line(size = 1, colour = "black"),
        axis.text.x = element_text(size = 12, face = "plain", hjust = 0.5, colour = "black"), 
        axis.text.y = element_text(size = 12, face = "plain", hjust = 0.5, colour = "black"), 
        axis.title.x = element_blank(),
        axis.title.y = element_text(size = 16, face = "plain", hjust = 0.5, colour = "black"),
        legend.position = "none",
        panel.border = element_blank(),
        panel.grid.major = element_blank(),
        panel.grid.minor = element_blank())
dev.off()

##human_mouse_gene_violin.pdf
GENES <- data$HUMAN_NUM_GENES + data$MOUSE_NUM_GENES
SPECIES <- data$SPECIES
lim_y <- max(GENES) + 100
data3 <- data.frame(species = SPECIES, genes = GENES)

  ##file_name, title, x, ylim()
pdf(file = "YK007_human_mouse_gene_violin.pdf")
ggplot(data3, aes(x=species, y=genes, fill=species)) +
  geom_violin(adjust =1, trim=TRUE, color="black", size = 0.75) +
  scale_fill_manual(values = c("#F8766D", "#00BFC4"))+
  geom_boxplot(width=0.2, size = 0.75, outlier.size = 2.5, position=position_dodge(0.9))+
  labs(title = "YK007", x = "YK007", y = "genes", fill = NULL)+
  ylim(100,lim_y)+
  theme_bw()+
  theme(plot.title = element_text(size = 18, face = "plain", hjust = 0.5, colour = "black"),
        axis.line = element_line(size = 1, colour = "black"),
        axis.text.x = element_text(size = 12, face = "plain", hjust = 0.5, colour = "black"),
        axis.text.y = element_text(size = 12, face = "plain", hjust = 0.5, colour = "black"),
        axis.title.x = element_blank(),
        axis.title.y = element_text(size = 16, face = "plain", hjust = 0.5, colour = "black"),
        legend.position = "none",
        panel.border = element_blank(),
        panel.grid.major = element_blank(),
        panel.grid.minor = element_blank())
dev.off()

##transcript_violin.pdf
UMIS <- data$HUMAN_NUM_TRANSCRIPTS + data$MOUSE_NUM_TRANSCRIPTS
SAMPLE <- data$SAMPLE_NAME
lim_y <- max(UMIS) + 250
data4 <- data.frame(sample = SAMPLE, umis = UMIS)

  ##file_name, title, x, ylim()
pdf(file = "YK007_transcript_violin.pdf")
ggplot(data4, aes(x=sample, y=umis, fill=sample)) +
  geom_violin(adjust =1, trim=TRUE, color="black", size = 0.75) +
  scale_fill_manual(values = c("#F8766D"))+
  geom_jitter(size = 2.5)+
  labs(title = "YK007", x = "YK007", y = "transcripts", fill = NULL)+
  ylim(250,lim_y)+
  theme_bw()+
  theme(plot.title = element_text(size = 18, face = "plain", hjust = 0.5, colour = "black"),
        axis.line = element_line(size = 1, colour = "black"),
        axis.text.x = element_text(size = 12, face = "plain", hjust = 0.5, colour = "black"),
        axis.text.y = element_text(size = 12, face = "plain", hjust = 0.5, colour = "black"),
        axis.title.x = element_blank(),
        axis.title.y = element_text(size = 16, face = "plain", hjust = 0.5, colour = "black"),
        legend.position = "none",
        panel.border = element_blank(),
        panel.grid.major = element_blank(),
        panel.grid.minor = element_blank())
dev.off()

##human_mouse_transcript_violin
UMIS <- data$HUMAN_NUM_TRANSCRIPTS + data$MOUSE_NUM_TRANSCRIPTS
SPECIES <- data$SPECIES
lim_y <- max(UMIS) + 250
data5 <- data.frame(species = SPECIES, umis = UMIS)

  ##file_name, title, x, ylim()
pdf(file = "YK007_human_mouse_transcript_violin.pdf")
ggplot(data5, aes(x=species, y=umis, fill=species)) +
  geom_violin(adjust =1, trim=TRUE, color="black", size = 0.75) +
  scale_fill_manual(values = c("#F8766D", "#00BFC4"))+
  geom_boxplot(width=0.2, size = 0.75, outlier.size = 2.5, position=position_dodge(0.9))+
  labs(title = "YK007", x = "YK007", y = "transcripts", fill = NULL)+
  ylim(250,lim_y)+
  theme_bw()+
  theme(plot.title = element_text(size = 18, face = "plain", hjust = 0.5, colour = "black"),
        axis.line = element_line(size = 1, colour = "black"),
        axis.text.x = element_text(size = 12, face = "plain", hjust = 0.5, colour = "black"),
        axis.text.y = element_text(size = 12, face = "plain", hjust = 0.5, colour = "black"),
        axis.title.x = element_blank(),
        axis.title.y = element_text(size = 16, face = "plain", hjust = 0.5, colour = "black"),
        legend.position = "none",
        panel.border = element_blank(),
        panel.grid.major = element_blank(),
        panel.grid.minor = element_blank())
dev.off()




