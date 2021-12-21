import os
import re

##python2 raw_fastqc.py

os.system("mkdir fastqc_result")
os.system("ls *.fq > list_seq.txt")
file=open('list_seq.txt','r')
for i in file:
    fq=re.sub('\n','',i)
    os.system("fastqc -o ./fastqc_result -t 5 %s" %(fq))
file.close()
os.system("rm list_seq.txt")
