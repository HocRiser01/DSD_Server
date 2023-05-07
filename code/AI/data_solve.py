import json
import os
import pickle

def get_label(name):
    if name.startswith('down'): return 0
    if name.startswith('left'): return 1
    if name.startswith('right'): return 2
    if name.startswith('sit'): return 3
    if name.startswith('stand'): return 4
    if name.startswith(''): return 5
    if name.startswith(''): return 6
    return -1

path = "./2023-04-24 DATA"
files = os.listdir(path)
for file in files:
    with open(path+'/'+file) as f:
        P=json.load(f)
        label = get_label(file)
        if (label==-1): continue
        for g in P:
            ls=[]
            for t in g:
                if (t.startswith('time')):
                    ls.append(float(g[t]))
                else:
                    dd=g[t]
                    for d in dd:
                        ls.append(float(dd[d]))
            if (len(ls)!=55): exit(0)



               # print(type(t))
