# !/usr/bin/env python
# -*- coding: utf-8 -*-

import re
import argparse

parser = argparse.ArgumentParser(description='在tSNE/UMAP降维坐标信息后添加细胞注释信息：\
                                              python reduction_annotation.py \
                                              -r reduction_tSNE/UMAP_embeddings \
                                              -a sample_annotation \
                                              -t Y/N')

parser.add_argument('-r', '--reduction', type=str, required=True, help='reduction_tSNE/UMAP_embeddings_output')
parser.add_argument('-a', '--annotation', type=str, default='drug_sample_annotation.txt', help='sample_annotation file. e.g. drug_sample_annotation.txt/drug_group_annotation.txt')
parser.add_argument('-t', '--tag', type=str, default='N', help='Y/N: Did you add "sample_name"tag to cell_barcode?')

args = parser.parse_args()


## 将cell_barcode和其注释信息储存在dict_annotation中
file_annotation = open(args.annotation, 'r')
dict_annotation = {}
if (args.tag == 'Y') or (args.tag == 'Yes') or (args.tag == 'YES'):
    for i in file_annotation:
        i = re.sub('\n', '', i)
        i = i.split('\t')
        dict_annotation['X'+i[0]] = i[1]
elif (args.tag == 'N') or (args.tag == 'No') or (args.tag == 'NO'):
    for i in file_annotation:
        i = re.sub('\n', '', i)
        i = i.split('\t')
        dict_annotation[i[0]] = i[1]
file_annotation.close()

## 读入tSNE/UMAP降维坐标
prefix = re.sub('.txt', '', args.reduction)
file_reduction = open(args.reduction, 'r')
cont_reduction = file_reduction.readlines()

## 在原列名后加一个新的列名'SAMPLE_NAME'
file_reduction_annotation = open(prefix+'_annotation.txt', 'w')
col_name = re.sub('\n', '', cont_reduction[0])
file_reduction_annotation.write(col_name+' SAMPLE_NAME\n')

## 在tSNE/UMAP降维坐标信息后添加细胞注释信息
cont_reduction = cont_reduction[1:]
for i in cont_reduction:
    i = re.sub('\n', '', i)
    i2 = i.split(' ')
    cn = i2[0]
    if cn not in dict_annotation:
        cn = cn.split('.')
        cn = cn[0]
    anno = dict_annotation[cn]
    line = i+' '+anno+'\n'
    file_reduction_annotation.write(line)
file_reduction.close()
file_reduction_annotation.close()
