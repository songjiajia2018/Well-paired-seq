# !usr/bin/env python
# -*- coding:utf-8 -*-

# python data_expr_nor_G1G2T_sum_log.py

import re
import os
import numpy as np
from decimal import Decimal
import math


def transpose_expr(file_in, file_out):
    file_i = open(file_in, 'r')
    file_o = open(file_out, 'w')
    cont_i = file_i.readlines()
    cont_i2 = []
    for i in cont_i:
        i = re.sub('\n', '', i)
        i = i.split('\t')
        cont_i2.append(i)
    array_i = np.array(cont_i2)
    cont_o = np.transpose(array_i).tolist()
    for i in cont_o:
        line = ''
        for j in i:
            line = line+j+'\t'
        line = line[:-1]+'\n'
        file_o.write(line)
    file_i.close()
    file_o.close()
    os.system("sed -i '1s/Gene/Barcode/' %s" % file_out)


def sum_log(file_name):
    file = open(file_name, 'r')
    cont = file.readlines()
    header = cont[0]
    cont = cont[1:]
    file.close()

    prefix = re.sub('.txt', '', file_name)
    fileo = open(prefix+'_sum_log.txt', 'w')
    fileo.write(header[:-1]+'\tSUM\tLOG(SUM)\n')
    for line in cont:
        mm = line[:-1].split('\t')[1:]
        expr = []
        for m in mm:
            e = Decimal(m)
            expr.append(e)
        expr_sum = sum(expr)
        if expr_sum > 0:
            expr_log = math.log(expr_sum)
        else:
            expr_log = 0
        lineo = line[:-1]+'\t'+str(expr_sum)+'\t'+str(expr_log)+'\n'
        fileo.write(lineo)
    fileo.close()


file_in_G1 = 'data_expr_nor_G1S.txt'
file_out_G1 = 'data_expr_nor_G1ST.txt'
transpose_expr(file_in_G1, file_out_G1)
sum_log(file_out_G1)
file_in_G2 = 'data_expr_nor_G2M.txt'
file_out_G2 = 'data_expr_nor_G2MT.txt'
transpose_expr(file_in_G2, file_out_G2)
sum_log(file_out_G2)
