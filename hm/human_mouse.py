#!/usr/bin/env python
#coding=utf-8

import re
import codecs
import numpy as np
import matplotlib as mpl
mpl.use('Agg')
import matplotlib.pyplot as plt
import argparse

parser = argparse.ArgumentParser(description='python human_mouse.py \
                                              -H human.dge.summary.txt \
                                              -M mouse.dge.summary.txt \
                                              -SM sample_name \
                                              -TR threshold_reads_number \
                                              -TU threshold_transcripts_number')

parser.add_argument('-H', '--human', type=str, required=True, help='human.dge.summary.txt')
parser.add_argument('-M', '--mouse', type=str, required=True, help='mouse.dge.summary.txt')
parser.add_argument('-SM', '--sample_name', type=str, required=True, help='sample_name or sample_number')
parser.add_argument('-TR', '--threshold_reads', type=str, default='0', help='threshold_reads_number, either -TR or -TU is required')
parser.add_argument('-TU', '--threshold_umis', type=str, default='0', help='threshold_transcripts_number, either -TR or -TU is required')

args = parser.parse_args()

##human+mouse --> list_merge
file_human=open(args.human,'r')
file_mouse=open(args.mouse,'r')
sample_name=args.sample_name
TR=int(args.threshold_reads)
TU=int(args.threshold_umis)
cont_human=file_human.readlines()
cont_mouse=file_mouse.readlines()
info_human=cont_human[7:-2]
info_mouse=cont_mouse[7:-2]
list_human=[]
list_mouse=[]
for i in info_human:
    i2=re.sub('\n','',i)
    i3=i2.split('\t')
    list_human.append(i3)
for i in info_mouse:
    i2=re.sub('\n','',i)
    i3=i2.split('\t')
    list_mouse.append(i3)
list_merge=[['CELL_BARCODE', 'HUMAN_NUM_GENIC_READS', 'HUMAN_NUM_TRANSCRIPTS', 'HUMAN_NUM_GENES', 'MOUSE_NUM_GENIC_READS', 'MOUSE_NUM_TRANSCRIPTS', 'MOUSE_NUM_GENES', 'SPECIES','SAMPLE_NAME']]+list_human
for m in list_mouse:
    bc=m[0]
    info=m[1:]
    n=0
    while (n < len(list_merge)):
        if (bc in list_merge[n]):
            list_merge[n]=list_merge[n]+info
        n=n+1
file_human.close()
file_mouse.close()

##species tag & sample_name
rnum=len(list_merge)
r=1
while (r < rnum):
    human=int(list_merge[r][2])
    mouse=int(list_merge[r][5])
    total=float(human+mouse)
    total_reads=int(list_merge[r][1])+int(list_merge[r][4])
    if (total <= TU) or (total_reads <= TR):
        list_merge[r]=list_merge[r]+['grey']
    else:
        p_human=float(human/total)
        p_mouse=float(mouse/total)
        if (p_human >= 0.9):
            list_merge[r]=list_merge[r]+['human']
        elif (p_mouse >= 0.9):
            list_merge[r]=list_merge[r]+['mouse']
        else:
            list_merge[r]=list_merge[r]+['mix']
    list_merge[r]=list_merge[r]+[sample_name]
    r=r+1
arr_merge=np.array(list_merge)

##merge_gene_exon_tagged_clean.dge.summary.txt
##merge_gene_exon_tagged_h+m.dge.summary.txt
file_merge_c=codecs.open('merge_gene_exon_tagged_clean.dge.summary.txt','w')
for l in list_merge:
    if ('grey' not in l):
        line=''
        for i in l:
            line=line+i+'\t'
        line2=line[:-1]
        file_merge_c.write(line2+'\n')
file_merge_c.close()

file_merge_hm=codecs.open('merge_gene_exon_tagged_h+m.dge.summary.txt','w')
for l in list_merge:
    if ('grey' not in l) and ('mix' not in l):
        line=''
        for i in l:
            line=line+i+'\t'
        line2=line[:-1]
        file_merge_hm.write(line2+'\n')
file_merge_hm.close()

