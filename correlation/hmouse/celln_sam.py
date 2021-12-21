# -*- coding: utf-8 -*-
"""
Created on Tue Jul 20 16:12:38 2021

@author: 牧木
"""

import numpy as np
import re
import os

num = 10

bc = []
file = open('mouse_bc.txt', 'r')
for i in file:
    i = i.rstrip()
    bc.append(i)
file.close()
BC = np.random.choice(bc, num, replace=False)

bname = 'cell_'+str(num)+'.txt'
file = open(bname, 'w')
for i in BC:
    file.write(i+'\n')
file.close()

pattern = r'XC:Z:(.*?)\s'
sam = open('mouse_bc.sam', 'r')
oname = 'mouse_bc_'+str(num)+'.sam'
out = open(oname, 'w')
for i in sam:
    if i.startswith('@'):
        out.write(i)
    else:
        m = re.search(pattern, i)
        if m:
            bcn = m.group(1)
            if bcn in BC:
                out.write(i)

os.system('''read_distribution.py -i %s -r /home/songjia/newdisk/YK/reference/hg19_mm10/hg19_mm10_transgenes_species_gene_name.bed''' % (oname))

nohup = open('nohup.out', 'r')
cont = nohup.readlines()
nohup.close()

outnohup = open('reads_distribution_'+str(num)+'.txt', 'w')
o = cont[-19:]
o = ''.join(o)
outnohup.write(o)
outnohup.close()

