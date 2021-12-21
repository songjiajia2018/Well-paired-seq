# ！usr/bin/env python
# -*- coding:utf-8 -*-

# python inf_pseudodose_dose.py -i pseudotime_pData_sample.txt/pseudotime_pData_cell.txt -b bin_num
# (pseudotime_pData_sample/cell_PseudodoseBin.txt
#  inf_pseudodose_dose_sample/cell.txt: header = 'PseudodoseBin	Dose(nM)	Count	Total_Count	Proportion')

import re
import os
import math
from decimal import Decimal
from interval import Interval
from collections import defaultdict, Counter
import argparse

parser = argparse.ArgumentParser(description='统计不同轨迹分段(bin)中不同给药浓度细胞的数量/占比: \
                                              python inf_pseudodose_dose.py \
                                              -i pseudotime_pData_sample.txt/pseudotime_pData_cell.txt \
                                              -b bin_num')

parser.add_argument('-i', '--inp', type=str, required=True, help='pseudotime_pData_sample.txt/pseudotime_pData_cell.txt')
parser.add_argument('-b', '--bin_num', type=int, required=True, help='bin_num')

args = parser.parse_args()

inp = args.inp
if 'cell' in inp:
    flag = 'c'
elif 'sample' in inp:
    flag = 's'
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
    listp.append(Decimal(m[4]))
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

# 确定每个细胞所在的bin
conto = []
for i in conti:
    m = i[:-1].split(' ')
    p = float(m[4])
    for k, v in dict_bin.items():
        if p in v:
            line = i[:-1]+' '+str(k)+'\n'
    conto.append(line)
if flag == 's':
    fileo = open('pseudotime_pData_sample_PseudodoseBin'+str(bn)+'.txt', 'w')
elif flag == 'c':
    fileo = open('pseudotime_pData_cell_PseudodoseBin'+str(bn)+'.txt', 'w')
fileo.write('barcode '+line1+' PseudodoseBin\n')
for o in conto:
    fileo.write(o)
fileo.close()

# 统计不同bin中不同给药浓度细胞的数量/占比
if flag == 's':
    fileii = open('pseudotime_pData_sample_PseudodoseBin'+str(bn)+'.txt', 'r')
elif flag == 'c':
    fileii = open('pseudotime_pData_cell_PseudodoseBin'+str(bn)+'.txt', 'r')
contii = fileii.readlines()
contii = contii[1:]
dict_b = defaultdict(Counter)
for i in contii:
    m = i[:-1].split(' ')
    b = m[-1]
    dose = m[2]
    dict_b[b][dose] += 1
dict_b = dict(dict_b)
fileii.close()

if flag == 's':
    fileoo = open('inf_pseudodose'+str(bn)+'_dose_sample.txt', 'w')
elif flag == 'c':
    fileoo = open('inf_pseudodose'+str(bn)+'_dose_cell.txt', 'w')
fileoo.write('PseudodoseBin\tDose(nM)\tCount\tTotal_Count\tProportion\n')
for k, v in dict_b.items():
    v = dict(v)
    total_count = 0
    for c in v.values():
        total_count = total_count + int(c)
    for d, c in v.items():
        p = int(c)/float(total_count)
        fileoo.write(str(k)+'\t'+str(d)+'\t'+str(c)+'\t'+str(total_count)+'\t'+str(p)+'\n')
fileoo.close()

# 更改dose表示形式
if flag == 's':
    os.system("sed -i 's/\t0nM/\ta_0/' inf_pseudodose%s_dose_sample.txt" % str(bn))
    os.system("sed -i 's/\t100nM/\tb_100/' inf_pseudodose%s_dose_sample.txt" % str(bn))
    os.system("sed -i 's/\t1uM/\tc_1000/' inf_pseudodose%s_dose_sample.txt" % str(bn))
    os.system("sed -i 's/\t10uM/\td_10000/' inf_pseudodose%s_dose_sample.txt" % str(bn))
elif flag == 'c':
    os.system("sed -i 's/\t0nM/\ta_0/' inf_pseudodose%s_dose_cell.txt" % str(bn))
    os.system("sed -i 's/\t100nM/\tb_100/' inf_pseudodose%s_dose_cell.txt" % str(bn))
    os.system("sed -i 's/\t1uM/\tc_1000/' inf_pseudodose%s_dose_cell.txt" % str(bn))
    os.system("sed -i 's/\t10uM/\td_10000/' inf_pseudodose%s_dose_cell.txt" % str(bn))
