# !/usr/bin/env python
# coding=utf-8
# raw file written by linli and the script should be run under py2 envrionment
# modified by qwz for batch process purpose

import re
import numpy as np
import codecs
import argparse

parser = argparse.ArgumentParser(description='取同一测序深度，对fastq文件进行过滤： \
                                              python SameDepth_fastq.py \
                                              -fq fastq file \
                                              -d depth')

parser.add_argument('-fq', '--fastq', type=str, required=True, help='fastq file')
parser.add_argument('-d', '--depth', type=str, required=True, help='depth')

args = parser.parse_args()

count = 0
list_id = []
with open(args.fastq, 'r')as ref:
    for line in ref:
        count += 1
        if count % 4 == 1:
            tmp = line.split()[0].lstrip('@')
            list_id.append(tmp)
d = int(args.depth)
list_ID = np.random.choice(list_id, d, replace = False)
dict0 = {}
for i in list_id:
    dict0[i] = 0
for i in list_ID:
    dict0[i] = 1

file_fastq = open(args.fastq, 'r')
prefix = re.sub('.fastq','',args.fastq)
depth_str = str((d/1000000)) + 'M'
file_fastq_id = open(prefix+'_' + depth_str + 'Depth.fastq','w')
cc = 0
tag = 0
for line in file_fastq:
    cc += 1
    if cc % 4 == 1:
        tag = 0
        read_id = line.split()[0].lstrip('@')
        if dict0[read_id]:
            file_fastq_id.write(line)
            tag = 1
    else:
        if tag == 1:
            file_fastq_id.write(line)
file_fastq.close()
file_fastq_id.close()


