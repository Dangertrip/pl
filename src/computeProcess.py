from moabs import Bsmap
from fastqc import Fastqc
from trim import Trim
import bsplot

def computeProcess(param):
    fastqc,trim,bsmap = Fastqc(), Trim(), Bsmap()
    ProcessObject=[fastqc,trim,bsmap]
    for obj in ProcessObject:
        status,word=obj.check()
        if not status:
            raise Exception(word)
    #check all software have been installed successfully.
    for obj in ProcessObject:
        obj.setpath('./')
    
    name = param['name']
    resultfilename={}
    if param['qc']:
        fn=[]
        for nn in name:
            temp=[]
            for n in nn:
                temp.append(fastqc.run(n))
            fn.append(temp)
        resultfilename['qc']=fn
    if param['trim']:
        fn=[]
        
         
        

        