##human_mouse_transcript.pdf
def human_mouse_transcript(list_merge, sample_name):
    umis_human_human=[]
    umis_human_mouse=[]
    umis_mouse_human=[]
    umis_mouse_mouse=[]
    umis_mix_human=[]
    umis_mix_mouse=[]
    umis_grey_human=[]
    umis_grey_mouse=[]
    r=1
    while (r < rnum):
        if (list_merge[r][7] == 'human'):
            umis_human_human.append(int(list_merge[r][2]))
            umis_human_mouse.append(int(list_merge[r][5]))
        elif (list_merge[r][7] == 'mouse'):
            umis_mouse_human.append(int(list_merge[r][2]))
            umis_mouse_mouse.append(int(list_merge[r][5]))
        elif (list_merge[r][7] == 'mix'):
            umis_mix_human.append(int(list_merge[r][2]))
            umis_mix_mouse.append(int(list_merge[r][5]))
        elif (list_merge[r][7] == 'grey'):
            umis_grey_human.append(int(list_merge[r][2]))
            umis_grey_mouse.append(int(list_merge[r][5]))
        r=r+1
    
    x1=umis_human_human
    y1=umis_human_mouse
    Human_count=len(umis_human_human)
    Human_label='HUMAN('+str(Human_count)+')'
    x2=umis_mouse_human
    y2=umis_mouse_mouse
    Mouse_count=len(umis_mouse_mouse)
    Mouse_label='MOUSE('+str(Mouse_count)+')'
    x3=umis_mix_human
    y3=umis_mix_mouse
    Mix_count=len(umis_mix_human)
    Mix_label='MIX('+str(Mix_count)+')'
    x4=umis_grey_human
    y4=umis_grey_mouse
    plt.figure(figsize=(8,8))
    plt.scatter(x3, y3, color = '#32CD32', s = 40, label = Mix_label)
    plt.scatter(x2, y2, color = 'blue', s = 40, label = Mouse_label)
    plt.scatter(x1, y1, color = 'red',s = 40, label = Human_label)
    plt.scatter(x4, y4, color = '#C0C0C0', s = 40)
    ax = plt.gca()
    ax.spines['right'].set_color('none')
    ax.spines['top'].set_color('none')
    ax.spines['bottom'].set_linewidth(2)
    ax.spines['left'].set_linewidth(2)
    handles, labels = ax.get_legend_handles_labels()
    ax.legend(handles[::-1], labels[::-1], loc = 'best', fontsize=18, frameon=False)
    if umis_human_human:
        max_human=int(max(umis_human_human))
    else:
        max_human=0
    if umis_mouse_mouse:
        max_mouse=int(max(umis_mouse_mouse))
    else:
        max_mouse=0
    if (max_human >= max_mouse):
        lim=max_human+1000
    else:
        lim=max_mouse+1000
    plt.xlim(-500, lim)
    plt.ylim(-500, lim)
    plt.xticks(fontsize=12)
    plt.yticks(fontsize=12)
    plt.xlabel('HUMAN transcripts', fontsize=18)
    plt.ylabel('MOUSE transcripts', fontsize=18)
    plt.title(sample_name+' with 90%',fontsize=18)
    plt.savefig(sample_name+'_human_mouse_transcript.pdf')
    plt.close()

