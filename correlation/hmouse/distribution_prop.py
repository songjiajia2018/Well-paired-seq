# -*- coding: utf-8 -*-
"""
Created on Wed Jul  7 11:02:37 2021

@author: 牧木
"""

# python distribution_prop.py
# 各比对率统计

import re


def rround(c, f):
    c = str(c)
    c = c.split('.')
    m = c[0]
    n = c[1]
    if n[2] in ['0', '1', '2', '3', '4']:
        c2 = m+'.'+n[0:2]
    elif n[2] in ['6', '7', '8', '9']:
        c2 = m+'.'+n[0]+str(int(n[1])+1)
    else:
        p = int(n[1])
        if p % 2 == 0:
            c2 = m+'.'+n[0:2]
        else:
            c2 = m+'.'+n[0]+str(int(n[1])+1)
    return(c2)


file = open('starLog.final.out', 'r')
cont = file.readlines()
file.close()
o = '==============================  starLog.final.out  ===============================\n'+''.join(cont)

for i in cont:
    if 'Number of input reads' in i:
        total_reads = i.rstrip().split('\t')[1]

file = open('reads_distribution.txt', 'r')
cont = file.readlines()
file.close()
o = o+'\n\n'+'====================  reads_distribution  ====================\n'+''.join(cont[3:])

mapped_reads = cont[3].rstrip().split('Reads')[1].lstrip()
total_tags = cont[4].rstrip().split('Tags')[1].lstrip()
assigned_tags = cont[5].rstrip().split('Tags')[1].lstrip()
unassigned_tags = str(int(total_tags)-int(assigned_tags))

pattern = r' ([0-9]+?) '
for i in cont[8:-1]:
    m = re.findall(pattern, i)
    if i.startswith("CDS_Exons"):
        cds_exons = m[1]
    if i.startswith("5'UTR_Exons"):
        UTR5_exons = m[1]
    if i.startswith("3'UTR_Exons"):
        UTR3_exons = m[1]
    if i.startswith("Introns"):
        introns = m[1]
intergenic_tags = str(int(total_tags)-int(cds_exons)-int(UTR5_exons)-int(UTR3_exons)-int(introns))

mapping_rate = (float(mapped_reads)/float(total_reads))*100
coding = (float(cds_exons)/float(total_tags))*mapping_rate
intronic = (float(introns)/float(total_tags))*mapping_rate
UTR = ((float(UTR5_exons)+float(UTR3_exons))/float(total_tags))*mapping_rate
intergenic = (float(intergenic_tags)/float(total_tags))*mapping_rate

head = 'mapping_rate\tcoding\tintronic\tUTR\tintergenic\n'
prop = rround(mapping_rate, 2)+'%\t'+rround(coding, 2)+'%\t'+rround(intronic, 2)+'%\t'+rround(UTR, 2)+'%\t'+rround(intergenic, 2)+'%\n'
anno = 'mapping_rate = Total Reads(reads_distribution)/Number of input reads(starLog.final.out)\n'
anno = anno+'coding = (CDS_Exons(reads_distribution)/Total Tags(reads_distribution)) * mapping_rate\n'
anno = anno+'intronic = (Introns(reads_distribution)/Total Tags(reads_distribution)) * mapping_rate\n'
anno = anno+"UTR = (5'UTR_Exons+3'UTR_Exons(reads_distribution))/Total Tags(reads_distribution) * mapping_rate\n"
anno = anno+"Intergenic_tags = Total Tags-CDS_Exons-5'UTR_Exons-3'UTR_Exons-Introns(reads_distribution)\n"
anno = anno+'intergenic = Intergenic_tags/Total Tags(reads_distribution) * mapping_rate\n'

o = head+prop+'\n'+anno+'\n\n'+o
out = open('distribution_prop.txt', 'w')
out.write(o)
out.close()

