import sys
import multiprocessing
import subprocess

class Pshell():

    def __init__(self,commend):
        self.commend = commend
        self.out = ""

    def change(self,commend):
        self.commend = commend

    def getcommend(self,commend):
        return commend

    def process(self):
        print(self.commend)
        t = subprocess.Popen(self.commend,shell=True,stdout = subprocess.PIPE,stderr = subprocess.PIPE)
        self.out = t.stdout.read().decode()
        self.err = t.stderr.read().decode()
        print(self.err)

    def get_result(self):
        return self.out

class reads():

    def __init__(self,chromosome,startpos,order,mismatch):
       # self.fqname = fqname
        self.chromosome = chromosome
        self.startpos = startpos
        self.sum = 0
        self.order = order
        self.chain = 0
        self.mismatch = mismatch

    def equal(self,rreads):
        if (rreads.getChrom()==self.chromosome)and(rreads.getStartPos()==self.startpos): return True
        return False

    def getChrom(self):
        return self.chromosome

    def getOrder(self):
        return self.order

    def getSum(self):
        return self.sum

    def getStartPos(self):
        return self.startpos

    def join(self,tail,mis):
        self.mismatch = self.mismatch + mis
        self.sum = tail.getOrder()-self.getOrder()

    def getChain(self):
        return self.chain

    def getMismatch(self):
        return self.mismatch

    def canjoin(self,tail,step,xx,binsize):
        if (tail.getChrom()==self.chromosome):
            if (tail.getStartPos() == self.startpos + step*(self.order-tail.getOrder()) or tail.getStartPos() == self.startpos - step*(self.order-tail.getOrder())):
            #if tail.getStartPos()>self.startpos: self.chain = 0
            #else: self.chain = 1
                return True
            if xx!=binsize:
                if xx % step == abs(self.startpos-tail.getStartPos())%step:
                    return True
        return False


def overlap(a,b,step,length_bin):
#Detect 2 kinds of overlapping
# 1. fragments combination overlap: fragment 1 and fragment 2,3,4.. can not appear in two different combinations
# 2. combinations can not overlap in reference genome.
    ordera = a.getOrder()
    orderb = b.getOrder()
    if (orderb<ordera):
        k=a
        a=b
        b=k
    ordera = a.getOrder()
    orderb = b.getOrder()
    sa = a.getStartPos()
    sb = b.getStartPos()
    suma = a.getSum()
    sumb = b.getSum()
    if (a.getChrom()==b.getChrom()) and ((sa<sb and sa+suma*step+length_bin>sb) or (sb<sa and sb+sumb*step+length_bin>sa)): 
        return True
    if orderb-ordera-suma<=(length_bin/step)-1: return True
    return False

def RemoveFastqExtension(name):
    '''
    This function is used for remove extensions like .gz .fq .fastq.gz
    '''
    newname = name
    if newname[-3:].lower()=='.gz':
        newnamename=newname[:-3]
    if newname[-3:].lower()=='.fq':
        newname=newname[:-3]
    if newname[-6:].lower()=='.fastq':
        newname=newname[:-6]
    return newname

def toolcheck(command):
    t = subprocess.Popen(command,shell=True,stdout = subprocess.PIPE,stderr = subprocess.PIPE)
    out = t.stdout.read().decode()
    err = t.stdout.read().decode()
    if ' command not found' in out or ' command not found' in err:
        return False
    return True

def readf(filename):
    with open(filename) as f:
        lines = f.readlines()
    return lines

def union(files):
    dic={}
    for f in files:
        lines = readf(f)
        for line in lines:
            temp = line.strip().split()
            key=temp[0]+'\t'+temp[1]+'\t'+temp[2]
            if key in dic:
                dic[key].append(int(temp[3]))
            else:
                dic[key]=[int(temp[3])]
    for key in dic:
        if len(dic[key])!=len(files):
            del(dic[key])
    return dic
            

if __name__=="__main__":
    dic=union(['BED_FILE/head_combine.bam.G.bed.short.bed','BED_FILE/head_combine.bam.G.bed.short.bed'])
    print(dic)
