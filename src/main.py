import argparse
import os
import xml.dom.minidom
from computeProcess import computeProcess
'''
    fastq pairs             k pairs
    sample label            k labels
    clipmode                True/False
    clipsetting             window, step
    ref                     string
    processes               number
'''

def nameprocess(s):
    #split samples using blank. split double end files using comma(,);
    ans=[]
    for f in s:
        if ',' in f:
            ff=f.strip().split(',')
        else:
            ff = [f]
    ans.append(ff)
    return ans


def getxmlcontent(dom,x):
    temp = dom.getElementsByTagName(x)
    if len(temp)==0:
        return None
    else:
        return temp[0].firstChild.data


def text_process(filename):
    dom = xml.dom.minidom.parse(filename)
    #root = dom.documentElement
    dic={}
    tagnames = ['fastq','label','clip','window','step','ref','process']
    tagcontent = list(map(lambda x:getxmlcontent(dom,x),tagnames))
    for i in range(len(tagnames)):
        name = tagnames[i]
        content = tagcontent[i]
        if name=='fastq':
            dic[name]=nameprocess(content.strip().split())
            continue
        if name=='label':
            dic[name]=content.strip().split()
            continue
        if name=='ref':
            dic[name]=content
            continue
        dic[name]=int(content)
        
    return dic

def inputorN(v):
    if v:
        return v
    else:
        return None

def valid(param):
    name = param['name']
    for n in name:
        for nn in n:
            if not os.path.exists(nn):
                raise Exception(nn+' not exist!')
    if len(param['label'])!=len(param['name']):
        raise Exception('Number of samples and number of labels should be the same!')
    if not os.path.exists(param['ref']):
        raise Exception(param['ref']+' not exist!')

def input_args():
    parser = argparse.ArgumentParser()
    parser.add_argument('-f','--file',type=int, help=r'Enter a number, 0 means using parameter to set up, 1 means using text file to set up',required=True,default=0)
    parser.add_argument('-sf','--settingfile',help='Setting txt file name. Ignore if -f is 0.',required=True)
    parser.add_argument('-n','--name',nargs="*",help=r'Fastq file name. ',required=True)
    parser.add_argument('-c','--clip',help=r'Clip mode. 0 means close. 1 means open. default: 0',type=int,default=0)
    parser.add_argument('-l','--label',nargs="*",help=r'Labels for samples',required=True)
    parser.add_argument('-w','--window',type=int,help=r'Window length for clipping mode.')
    parser.add_argument('-s','--step',type=int,help=r'Step size for clipping mode.')
    parser.add_argument('-p','--process',type=int,help=r'Process using for one pipeline. Normally bsmap will cost 8 cpu number. So total will be 8p.')
    parser.add_argument('-r','--ref',help=r'Reference',required=True)
    parser.add_argument('-qc','--QualityControl',help=r'Do(1) quality control or not(0)',default=False,required=True)
    parser.add_argument('-t','--trim',help=r"Do(1) trimming or not(0). Don't need to do trimming if you use clip mode.")

    args = parser.parse_args()
    '''
    if (not args.ref):
        raise Exception("No file designated as reference!")
    if (not args.name):
        raise Exception("No file designated as fastq files!")
    if (not )
    '''
    if args.file==1:
        param=text_process(args.settingfile)
    else:
        param={'name':(nameprocess(args.name) or None), 
               'clip':args.clip, 
               'label':(args.label or None), 
               'window':int(inputorN(args.window)), 
               'step':int(inputorN(args.step)), 
               'process':int(inputorN(args.step)), 
               'ref':(args.ref or None) 
               'qc':int(args.QualityControl)
               'trim':int(args.trim)
              }
    valid(param)
    return param

if __name__=="__main__":
    param=input_args()
    computeProcess(param)


