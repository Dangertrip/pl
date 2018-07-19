from moabs import Bsmap
from fastqc import Fastqc
from trim import Trim
import bsplot

def computeProcess(param):
    ProcessObject=[Fastqc(),Trim(),Bsmap()]
    for obj in ProcessObject:
        status,word=obj.check()
        if not status:
            raise Exception(word)
    #check all software have been installed successfully.
    
    if param['qc']:
        
