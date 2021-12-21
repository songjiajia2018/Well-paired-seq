# -*- coding: utf-8 -*-
"""
Created on Tue Jul 20 16:12:38 2021

@author: 牧木
"""

import pandas as pd
import numpy as np
import re
import os
import os.path

num = 1
flag = 1

if (flag == 1):
    bc = []
    file = open('mouse_bc.txt', 'r')
    for i in file:
        i = i.rstrip()
        bc.append(i)
    file.close()
    BC = np.random.choice(bc, num, replace=False)
elif (flag == 2):
    info = 'celln_info_'+str(num)+'.txt'
    if (os.path.isfile(info)):
        bc = pd.read_csv(info, sep='\t', encoding='utf-8')
        BC = list(bc['CELL_BARCODE'])[:-1]
    else:
        print('File '+info+' does not exit!!!')
        print('Please run python celln_info.py!!!')
else:
    print('"flag" error!!!')
#BC = ['GAGCGCTAGGCC']

bname = 'mouse_bc_'+str(num)+'.txt'
file = open(bname, 'w')
for i in BC:
    file.write(i+'\n')
file.close()

pattern = r'XC:Z:(.*?)\s'
#sam = open('mouse_bc.sam', 'r')
sam = open('my_clean.sam', 'r')
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
out.close()

os.system('''read_distribution.py -i %s -r /home/songjia/newdisk/YK/reference/mm10/mm10.bed''' % (oname))

nohup = open('nohup.out', 'r')
cont = nohup.readlines()
nohup.close()

outnohup = open('reads_distribution_'+str(num)+'.txt', 'w')
o = cont[-19:]
o = ''.join(o)
outnohup.write(o)
outnohup.close()


