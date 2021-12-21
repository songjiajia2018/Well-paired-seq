# !usr/bin/env python
# -*- coding:utf-8 -*-

import re
import pandas as pd
from decimal import Decimal
import argparse

parser = argparse.ArgumentParser(description='在降维坐标信息后添加proliferation index注释信息: \
                                              python reduction_G1G2_proliferation_index.py \
                                              -r reduction.txt')

parser.add_argument('-r', '--reduction', type=str, nargs='+', help='reduction.txt')

args = parser.parse_args()


def barcode_log(file_name):
    file = pd.read_csv(file_name, sep='\t', encoding='utf-8')
    barcode = file['Barcode']
    log_sum = file['LOG(SUM)']
    barcode = list(barcode)
    log_sum = list(log_sum)
    dict0 = {}
    for i in range(0, len(barcode)):
        dict0[barcode[i]] = log_sum[i]
    return dict0


dictG1 = barcode_log('data_expr_nor_G1ST_sum_log.txt')
dictG2 = barcode_log('data_expr_nor_G2MT_sum_log.txt')

list_red = args.reduction
if list_red is None:
    list_red = ['umap_result.txt']
for red in list_red:
    file_red = open(red, 'r')
    cont_red = file_red.readlines()
    header = cont_red[0].rstrip()
    cont_red = cont_red[1:]
    file_red.close()

    prefix = re.sub('.txt', '', red)
    file_out = open(prefix+'_G1G2.txt', 'w')
    if ' ' in header:
        file_out.write(header+' Log_G1S Log_G2M Log_G1G2\n')
    elif '\t' in header:
        file_out.write(header+'\tLog_G1S\tLog_G2M\tLog_G1G2\n')
    for line in cont_red:
        line_out = ''
        line = line.rstrip()
        if ' ' in line:
            result = re.match(r'(.*?) ', line)
            bc = result.group(1)
            Log_G1G2 = Decimal(dictG1[bc])+Decimal(dictG2[bc])
            line_out = line+' '+str(dictG1[bc])+' '+str(dictG2[bc])+' '+str(Log_G1G2)+'\n'
        elif '\t' in line:
            result = re.match(r'(.*?)\t', line)
            bc = result.group(1)
            Log_G1G2 = Decimal(dictG1[bc])+Decimal(dictG2[bc])
            line_out = line+'\t'+str(dictG1[bc])+'\t'+str(dictG2[bc])+'\t'+str(Log_G1G2)+'\n'
        file_out.write(line_out)
    file_out.close()
