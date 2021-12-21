# !usr/bin/env python
# -*- coding:utf-8 -*-

# python counts2count.py

import os
import re

os.system("ls *_counts.txt > list_counts")
file = open('list_counts', 'r')
for i in file:
    i = i.rstrip()
    prefix = re.sub('_counts.txt', '', i)
    j = prefix+'_count.txt'
    file_counts = open(i, 'r')
    file_count = open(j, 'w')
    cont_counts = file_counts.readlines()
    cont_count = cont_counts[:-5]
    file_count.write(''.join(cont_count))
    file_counts.close()
    file_count.close()
    print(j+" finished!!!")
os.system("rm list_counts")
print("Counts2Count Finished!!!")

