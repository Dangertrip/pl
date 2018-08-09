'''
Tested
'''
from utils import *
import os

class Fastqc():


    def check(self):
        if not toolcheck('fastqc --help'):
            return False,'Fastqc command not found'
        if os.path.exists('Fastqc'):
            return False,'Fastqc file or dir exists'
        os.mkdir('Fastqc')
        return True,''

    def setpath(self,path):
        self.path = path+'Fastqc'

    def run(self,filename):
        pshell=Pshell('fastqc -o '+self.path+' '+filename)
        pshell.process()

    

if __name__=="__main__":
    a = Fastqc()
    #print(a.check())
    a.setpath('./')
    a.run('../trimtest/SRR1248444_1.1.1.1.fastq')
