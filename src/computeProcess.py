from moabs import *
from fastqc import Fastqc
from trim import Trim
import bsplot
from utils import *

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

def computeTrim(name,trim,param={})
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
    '''
        
         
        

        
