# ！usr/bin/env python
# -*- coding:utf-8 -*-

# python inf_clu_dose.py -i phenoData.txt
# (phenoData.txt: header = 'barcode\tcluster\tdrug_conc')

from collections import defaultdict, Counter
import os
import argparse

parser = argparse.ArgumentParser(description='统计每个cluster包含的不同给药浓度的细胞数目/占比: \
                                              python inf_clu_dose.py \
                                              -i phenoData.txt')

parser.add_argument('-i', '--inp', type=str, required=True, help='phenoData.txt')

args = parser.parse_args()

filei = open(args.inp, 'r')
conti = filei.readlines()
conti = conti[1:]
dict_clu = defaultdict(Counter)
for i in conti:
    m = i[:-1].split('\t')
    clu = m[1]
    samp = m[2]
    dict_clu[clu][samp] += 1
dict_clu = dict(dict_clu)
filei.close()

fileo = open('inf_clu_dose.txt', 'w')
fileo.write('Cluster\tDose(nM)\tCount\tTotal_Count\tProportion\n')
for k, v in dict_clu.items():
    v = dict(v)
    total_count = 0
    for c in v.values():
        total_count = total_count + int(c)
    for d, c in v.items():
        p = int(c)/float(total_count)
        fileo.write(str(k)+'\t'+str(d)+'\t'+str(c)+'\t'+str(total_count)+'\t'+str(p)+'\n')
fileo.close()

os.system("sed -i 's/\t0nM/\ta_0/' inf_clu_dose.txt")
os.system("sed -i 's/\t100nM/\tb_100/' inf_clu_dose.txt")
os.system("sed -i 's/\t1uM/\tc_1000/' inf_clu_dose.txt")
os.system("sed -i 's/\t10uM/\td_10000/' inf_clu_dose.txt")

os.system("sed -i 's/cluster0\t/C_cluster0\t/' inf_clu_dose.txt")
os.system("sed -i 's/cluster1\t/A_cluster1\t/' inf_clu_dose.txt")
os.system("sed -i 's/cluster2\t/D_cluster2\t/' inf_clu_dose.txt")
os.system("sed -i 's/cluster3\t/B_cluster3\t/' inf_clu_dose.txt")

