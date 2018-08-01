from utils import *

def readf(filename):
    with open(filename) as f:
        lines = f.readlines()
    return lines

def BsmapOutputExtractor(filename):
    #aligned=[]
    #unique=[]
    #total=[]
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
    return [total,aligned,unique]


def McallOutputExtractor(filename):
    lines = readf(filename)


def TrimOutputExtractor(filename):
    ratio=[]
    for nn in filename:
        temp=[]
        for name in nn: 
            lines = readf(name)
            #Total written (filtered):  1,085,317,679 bp (94.2%)
            for line in lines:
                temp = line.strip().split()
                r=None
                if temp[0]=='Total' and temp[1]=='written' and temp[2]=='(filtered):':
                    r=float(temp[5].strip()[1:-2])
                    break
                temp.append(r)
            ratio.append(temp)
    return r

'''
Result from BsmapOutputExtractor:
    total reads, mapped reads, uniquely mapped reads
Result from BsmapResult:
    [[total reads,mapped reads,uniquely mapped reads, clipped reads, unique clipped reads,
    all mapped reads, all uniquely mapped reads, mapping ratio, uniquely mapping ratio],...]
'''
def BsmapResult(filenames,clip):
    if clip:
        '''
        We will get two record files in this mode
        '''
        result=[]
        for name in filenames:
            ori,spl = name
            ori_info,spl_info = BsmapOutputExtractor(ori),BsmapOutputExtractor(spl)
            total_reads,mapped_reads,uniquely_mapped_reads=ori_info
            _,clipped_reads,uniquely_clipped_reads=spl_info
            result.append([total_reads,mapped_reads,uniquely_mapped_reads,clipped_reads,
                uniquely_clipped_reads,
                mapped_reads+clipped_reads,uniquely_mapped_reads+uniquely_clipped_reads,
                (mapped_reads+clipped_reads)/float(total_reads),
                (uniquely_mapped_reads+uniquely_clipped_reads)/float(total_reads)])
    else:
        '''
        Only one record file need to be processed.
        '''
        result=[]
        for name in filenames:
            ori = name
            ori_info = BsmapOutputExtractor(ori)
            total_reads,mapped_reads,uniquely_mapped_reads=ori_info
            _,clipped_reads,uniquely_clipped_reads=[0,0,0]
            result.append([total_reads,mapped_reads,uniquely_mapped_reads,clipped_reads,
                uniquely_clipped_reads,
                mapped_reads+clipped_reads,uniquely_mapped_reads+uniquely_clipped_reads,
                (mapped_reads+clipped_reads)/float(total_reads),
                (uniquely_mapped_reads+uniquely_clipped_reads)/float(total_reads)])
    return result
