'''
This is a wapper for MOABS in this pipeline. It contains commands for BSMAP, bam sort, bam deduplicate, methylation calling.
'''

from utils import *
from clipmode import clipmode
import os

class Mcall():

    def check(self):
        if not toolcheck('mcall'):
            return False,'Mcall not found!'
        if os.path.exists('BED_FILE'):
            return False,'"BED_FILE" exists! Please delete "BED_FILE"'
        os.mkdir("BED_FILE")
        return True,''

    def setpath(self,path):
        this.path = path+'BED_FILE/'

    def setparam(self,param):
        mcallparam=None
        if 'mcall' in param:
            mcallparam=param['mcall']
        this.refpath = param['ref']
        this.extraparam=''

    def run(self,name):
        '''
        NEED FIX THE PATH
        '''
        cmd='mcall -m '+n+' -r '+this.refpath+' -p 8 1>>'+this.path+'log 2>>'+this.path+'err'
        p = Pshell(cmd)
        p.process()
        generatedfile=['.G.bed','.HG.bed','_stat.txt']
        newname=[]
        for g in generatedfile:
            os.rename(n+g,this.path+n[n.rfind('/'):]+g)
            newname.append(this.path+n[n.rfind('/'):]+g)
        
        return newname[0],newname[2]

        



class Bsmap():

    def check(self):
        if not toolcheck('bsmap -h'):
            return False,'BSMAP not found!'
        if os.path.exists('BAM_FILE'):
            return False,'"BAM_FILE" exists! Please delete "BAM_FILE"'
        os.mkdir("BAM_FILE")
        return True,''
   
    def setpath(self,path):
        this.path = path+'BAM_FILE/'

    def setparam(self,param):
        this.extraparam=''
        bsmapparam=None
        if 'bsmap' in param:
            bsmapparam = param['bsmap']
        '''
        Once I'm ready to add all parameters for bsmap and mcall (After finish the dictionary 
        to parameter function, I will delete variable named ***param )
        '''
        this.refpath = param['ref']

    def normalmode(self,file,param={})
        f = file.strip().split()
        name = this.path+f[0]+'.bam'
        logname = this.path+RemoveFastqExtension(f[0])+'.record'
        if len(f)==1:
            cmd = 'bsmap -a '+f[0]+' -d '+this.refpath+' -o '+name+' -n 0 1>>BAM_FILE/bsmap_log 2>'+logname
        else:
            cmd = 'bsmap -a '+f[0]+' -b '+f[1]+' -d '+this.refpath+' -o '+name+'-n 0 1>>BAM_FILE/bsmap_log 2>'+logname
        p = Pshell(cmd)
        p.process()
        return name,logname

    def clipping(self,filenames,param={}):
        '''
        I should return a bam file name and a log file name here
        '''
        mark,names = clipmode(filenames,param)
        if mark:
            return mark,names
        else:
            return False,[]
