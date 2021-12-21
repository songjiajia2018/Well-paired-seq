# ！usr/bin/env python
# -*- coding:utf-8 -*-

# python pheno_feature_Data.py -d data_expr.txt -s sample_drug.txt/-c cell_identity.txt
# (sample_drug.txt: "Xsample_num\tdrug"
#  cell_identity.txt: "barcode\tcluster")
# (phenoData.txt	header = '\tdrug_conc'
#  featureData.txt	header = '\tgene_short_name')

import argparse

parser = argparse.ArgumentParser(description='生成矩阵对应的phenoData.txt和featureData.txt: \
                                              python pheno_feature_Data.py \
                                              -d data_expr.txt \
                                              -s sample_drug.txt \
                                              -c cell_identity.txt')

parser.add_argument('-d', '--dge', type=str, required=True, help='data_expr.txt')
parser.add_argument('-s', '--sample', type=str, required=True, help='sample_drug.txt')
parser.add_argument('-c', '--cell', type=str, required=True, help='cell_identity.txt')

args = parser.parse_args()

file = open(args.dge, 'r')
cont = file.readlines()
barcode = cont[0][:-1]
barcode = barcode.split('\t')
gene = []
for i in cont[1:]:
    i = i.split('\t')[0]
    gene.append(i)
file.close()

file_s = open(args.sample, 'r')
cont_s = file_s.readlines()
dict_s = {}
for i in cont_s:
    i = i[:-1].split('\t')
    dict_s[i[0]] = i[1]
file_s.close()

file_c = open(args.cell, 'r')
cont_c = file_c.readlines()
dict_c = {}
for i in cont_c:
    i = i[:-1].split('\t')
    dict_c[i[0]] = i[1]
file_c.close()

file_p = open('phenoData.txt', 'w')
file_p.write('\tcluster\tdrug_conc\n')
for b in barcode:
    samp = b.split('_')[0]
    conc = dict_s[samp]
    clu = dict_c[b]
    file_p.write(b+'\tcluster'+clu+'\t'+conc+'\n')
file_p.close()

file_f = open('featureData.txt', 'w')
file_f.write('\tgene_short_name\n')
for g in gene:
    file_f.write(g+'\t'+g+'\n')
file_f.close()
