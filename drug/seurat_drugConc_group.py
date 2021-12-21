# !usr/bin/env python
# -*- coding:utf-8 -*-

# 按给药浓度（实际样本）找marker，需要给seurat新的group（分群）信息
# 实现方法：从drug_sample_annotation.txt提取每个barcode对应的给药浓度
# 	从cell_identity.txt获取seurat中barcode的顺序
# python seurat_drugConc_group.py drug_sample_annotation.txt cell_identity.txt

import sys

filea = open(sys.argv[1], 'r')
dicta = {}
for i in filea:
    i = i[:-1].split('\t')
    bc = 'X'+i[0]
    sa = i[1]
    dicta[bc] = sa
filea.close()

filec = open(sys.argv[2], 'r')
listc = []
for i in filec:
    c = i.split('\t')[0]
    listc.append(c)
filec.close()

file_out = open('seurat_drugConc_group.txt', 'w')
file_out.write('barcode\tsample_annotation\n')
for cell in listc:
    file_out.write(cell+'\t'+dicta[cell]+'\n')
file_out.close()

