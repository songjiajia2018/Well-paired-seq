# !usr/bin/env python
# -*- coding:utf-8 -*-

# python readorUMI_gene_cells.py summary.txt sample_name

import sys
import matplotlib as mpl
mpl.use('Agg')
import matplotlib.pyplot as plt


# read_gene.pdf
def read_gene(list_sum, sample_name):
    reads = []
    genes = []
    for i in list_sum:
        read = int(i[1])
        gene = int(i[3])
        reads.append(read)
        genes.append(gene)

    x = reads
    y = genes
    plt.figure(figsize=(8, 8))
    plt.scatter(x, y, color='black', s=15)
    ax = plt.gca()
    ax.spines['right'].set_color('none')
    ax.spines['top'].set_color('none')
    ax.spines['bottom'].set_linewidth(2)
    ax.spines['left'].set_linewidth(2)
    max_reads = int(max(reads))
    max_genes = int(max(genes))
    lim_reads = max_reads+10000
    lim_genes = max_genes+250
    plt.xlim(-5000, lim_reads)
    plt.ylim(-100, lim_genes)
    plt.xticks(fontsize=12)
    plt.yticks(fontsize=12)
    plt.xlabel('reads per cell', fontsize=16)
    plt.ylabel('genes per cell', fontsize=16)
    plt.title(sample_name, fontsize=18)
    plt.savefig(sample_name+'_read_gene.pdf')
    plt.close()


# transcript_gene.pdf
def transcript_gene(list_sum, sample_name):
    umis = []
    genes = []
    for i in list_sum:
        umi = int(i[2])
        gene = int(i[3])
        umis.append(umi)
        genes.append(gene)

    x = umis
    y = genes
    plt.figure(figsize=(8, 8))
    plt.scatter(x, y, color='black', s=15)
    ax = plt.gca()
    ax.spines['right'].set_color('none')
    ax.spines['top'].set_color('none')
    ax.spines['bottom'].set_linewidth(2)
    ax.spines['left'].set_linewidth(2)
    max_umis = int(max(umis))
    max_genes = int(max(genes))
    lim_umis = max_umis+1500
    lim_genes = max_genes+500
    plt.xlim(-500, lim_umis)
    plt.ylim(-250, lim_genes)
    plt.xticks(fontsize=12)
    plt.yticks(fontsize=12)
    plt.xlabel('transcripts per cell', fontsize=16)
    plt.ylabel('genes per cell', fontsize=16)
    plt.title(sample_name, fontsize=18)
    plt.savefig(sample_name+'_transcript_gene.pdf')
    plt.close()


file = open(sys.argv[1], 'r')
cont = file.readlines()
list_sum = []
for line in cont:
    if line.startswith('#') or line == '\n':
        continue
    else:
        line = line.rstrip()
        line = line.split('\t')
        list_sum.append(line)
file.close()

list_sum = list_sum[1:]
sample_name = sys.argv[2]
read_gene(list_sum, sample_name)
transcript_gene(list_sum, sample_name)