##human_mouse_read.pdf
def human_mouse_read(list_merge, sample_name):
    reads_human_human=[]
    reads_human_mouse=[]
    reads_mouse_human=[]
    reads_mouse_mouse=[]
    reads_mix_human=[]
    reads_mix_mouse=[]
    reads_grey_human=[]
    reads_grey_mouse=[]
    r=1
    while (r < rnum):
        if (list_merge[r][7] == 'human'):
            reads_human_human.append(int(list_merge[r][1]))
            reads_human_mouse.append(int(list_merge[r][4]))
        elif (list_merge[r][7] == 'mouse'):
            reads_mouse_human.append(int(list_merge[r][1]))
            reads_mouse_mouse.append(int(list_merge[r][4]))
        elif (list_merge[r][7] == 'mix'):
            reads_mix_human.append(int(list_merge[r][1]))
            reads_mix_mouse.append(int(list_merge[r][4]))
        elif (list_merge[r][7] == 'grey'):
            reads_grey_human.append(int(list_merge[r][1]))
            reads_grey_mouse.append(int(list_merge[r][4]))
        r=r+1

    x1=reads_human_human
    y1=reads_human_mouse
    Human_count=len(reads_human_human)
    Human_label='HUMAN('+str(Human_count)+')'
    x2=reads_mouse_human
    y2=reads_mouse_mouse
    Mouse_count=len(reads_mouse_mouse)
    Mouse_label='MOUSE('+str(Mouse_count)+')'
    x3=reads_mix_human
    y3=reads_mix_mouse
    Mix_count=len(reads_mix_human)
    Mix_label='MIX('+str(Mix_count)+')'
    x4=reads_grey_human
    y4=reads_grey_mouse
    plt.figure(figsize=(8,8))
    plt.scatter(x3, y3, color = '#32CD32', s = 40, label = Mix_label)
    plt.scatter(x2, y2, color = 'blue', s = 40, label = Mouse_label)
    plt.scatter(x1, y1, color = 'red',s = 40, label = Human_label)
    plt.scatter(x4, y4, color = '#C0C0C0', s = 40)
    ax = plt.gca()
    ax.spines['right'].set_color('none')
    ax.spines['top'].set_color('none')
    ax.spines['bottom'].set_linewidth(2)
    ax.spines['left'].set_linewidth(2)
    handles, labels = ax.get_legend_handles_labels()
    ax.legend(handles[::-1], labels[::-1], loc = 'best',fontsize=18, frameon=False)
    if reads_human_human:
        max_human=int(max(reads_human_human))
    else:
        max_human=0
    if reads_mouse_mouse:
        max_mouse=int(max(reads_mouse_mouse))
    else:
        max_mouse=0
    if (max_human >= max_mouse):
        lim=max_human+5000
    else:
        lim=max_mouse+5000
    plt.xlim(-2500, lim)
    plt.ylim(-2500, lim)
    plt.xticks(fontsize=11)
    plt.yticks(fontsize=11)
    plt.xlabel('HUMAN reads', fontsize=16)
    plt.ylabel('MOUSE reads', fontsize=16)
    plt.title(sample_name+' with 90%', fontsize=18)
    plt.savefig(sample_name+'_human_mouse_read.pdf')
    plt.close()

##human_mouse_gene.pdf
def human_mouse_gene(list_merge, sample_name):
    genes_human=[]
    genes_mouse=[]
    r=1
    while (r < rnum):
        if (list_merge[r][7] == 'human') or (list_merge[r][7] == 'mouse') or (list_merge[r][7] == 'mix'):
            genes_human.append(int(list_merge[r][3]))
            genes_mouse.append(int(list_merge[r][6]))
        r=r+1

    x=genes_human
    y=genes_mouse
    plt.figure(figsize=(8,8))
    plt.scatter(x, y, color = 'black', s = 15)
    ax = plt.gca()
    ax.spines['right'].set_color('none')
    ax.spines['top'].set_color('none')
    ax.spines['bottom'].set_linewidth(2)
    ax.spines['left'].set_linewidth(2)
    if genes_human:
        max_human=int(max(genes_human))
    else:
        max_human=0
    if genes_mouse:
        max_mouse=int(max(genes_mouse))
    else:
        max_mouse=0
    if (max_human >= max_mouse):
        lim=max_human+200
    else:
        lim=max_mouse+200 
    plt.xlim(-200, lim)
    plt.ylim(-200, lim)
    plt.xticks(fontsize=12)
    plt.yticks(fontsize=12)
    plt.xlabel('HUMAN genes', fontsize=16)
    plt.ylabel('MOUSE genes', fontsize=16)
    plt.title(sample_name, fontsize=18)
    plt.savefig(sample_name+'_human_mouse_gene.pdf')
    plt.close()

