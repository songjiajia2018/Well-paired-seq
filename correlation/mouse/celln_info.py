# -*- coding: utf-8 -*-
"""
Created on Wed Sep  1 00:41:46 2021

@author: 牧木
"""

import pandas as pd
import numpy as np
import os

num = 100
fn = 'out_gene_exon_tagged_3000.dge.summary.txt'

bc = []
file = open('mouse_bc.txt', 'r')
for i in file:
    i = i.rstrip()
    bc.append(i)
file.close()
BC = np.random.choice(bc, num, replace=False)
BC = list(BC)

fr = open('out_cell_readcounts.txt', 'r')
cr = fr.readlines()
fr.close()
dr = {}
for i in cr:
    if i.startswith('#'):
        continue
    else:
        i = i.rstrip().split('\t')
        dr[i[1]] = int(i[0])

fm = open(fn, 'r')
cm = fm.read()
fm.close()
if cm.startswith('#'):
    os.system('bash ccat.sh %s' % (fn))
    m = pd.read_csv(fn+'.tmp', sep='\t', encoding='utf-8')
    os.system('rm %s.tmp' % (fn))
else:
    m = pd.read_csv(fn+'.tmp', sep='\t', encoding='utf-8')

n = m[(m['CELL_BARCODE'].isin(BC))]
n['NUM_READS'] = n['CELL_BARCODE'].apply(lambda x: dr[x])
n.loc['SUM'] = n.apply(lambda x: x.sum())
n.loc['SUM', 'CELL_BARCODE'] = 'NULL'
out = 'celln_info_'+str(num)+'.txt'
print(n.loc['SUM'])
n.to_csv(out, sep='\t')

