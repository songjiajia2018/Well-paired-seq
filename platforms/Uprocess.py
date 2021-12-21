# -*- coding: utf-8 -*-
"""
Created on Tue Jul  6 18:26:11 2021

@author: 牧木
"""

import os

url_18_23_1 = './18_23-1'
url_18_3K_1 = './18_3K-1'
url_seqwell = './SeqWell'
url_ftd = './scFTDseq'
url_dropseq11 = './Dropseq11'
url_dropseq12 = './Dropseq12'
url_dropseq77 = './Dropseq77'
url_10x_v2 = './10x_v2'
url_10x_v3_1 = './v3_10x_1'
url_10x_v3_2 = './v3_10x_2'
url = [url_18_23_1, url_18_3K_1, url_seqwell, url_ftd, url_dropseq11, url_dropseq12, url_dropseq77, url_10x_v2, url_10x_v3_1, url_10x_v3_2]

max_d = '300000'
l_by = '10000'
v_by = '30000'
v_low = '35000'
v_high = '200000'
summary_file = 'merge_gene_exon_tagged_h+m.dge.summary.txt'

for i in url:
    print(i)
    summary = i+'/'+summary_file
    os.system('''Rscript U1_hm_info.R %s %s %s %s %s %s''' % (max_d, l_by, v_by, v_low, v_high, summary))
    os.system('''ls V1*''')
    os.system('''mv V1* %s''' % (i))

os.system('''Rscript U2_lineplot.R''')
low = str(int(int(v_low)/1000))
high = str(int(int(v_high)/1000))
os.system('''Rscript U3_violinplot.R %s %s''' % (low, high))

