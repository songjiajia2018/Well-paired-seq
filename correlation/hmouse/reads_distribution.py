import os

os.system('''read_distribution.py -i my_clean.bam -r /home/songjia/newdisk/YK/reference/hg19_mm10/hg19_mm10_transgenes_species_gene_name.bed''')

file = open('nohup.out', 'r')
cont = file.readlines()
file.close()

out = open('reads_distribution.txt', 'w')
o = cont[-19:]
o = ''.join(o)
out.write(o)
out.close()

