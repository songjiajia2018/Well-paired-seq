# !/usr/bin/env python
# coding=utf-8

import re
import numpy as np
import argparse

parser = argparse.ArgumentParser(description='取同一测序深度，fastq取同一深度，对reads进行过滤： \
                                              python SameDepth.py \
                                              -f *.fastq \
                                              -s *.sam \
                                              -d depth')

parser.add_argument('-f', '--fastq', type=str, required=True, help='fastq file')
parser.add_argument('-s', '--sam', type=str, required=True, help='sam file')
parser.add_argument('-d', '--depth', type=str, required=True, help='depth')

args = parser.parse_args()



file_fq = open(args.fastq, 'r')
cont_fq = file_fq.readlines()
nn = 0
nn_max = len(cont_fq)
pattern = r'@(.*?)\s'
list_id = []
while (nn<nn_max):
    if nn%4==0:
        idid = re.match(pattern, cont_fq[nn])
        list_id.append(idid.group(1))
    nn = nn+1
d = int(args.depth)
list_ID = np.random.choice(list_id, d, replace = False)
dict0 = {}
for i in list_id:
    dict0[i] = 0
for i in list_ID:
    dict0[i] = 1
file_fq.close()

file_align = open(args.sam, 'r')
prefix = re.sub('.sam','',args.sam)
depth_str = str((d/1000000)) + 'M'
file_align_id = open(prefix+'_' + depth_str + 'Depth.sam','w')
for line in file_align:
    if line.startswith('@'):
        file_align_id.write(line)
    else:
        ll = line.split('\t')
        if dict0[ll[0]]:
            file_align_id.write(line)
file_align.close()
file_align_id.close()

