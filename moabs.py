'''
This is a wapper for MOABS in this pipeline. It contains commands for BSMAP, bam sort, bam deduplicate, methylation calling.
'''

from utils import *
from clipmode import clipmode
import os

class Bsmap()

    def check(self):
        if not toolcheck('bsmap -h'):
            return False,'BSMAP not found!'
        if os.path.exists('BAM_FILE'):
            return False,'"BAM_FILE" exists! Please delete "BAM_FILE"'
        os.mkdir("BAM_FILE")
        return True,''

    def bsmap(self,filenames,param={}):
        refpath = param['ref']
        names = []
        for file in filenames:
            mark,name=normalmode(file,param)
            if mark:
                names.append(name)
        print('Finished normal mode BSMAP')
        return True,names

    def normalmode(file,param)
        f = file.strip().split()
        if len(f)==1:
            name = f[0]+'.bam'
            cmd = 'bsmap -a '+f[0]+' -d '+refpath+' -o '+name+' -n 0 1>>BAM_FILE/bsmap_log 2>'+name[:-4]+'.record'
        else:
            name = f[0]+'.bam'
            cmd = 'bsmap -a '+f[0]+' -b '+f[1]+' -d '+refpath+' -o '+name+'-n 0 1>>BAM_FILE/bsmap_log 2>'+name[:-4]+'.record'
        p = Pshell(cmd)
        p.process()
        return True,name

    def clipping(self,filenames,param={}):
        mark,names = clipmode(filenames,param)
        if mark:
            return mark,names
        else:
            return False,[]
