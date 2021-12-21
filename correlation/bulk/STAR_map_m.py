# -*- coding: utf-8 -*-
"""
Created on Thu Jul  1 10:30:47 2021

@author: 牧木
"""

# 目录下的测序文件需同为single或paired，本脚本处理不了混合数据

import Levenshtein
import os
import re
import sys
import datetime
from collections import defaultdict
import argparse

parser = argparse.ArgumentParser(description='STAR mapping: \
                                              python STAR_map.py \
                                              -t y/n \
                                              -l p/s \
                                              -s STAR \
                                              -g gtf \
                                              -n thread')

parser.add_argument('-t', '--trim_before_star', type=str, default='y',
                    help='whether the fq processed by trim_before_STAR.py already? y for yes, n for no. Defalut: y')
parser.add_argument('-l', '--layout', type=str, default='p', help='LibraryLayout: \
                    s for single, p for paired. Default: p')
parser.add_argument('-s', '--star', type=str, default='/home/songjia/newdisk/YK/reference/mm10/STAR', help='STAR index directory')
parser.add_argument('-g', '--gtf', type=str, default='/home/songjia/newdisk/YK/reference/mm10/mm10.gtf', help='gtf file')
parser.add_argument('-n', '--thread', type=str, default='10', help='thread used in STAR. Default: 10.')

args = parser.parse_args()


def tag_sample(string):
    if string.endswith('.fq'):
        tag = 'fq'
        sample = re.sub('.fq', '', string)
    elif string.endswith('.fastq'):
        tag = 'fastq'
        sample = re.sub('.fastq', '', string)
    elif string.endswith('.fa'):
        tag = 'fa'
        sample = re.sub('.fa', '', string)
    elif string.endswith('.fasta'):
        tag = 'fasta'
        sample = re.sub('.fasta', '', string)
    return(tag, sample)


def tag_sample2(str1, str2):
    if trim == 'y':
        str1 = re.sub('_repair_1', '', str1)
        str2 = re.sub('_repair_2', '', str2)
    if str1.endswith('.fq'):
        tag = 'fq'
    elif str1.endswith('.fastq'):
        tag = 'fastq'
    elif str1.endswith('.fa'):
        tag = 'fa'
    elif str1.endswith('.fasta'):
        tag = 'fasta'
    ss1 = list(str1)
    ss2 = list(str2)
    for i in range(len(ss1)):
        if ss1[i] == ss2[i]:
            continue
        else:
            flag = 1
            while flag:
                n = i-1
                if ss1[n] == '_':
                    flag = 0
                elif ss1[n] == '-':
                    flag = 0
                elif ss1[n] == '.':
                    flag = 0
    sample = str1[0:n]
    return(tag, sample)


def match(list_fq):
    # 对trim后的fq名进行调整
    list_fq0 = []
    if trim == 'y':
        for i in list_fq:
            i = re.sub('_repair_1', '', i)
            i = re.sub('_repair_2', '', i)
            list_fq0.append(i)
    else:
        list_fq0 = list_fq

    # 首先，对每个fq名，找到海明距离最小的fq名列表，存入dict_fq
    dict_fq = defaultdict(list)
    for i in range(len(list_fq0)-1):
        str1 = list_fq0[i]
        dict_sim = {}
        m = range(i+1, len(list_fq0))
        for j in m:
            str2 = list_fq0[j]
            if len(str1) != len(str2):
                sim = len(list_fq0[i])
            else:
                sim = Levenshtein.hamming(str1, str2)
            dict_sim[str2] = sim
        min_sim = min(dict_sim.values())
        for k, v in dict_sim.items():
            if v == min_sim:
                dict_fq[str1].append(k)
    dict_fq = dict(dict_fq)

    # 对dict_fq的列表（值）进行处理：
    # 仅一个fq名的列表，将列表转为字符串
    # 多个fq名的列表：找到每个fq名和键fq名的差异内容及差异位点，“差异内容为1或2，且差异位点最靠后”的fq名被保留
    dict_fq2 = {}
    for k, v in dict_fq.items():
        if len(v) == 1:
            dict_fq2[k] = v[0]
        else:
            diff_index = []
            for p in v:
                kk = list(k)
                pp = list(p)
                for q in range(len(kk)):
                    if kk[q] != pp[q]:
                        if kk[q] in [1, 2, '1', '2'] and pp[q] in [1, 2, '1', '2']:
                            diff_index.append(q)
                        else:
                            diff_index.append(0)
                        break
            max_diff_index = max(diff_index)
            index = diff_index.index(max_diff_index)
            v2 = v[index]
            dict_fq2[k] = v2

    # 去重
    dict_fq3 = {}
    for k in dict_fq2.keys():
        if k in dict_fq3.keys() or k in dict_fq3.values():
            continue
        else:
            dict_fq3[k] = dict_fq2[k]

    # 判断R1和R2
    # R1为键，R2为值，保存在dict_fq4
    dict_fq4 = {}
    for k, v in dict_fq3.items():
        kk = list(k)
        vv = list(v)
        if kk.count('1') > vv.count('1'):
            dict_fq4[k] = v
        else:
            dict_fq4[v] = k

    # 将调整后的fq名改为原名
    dict_fq5 = {}
    for k, v in dict_fq4.items():
        index_k = list_fq0.index(k)
        index_v = list_fq0.index(v)
        k2 = list_fq[index_k]
        v2 = list_fq[index_v]
        dict_fq5[k2] = v2
    return(dict_fq5)


