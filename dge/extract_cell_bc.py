#!/usr/bin/env python
#coding=utf-8

import sys
import re

##python extract_cell_bc.py out_cell_readcounts.txt(DGE1.py) num
##extract cell_bc_file.txt from out_cell_readcounts.txt

file=open(sys.argv[1],'r')
n=sys.argv[2]
file_bc=open('cell_bc_file_'+n+'.txt','w')
pattern='\s([A-Z]*?)\n'
count=0
num=int(n)
for i in file:
    if (re.search(pattern,i)):
        cell_bc=re.search(pattern,i)
        bc=cell_bc.group(1)
        print(bc)
        file_bc.write(bc+'\n')
        count=count+1
        if (count >= num):
            break
file_bc.close()
file.close()
