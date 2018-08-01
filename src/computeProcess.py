from moabs import *
from fastqc import Fastqc
from trim import Trim
import bsplot
from utils import *
from NumExtractor import *
from bedtools import Bedtools

def computeQC(name,fastqc,param={}):
    '''
    Computing function for qc. Return two arrays: The first one contains filenames for next step computing.
    The second one contains 
    '''
    fn=[]
    filename=''
    for nn in name:
        temp=[]
        for n in nn:
            filename = filename+n+' '
            newname = RemoveFastqExtension(n)
            temp.append(newname+'_fastqc.html')
        fn.append(temp)
    fastqc.run(filename)
    return name,fn

def computeTrim(name,trim,param={}):
    fn=''
    trimmedname=[]
    triminfo=[]
    for n in name:
        temp=[]
        infotemp=[]
        for nn in n:
            newname = RemoveFastqExtension(nn)
            fn = fn+nn+' '
            temp.append(newname+'_trimmed.fq.gz')
            infotemp.append(nn+'_trimming_report.txt')
        trimmedname.append(temp)
        triminfo.append(infotemp)
    fn.strip()
    trim.run(fn)
    name=trimmedname
    return name,triminfo

def computeBsmap(name,bsmap,param):
    clip = param['clip']
    bamname=[]
    bamlogname=[]
    for n in name:
        if clip:
            newname,logname = bsmap.clipping(n)
        else:
            newname,logname = bsmap.normalmode(n)
        bamname.append(newname)
        bamlogname.append(logname)
    return bamname,bamlogname

def computeMcall(name,mcall,param):
    bedname=[]
    logname=[]
    for n in name:
        bn,ln=mcall.run(name)
        bedname.append(bn)
        logname.append(ln)
    return bedname,logname

def computeProcess(param):
    fastqc,trim,bsmap,mcall = Fastqc(), Trim(), Bsmap(), Mcall()
    ProcessObject=[fastqc,trim,bsmap,mcall]
    for obj in ProcessObject:
        status,word=obj.check()
        if not status:
            raise Exception(word)
    #check all software have been installed successfully.
    for obj in ProcessObject:
        obj.setpath('./')
    
    bsmap.setparam(param)
    mcall.setparam(param)

    name = param['name']
    resultfilename={}
    if param['qc']:
        name,qcresult=computeQC(name,fastqc,{}) 
        resultfilename['qc']=qcresult
    
    if param['trim']:
        name,trimresult = computeTrim(name,trim,{})
        resultfilename['trim']=trimresult

    name,bsmapresult = computeBsmap(name,bsmap,param) 
    resultfilename['bsmap'] = bsmapresult

    name,mcallresult = computeMcall(name,mcall,param)
    resultfilename['mcall'] = mcallresult
        
    '''
    All computing job is done here. Plotting is behind.
    Table:
    Filename, Label, trim ratio(TrimOutputExtractor),input reads,mapped reads, unique mapped reads,
    clipped reads, unique clipped reads, all mapped reads, unique all, mapping ratio, unique mapping ratio
    
    Plots:
    1. Extract trim ratio from trim report files. Generate a bar plot
    2. Extract bsmap mapping ratio 
    3. 
    
    '''
    originalfilename = param['name']
    filelabel = param['label']
    marker=['Filename','Label']
    if param['qc']:
        marker.append('QC')
    if param['trim']:
        marker.append('Trim')
        trimresult =TrimOutputExtractor(resultfilename['trim']) 
    '''
    Result from BsmapResult:
    [[total reads,mapped reads,uniquely mapped reads, clipped reads, unique clipped reads,
    all mapped reads, all uniquely mapped reads, mapping ratio, uniquely mapping ratio],...]
    '''
    marker.extend(['Input reads','mapped reads','uniquely mapped reads','clipped reads','uniquely clipped reads','all mapped reads','all uniquely mapped reads','mapping ratio','uniquely mapping ratio'])
    bsmapresult = BsmapResult(resultfilename['bsmap'])#All contents required by the last extend

    sample=0
    datatable=[marker]
    for orin in originalfilename:
        l = label[sample]
        br = bsmapresult[sample]
        temp=[]
        filenum=0
        for nn in orin:
            temp.extend([nn,l])
            if param['qc']:
                temp.append(resultfilename['qc'][sample][filenum])
            if param['trim']:
                temp.append(resultfilename['trim'][sample][filenum])
            filenum=filenum+1
            temp.extend(br)
        sample = sample+1
        datatable.append(temp)
        

    datatableprint = list(map(lambda x: ''.join(list(map(lambda y:str(y)+'\t',x ))).strip(),datatable))
    with open('RESULT/datatable.txt','w') as f:
        f.writelines(datataleprint)
    '''
    Table generated as RESULT/datatable.txt
    '''




        
         
        

        
