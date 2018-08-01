from utils import *

def readf(filename):
    with open(filename) as f:
        lines = f.readlines()
    return lines

def BsmapOutputExtractor(filename):
    #aligned=[]
    #unique=[]
    #total=[]
    info=[]#aligned,unique,total
    for name in filename:
        lines = readf(name)
        countinputfile=sum(list(map(lambda x: 'Input read file' in x,lines)))
        total=0
        unique=0
        aligned=0
        if countinputfile==2:
            for line in lines:
                if "total read pairs:" in line:
                    a = line.strip().split()
                    total=int(a[a.rfind('total read pairs:')+len('total read pairs:'):].split()[0])                    
                    continue
                if "aligned pairs:" in line:
                    a = line.strip().split()
                    aligned = aligned+int(a[2])*2
                    unique = unique + int(a[6])*2
                    continue
                if "unpaired read #1:" in line or "unpaired read #2:" in line:
                    a = ling.strip().split()
                    aligned = aligned+int(a[3])
                    unique = unique+int(a[7])
        else:
            for line in lines:
                if "total read pairs:" in line:
                    a = line.strip().split()
                    total=int(a[a.rfind('total read pairs:')+len('total read pairs:'):].split()[0])
                    continue
                if "aligned reads:" in line:
                    a = line.strip().split()
                    aligned = aligned+int(a[2])
                    unique = unique+int(a[6])
        info.append([total,aligned,unique])
    return info


def McallOutputExtractor(filename):
    lines = readf(filename)


def TrimOutputExtractor(filename):
    ratio=[]
    for name in filename:
        lines = readf(name)
        #Total written (filtered):  1,085,317,679 bp (94.2%)
        for line in lines:
            temp = line.strip().split()
            r=None
            if temp[0]=='Total' and temp[1]=='written' and temp[2]=='(filtered):':
                r=float(temp[5].strip()[1:-2])
                break
            ratio.append(r)
    return r



