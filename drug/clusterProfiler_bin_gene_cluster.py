import re

file_g = open('clusterProfiler_bin_gene.txt', 'r')
file_cg = open('markers_bin_cluster_gene.txt', 'r')
file_gc = open('clusterProfiler_bin_gene_cluster.txt', 'w')

cont_cg = file_cg.readlines()
cont_cg = cont_cg[1:]
dict_cg = {}
for i in cont_cg:
    i = re.sub('\n', '', i)
    i = i.split(' ')
    dict_cg[i[1]] = i[0]

cont_g = file_g.readlines()
col_name_g = cont_g[0]
col_name_gc = re.sub('\n', '', col_name_g)+' CLUSTER\n'
file_gc.write(col_name_gc)
cont_g = cont_g[1:]
for i in cont_g:
    i = re.sub('\n', '', i)
    m = i.split(' ')
    line = i+' '+dict_cg[m[0]]+'\n'
    file_gc.write(line)

file_g.close()
file_cg.close()
file_gc.close()
