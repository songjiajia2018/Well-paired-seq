# ！usr/bin/env python
# -*- coding:utf-8 -*-

# python seurat_bin_group.py -i pseudotime_pData_sample.txt/pseudotime_pData_cell.txt -c cell_identity.txt -b bin_num
#  (seurat_bin_group.txt: header = 'barcode	bin')

import re
import os
import math
from decimal import Decimal
from interval import Interval
from collections import defaultdict, Counter
import argparse

parser = argparse.ArgumentParser(description='按bin找差异表达基因并输出结果，需要给seurat新的group（分群）信息: \
                                              python seurat_bin_group.py \
                                              -p pseudotime_pData_sample.txt/pseudotime_pData_cell.txt \
                                              -c cell_identity.txt \
                                              -b bin_num')

parser.add_argument('-p', '--pseudotime', type=str, required=True, help='pseudotime_pData_sample.txt/pseudotime_pData_cell.txt')
parser.add_argument('-c', '--cell_id', type=str, required=True, help='cell_identity.txt')
parser.add_argument('-b', '--bin_num', type=int, required=True, help='bin_num')

args = parser.parse_args()

inp = args.pseudotime
cell_id = args.cell_id
bn = int(args.bin_num)

# 确定各个bin的范围
# 读入伪时间坐标
filei = open(inp, 'r')
conti = filei.readlines()
cont_tmp = []
for i in conti:
    i = re.sub('"', '', i)
    cont_tmp.append(i)
conti = cont_tmp
line1 = conti[0][:-1]
conti = conti[1:]
listp = []
for i in conti:
    m = i[:-1].split(' ')
    listp.append(float(m[4]))
filei.close()
# 按照给定bin个数划分bin，保存在dict_bin
listp_min = min(listp)
listp_max = max(listp)
listp_mmin = Decimal(str(float(math.floor(listp_min))))
listp_mmax = Decimal(str(float(math.ceil(listp_max))))
inter = Decimal(str((listp_mmax-listp_mmin)/bn))
lo = listp_mmin
up = listp_mmin+inter
count = 1
dict_bin = defaultdict()
while up <= listp_mmax and count <= bn:
    if count == bn:
        dict_bin['bin'+str(count)] = Interval(lo, up)
    dict_bin['bin'+str(count)] = Interval(lo, up, upper_closed=False)
    lo = up
    up = up+inter
    count += 1
dict_bin = dict(dict_bin)

# 确定每个细胞所在的bin，保存在cell_bin={}中
cell_bin = {}
for i in conti:
    m = i[:-1].split(' ')
    bc = m[0]
    p = float(m[4])
    for k, v in dict_bin.items():
        if p in v:
            cell_bin[bc] = str(k)

# 按cell_identity.txt中的barcode顺序输出对应bin的文件
filec = open(cell_id, 'r')
contc = filec.readlines()
fileo = open('seurat_bin_group.txt', 'w')
fileo.write('barcode\tbin\n')
for line in contc:
    line = line.rstrip()
    line = line.split('\t')
    barcode = line[0]
    fileo.write(barcode+'\t'+cell_bin[barcode]+'\n')
filec.close()
fileo.close()