# trim_tag
trim = args.trim_before_star
if trim != 'y' and trim != 'n':
    print("The input of -t/trim should be 'y' or 'no'!!! ")
    print("Exit!!!")
    sys.exit()

# genome annotation file & thread
star_path = args.star
gtf_path = args.gtf
star_n = args.thread

# out directory
now_time = datetime.datetime.now()
time_str = now_time.strftime('%Y-%m-%d-%H_%M_%S')
star_out_path = time_str+'_star_out'
os.system('''mkdir -p ./%s''' % (star_out_path))

# fq list
os.system('''ls *.fq *.fastq *.fa *.fasta > trim_fq_tmp.txt''')

# single
if args.layout == 's' or args.layout == 'single' or args.layout == 'S' or args.layout == 'SINGLE':
    file = open('trim_fq_tmp.txt', 'r')
    for fq in file:
        fq = fq.rstrip()
        tag, sample = tag_sample(fq)
        if trim == 'y':
            sample = re.sub('_trim', '', sample)
        print('now processing: %s' % (fq))
        os.system('''STAR --runThreadN %s \
                          --genomeDir %s \
                          --sjdbGTFfile %s \
                          --outFileNamePrefix %s \
                          --outSAMunmapped Within \
                          --readFilesIn %s''' % (star_n, star_path, gtf_path, sample, fq))
        os.system('''mv %sAligned.out.sam %sLog.final.out %sLog.out %sLog.progress.out %sSJ.out.tab %s_STARgenome ./%s
                  ''' % (sample, sample, sample, sample, sample, sample, star_out_path))
    file.close()
    os.system('''rm trim_fq_tmp.txt''')

# paired
elif args.layout == 'p' or args.layout == 'paired' or args.layout == 'pair' \
  or args.layout == 'P' or args.layout == 'PAIRED' or args.layout == 'PAIR':
    list_fq = []
    dict_fq = {}
    file = open('trim_fq_tmp.txt', 'r')
    for i in file:
        i = i.rstrip()
        list_fq.append(i)
    file.close()
    os.system('''rm trim_fq_tmp.txt''')
    dict_fq = match(list_fq)

    for fq1, fq2 in dict_fq.items():
        tag, sample = tag_sample2(fq1, fq2)
        print('now processing: %s and %s' % (fq1, fq2))
        os.system('''STAR --runThreadN %s \
                          --genomeDir %s \
                          --sjdbGTFfile %s \
                          --outFileNamePrefix %s \
                          --readFilesIn %s %s''' % (star_n, star_path, gtf_path, sample, fq1, fq2))
        os.system('''mv %sAligned.out.sam %sLog.final.out %sLog.out %sLog.progress.out %sSJ.out.tab %s_STARgenome ./%s
                  ''' % (sample, sample, sample, sample, sample, sample, star_out_path))

# done
print('cut & fastqc done!!!')