##read_per_cell.pdf
def read_per_cell(list_merge, sample_name):
    reads=[]
    r=1
    while (r < rnum):
        if (list_merge[r][7] == 'human') or (list_merge[r][7] == 'mouse') or (list_merge[r][7] == 'mix'):
            read=int(list_merge[r][1])+int(list_merge[r][4])
            reads.append(read)
        r=r+1
    reads2=sorted(reads)
    stamps=range(1,len(reads2)+1)
    
    x=stamps
    y=reads2
    plt.figure(figsize=(8,8))
    plt.scatter(x, y, color = 'black', s = 15)
    ax = plt.gca()
    ax.spines['right'].set_color('none')
    ax.spines['top'].set_color('none')
    ax.spines['bottom'].set_linewidth(2)
    ax.spines['left'].set_linewidth(2)
    max_stamps=int(max(stamps))
    max_reads=int(max(reads2))
    lim_stamps=max_stamps+30
    lim_reads=max_reads+15000
    plt.xlim(-200, lim_stamps)
    plt.ylim(-4000, lim_reads)
    plt.xticks(fontsize=11)
    plt.yticks(fontsize=11)
    plt.xlabel('STAMPs(ordered by amount of reads)', fontsize=16)
    plt.ylabel('reads per cell', fontsize=16)
    plt.title(sample_name, fontsize=18)
    plt.savefig(sample_name+'_read_per_cell.pdf')
    plt.close()

    plt.figure(figsize=(8,8))
    plt.scatter(x, y, color = 'black', s = 15)
    ax = plt.gca()
    ax.spines['right'].set_color('none')
    ax.spines['top'].set_color('none')
    ax.spines['bottom'].set_linewidth(2)
    ax.spines['left'].set_linewidth(2)
    plt.xlim(-10, 100)          
    plt.ylim(-1000, 10000)
    plt.xticks(fontsize=11)
    plt.yticks(fontsize=11)
    plt.xlabel('STAMPs(ordered by amount of reads)', fontsize=16)
    plt.ylabel('reads per cell', fontsize=16)
    plt.title(sample_name, fontsize=18)
    plt.savefig(sample_name+'_read_per_cell_100.pdf')
    plt.close()

##transcript_per_cell.pdf
def transcript_per_cell(list_merge, sample_name):
    umis=[]
    r=1
    while (r < rnum):
        if (list_merge[r][7] == 'human') or (list_merge[r][7] == 'mouse') or (list_merge[r][7] == 'mix'):
            umi=int(list_merge[r][2])+int(list_merge[r][5])
            umis.append(umi)
        r=r+1
    umis2=sorted(umis)
    stamps=range(1,len(umis2)+1)

    x=stamps
    y=umis2
    plt.figure(figsize=(8,8))
    plt.scatter(x, y, color = 'black', s = 15)
    ax = plt.gca()
    ax.spines['right'].set_color('none')
    ax.spines['top'].set_color('none')
    ax.spines['bottom'].set_linewidth(2)
    ax.spines['left'].set_linewidth(2)
    max_stamps=int(max(stamps))
    max_umis=int(max(umis2))
    lim_stamps=max_stamps+30
    lim_umis=max_umis+5000
    plt.xlim(-300, lim_stamps)
    plt.ylim(-300, lim_umis)
    plt.xticks(fontsize=11)
    plt.yticks(fontsize=11)
    plt.xlabel('STAMPs(ordered by amount of reads)', fontsize=16)
    plt.ylabel('transcripts per cell', fontsize=16)
    plt.title(sample_name, fontsize=18)
    plt.savefig(sample_name+'_transcript_per_cell.pdf')
    plt.close()

    plt.figure(figsize=(8,8))
    plt.scatter(x, y, color = 'black', s = 15)
    ax = plt.gca()
    ax.spines['right'].set_color('none')
    ax.spines['top'].set_color('none')
    ax.spines['bottom'].set_linewidth(2)
    ax.spines['left'].set_linewidth(2)
    plt.xlim(-30, 150)
    plt.ylim(-30, 1000)
    plt.xticks(fontsize=11)
    plt.yticks(fontsize=11)
    plt.xlabel('STAMPs(ordered by amount of reads)', fontsize=16)
    plt.ylabel('transcripts per cell', fontsize=16)
    plt.title(sample_name, fontsize=18)
    plt.savefig(sample_name+'_transcript_per_cell_150.pdf')
    plt.close()

##transcript_violin.pdf
def transcript_violin(list_merge, sample_name):
    umis=[]
    r=1
    while (r < rnum):
        if (list_merge[r][7] == 'human') or (list_merge[r][7] == 'mouse') or (list_merge[r][7] == 'mix'):
            umi=int(list_merge[r][2])+int(list_merge[r][5])
            umis.append(umi)
        r=r+1
    plt.figure(figsize=(8,8))
    violin = plt.violinplot(umis, widths=0.5, showmeans=False, showmedians=False, showextrema=False)
    for patch in violin['bodies']:
        patch.set_facecolor('#FA8072')
        patch.set_edgecolor('black')
        patch.set_alpha(1)
    ax = plt.gca()
    ax.spines['right'].set_color('none')
    ax.spines['top'].set_color('none')
    ax.spines['bottom'].set_linewidth(2)
    ax.spines['left'].set_linewidth(2)
    plt.xticks(fontsize=12)
    plt.yticks(fontsize=12)
    plt.xticks([1], [sample_name])
    plt.xlabel('', fontsize=16)
    plt.ylabel('transcripts', fontsize=16)
    plt.title(sample_name,fontsize=18)
    plt.savefig(sample_name+'_transcript_violin.pdf')
    plt.close()

