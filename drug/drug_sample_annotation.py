# !/usr/bin/env python
# -*- coding: utf-8 -*-

import re
import argparse

parser = argparse.ArgumentParser(description='生成药物刺激的细胞注释文件，从DGE中抽取cell barcode，并添加指定的样本注释\
                                              （多个DGE的注释会在原注释文件后面补充，不覆盖原注释文件）：\
                                              python drug_sample_annotation.py \
                                              -d DGE_file \
                                              -s sample_name \
                                              -a sample_annotation')

parser.add_argument('-d', '--dge', type=str, required=True, help='DGE_file')
parser.add_argument('-s', '--sample', type=str, default='', help='sample_name')
parser.add_argument('-a', '--annotation', type=str, required=True, help='sample_annotation')

args = parser.parse_args()


def dge_sample_annotation(dge_file, sample_name, sample_annotation):
    file_dge = open(dge_file, 'r')
    for line in file_dge:
        line = re.sub('\n', '', line)
        line = line.split('\t')
        cell = line[1:]
        break
    file_dge.close()
    new_cont_a = []
    if sample_name:
        for c in cell:
            new_cont_a.append(sample_name+'_'+c+'\t'+sample_annotation+'\n')
    else:
        for c in cell:
            new_cont_a.append(c+'\t'+sample_annotation+'\n')
    return new_cont_a


dge_file = args.dge
sample_name = args.sample
sample_annotation = args.annotation

try:
    f = open('drug_sample_annotation.txt', 'r')
    f.close()
except FileNotFoundError:
    check_file = 0
except PermissionError:
    print("You don't have permission to access this file.")
else:
    check_file = 1

cont_a = ''
if check_file == 1:
    file_a = open('drug_sample_annotation.txt', 'r')
    cont_a = file_a.read()
    file_a.close()
file_a = open('drug_sample_annotation.txt', 'w')
file_a.write(cont_a)
new_cont_a = dge_sample_annotation(dge_file, sample_name, sample_annotation)
for c_a in new_cont_a:
    file_a.write(c_a)
file_a.close()
