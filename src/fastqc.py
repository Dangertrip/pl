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
        self.path = path+'/Fastqc'

    def run(self,filename):
        pshell=Pshell('fastqc -o '+path+' '+filename)
        pshell.process()
        return filename[:filename.find('.')]


if __name__=="__main__":
    a = Fastqc()
    print(a.check())