##gene_violin.pdf
def gene_violin(list_merge, sample_name):
    genes=[]
    r=1
    while (r < rnum):
        if (list_merge[r][7] == 'human') or (list_merge[r][7] == 'mouse') or (list_merge[r][7] == 'mix'):
            gene=int(list_merge[r][3])+int(list_merge[r][6])
            genes.append(gene)
        r=r+1

    plt.figure(figsize=(8,8))
    violin = plt.violinplot(genes, widths=0.5, showmeans=False, showmedians=False, showextrema=False)
    for patch in violin['bodies']:
        patch.set_facecolor('#FA8072')
        patch.set_edgecolor('black')
        patch.set_alpha(1)
    ax = plt.gca()
    ax.spines['right'].set_color('none')
    ax.spines['top'].set_color('none')
    ax.spines['bottom'].set_linewidth(2)
    ax.spines['left'].set_linewidth(2)
    plt.xticks(fontsize=12)
    plt.yticks(fontsize=12)
    plt.xticks([1], [sample_name])
    plt.xlabel('', fontsize=16)
    plt.ylabel('genes', fontsize=16)
    plt.title(sample_name,fontsize=18)
    plt.savefig(sample_name+'_gene_violin.pdf')
    plt.close()

##human_mouse_transcript_violin.pdf
def human_mouse_transcript_violin(list_merge, sample_name):
    human_umis=[]
    mouse_umis=[]
    r=1
    while (r < rnum):
        if (list_merge[r][7] == 'human'):
            human_umi=int(list_merge[r][2])+int(list_merge[r][5])
            human_umis.append(human_umi)
        if (list_merge[r][7] == 'mouse'):
            mouse_umi=int(list_merge[r][2])+int(list_merge[r][5])
            mouse_umis.append(mouse_umi)
        r=r+1
    umis=[human_umis, mouse_umis]
    
    plt.figure(figsize=(8,8))
    violin = plt.violinplot(umis, showmeans=False, showmedians=False, showextrema=False)
    #boxprops = dict(linewidth=2) 
    medianprops = dict(linewidth=2, color='black')
    plt.boxplot(umis, sym='ko', showcaps=False, medianprops=medianprops)
    for patch in violin['bodies']:
        patch.set_facecolor('#FA8072')
        patch.set_edgecolor('black')      
        patch.set_alpha(1)
    ax = plt.gca()
    ax.spines['right'].set_color('none')
    ax.spines['top'].set_color('none')
    ax.spines['bottom'].set_linewidth(2)
    ax.spines['left'].set_linewidth(2)
    plt.xticks(fontsize=12)
    plt.yticks(fontsize=12)
    plt.xticks([1,2], ['human','mouse'])
    plt.xlabel('', fontsize=16)
    plt.ylabel('transcripts', fontsize=16)
    plt.title(sample_name,fontsize=18)
    plt.savefig(sample_name+'_human_mouse_transcript_violin.pdf')
    plt.close()

