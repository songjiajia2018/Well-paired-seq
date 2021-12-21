import re

file = open('mouse_bc.txt','r')
lbc = []
for i in file:
    i = i.rstrip()
    lbc.append(i)
file.close()

pattern = r'XC:Z:(.*?)\s'
sam = open('mouse.sam','r')
out = open('mouse_bc.sam','w')
for i in sam:
    if i.startswith('@'):
        out.write(i)
    else:
        m = re.search(pattern,i)
        if m:
            bc = m.group(1)
            if bc in lbc:
                out.write(i)
sam.close()
out.close()

