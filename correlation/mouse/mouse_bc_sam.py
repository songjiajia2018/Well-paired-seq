# -*- coding: utf-8 -*-
"""
Created on Tue Aug 31 02:24:02 2021

@author: 牧木
"""

# mouse_bc_sam.py summary.txt TU sam

import os
import re
import sys
import pandas as pd


#fn = sys.argv[1]
#TU = int(sys.argv[2])
#raw_sam = sys.argv[3]
fn = 'out_gene_exon_tagged_3000.dge.summary.txt'
TU = 500
raw_sam = 'my_clean.sam'

fm = open(fn, 'r')
cm = fm.read()
fm.close()
if cm.startswith('#'):
    os.system('bash ccat.sh %s' % (fn))
    m = pd.read_csv(fn+'.tmp', sep='\t', encoding='utf-8')
    os.system('rm %s.tmp' % (fn))
else:
    m = pd.read_csv(fn+'.tmp', sep='\t', encoding='utf-8')

fr = open('out_cell_readcounts.txt', 'r')
cr = fr.readlines()
fr.close()
lbc = []
nn = 2750
cc = 0
for i in cr:
    if i.startswith('#'):
        continue
    else:
        bc = i.rstrip().split('\t')[1]
        lbc.append(bc)
        cc = cc+1
        if (cc == nn):
            break

mm = m[(m['CELL_BARCODE'].isin(lbc))]
mmm = mm[(mm['NUM_TRANSCRIPTS'] >= TU)]
lbc = list(mmm['CELL_BARCODE'])
fbc = open('mouse_bc.txt', 'w')
fbc.write('\n'.join(lbc))
fbc.close()

pattern = r'XC:Z:(.*?)\s'
sam = open(raw_sam, 'r')
out = open('mouse_bc.sam', 'w')
for i in sam:
    if i.startswith('@'):
        out.write(i)
    else:
        mi = re.search(pattern, i)
        if mi:
            bc = mi.group(1)
            if bc in lbc:
                out.write(i)
sam.close()
out.close()