##human_mouse_gene_violin.pdf
def human_mouse_gene_violin(list_merge, sample_name):
    human_genes=[]
    mouse_genes=[]
    r=1
    while (r < rnum):
        if (list_merge[r][7] == 'human'):
            human_gene=int(list_merge[r][3])+int(list_merge[r][6])
            human_genes.append(human_gene)
        if (list_merge[r][7] == 'mouse'):
            mouse_gene=int(list_merge[r][3])+int(list_merge[r][6])
            mouse_genes.append(mouse_gene)
        r=r+1
    genes=[human_genes, mouse_genes]

    plt.figure(figsize=(8,8))
    violin = plt.violinplot(genes, showmeans=False, showmedians=False, showextrema=False)
    #boxprops = dict(linewidth=2)
    medianprops = dict(linewidth=2, color='black')
    plt.boxplot(genes, sym='ko', showcaps=False, medianprops=medianprops)
    for patch in violin['bodies']:
        patch.set_facecolor('#FA8072')
        patch.set_edgecolor('black')
        patch.set_alpha(1)
    ax = plt.gca()
    ax.spines['right'].set_color('none')
    ax.spines['top'].set_color('none')
    ax.spines['bottom'].set_linewidth(2)
    ax.spines['left'].set_linewidth(2)
    plt.xticks(fontsize=12)
    plt.yticks(fontsize=12)
    plt.xticks([1,2], ['human','mouse'])
    plt.xlabel('', fontsize=16)
    plt.ylabel('genes', fontsize=16)
    plt.title(sample_name,fontsize=18)
    plt.savefig(sample_name+'_human_mouse_gene_violin.pdf')
    plt.close()

##read_gene.pdf
def read_gene(list_merge, sample_name):
    reads=[]
    genes=[]
    r=1
    while (r < rnum):
        if (list_merge[r][7] == 'human') or (list_merge[r][7] == 'mouse') or (list_merge[r][7] == 'mix'):
            read=int(list_merge[r][1])+int(list_merge[r][4])
            reads.append(read)
            gene=int(list_merge[r][3])+int(list_merge[r][6])
            genes.append(gene)
        r=r+1

    x=reads
    y=genes
    plt.figure(figsize=(8,8))
    plt.scatter(x, y, color = 'black', s = 15)
    ax = plt.gca()
    ax.spines['right'].set_color('none')
    ax.spines['top'].set_color('none')
    ax.spines['bottom'].set_linewidth(2)
    ax.spines['left'].set_linewidth(2)
    max_reads=int(max(reads))
    max_genes=int(max(genes))
    lim_reads=max_reads+10000
    lim_genes=max_genes+250
    plt.xlim(-5000, lim_reads)
    plt.ylim(-100, lim_genes)
    plt.xticks(fontsize=12)
    plt.yticks(fontsize=12)
    plt.xlabel('reads per cell', fontsize=16)
    plt.ylabel('genes per cell', fontsize=16)
    plt.title(sample_name, fontsize=18)
    plt.savefig(sample_name+'_read_gene.pdf')
    plt.close()

##transcript_gene.pdf
def transcript_gene(list_merge, sample_name):
    umis=[]
    genes=[]
    r=1
    while (r < rnum):
        if (list_merge[r][7] == 'human') or (list_merge[r][7] == 'mouse') or (list_merge[r][7] == 'mix'):
            umi=int(list_merge[r][2])+int(list_merge[r][5])
            umis.append(umi)
            gene=int(list_merge[r][3])+int(list_merge[r][6])
            genes.append(gene)
        r=r+1

    x=umis
    y=genes
    plt.figure(figsize=(8,8))
    plt.scatter(x, y, color = 'black', s = 15)
    ax = plt.gca()
    ax.spines['right'].set_color('none')
    ax.spines['top'].set_color('none')
    ax.spines['bottom'].set_linewidth(2)
    ax.spines['left'].set_linewidth(2)
    max_umis=int(max(umis))
    max_genes=int(max(genes))
    lim_umis=max_umis+1500
    lim_genes=max_genes+500
    plt.xlim(-500, lim_umis)
    plt.ylim(-250, lim_genes)
    plt.xticks(fontsize=12)
    plt.yticks(fontsize=12)
    plt.xlabel('transcripts per cell', fontsize=16)
    plt.ylabel('genes per cell', fontsize=16)
    plt.title(sample_name, fontsize=18)
    plt.savefig(sample_name+'_transcript_gene.pdf')
    plt.close()


human_mouse_transcript(list_merge, sample_name)
human_mouse_read(list_merge, sample_name)
human_mouse_gene(list_merge, sample_name)
read_per_cell(list_merge, sample_name)
transcript_per_cell(list_merge, sample_name)
#transcript_violin(list_merge, sample_name)
#gene_violin(list_merge, sample_name)
#human_mouse_transcript_violin(list_merge, sample_name)
#human_mouse_gene_violin(list_merge, sample_name)
read_gene(list_merge, sample_name)
transcript_gene(list_merge, sample_name)
