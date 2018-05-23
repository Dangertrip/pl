import numpy as np 
import matplotlib.pyplot as plt 
import pandas as pd
import seaborn as sns
from sklearn.manifold import TSNE
from sklearn.decomposition import PCA
import os
from urllib import request
'''
np.random.seed(2) 
df = pd.DataFrame(np.random.rand(5,4), columns=['A', 'B', 'C', 'D'])
df.boxplot() #也可用plot.box() 
plt.show()
'''

def boxplot(data,xname,yname):
    sns.set_style("whitegrid")
    group_num = len(x)
    fig,ax = plt.subplot(figsize=(10,10))
    sns.boxplot(x=xname,y=yname,data = data,ax=ax)
    fig.savefig('plot/'xname+'_'+yname+'.png')
    return True,''

def point_cluster(data,method='TSNE',windowlength=10000,genome='hg19'):
    url=request.urlopen('http://hgdownload.cse.ucsc.edu/goldenPath/'+genome+'/bigZips/'+genome+'.chrom.sizes')
    with open('plot/chromsize.txt') as f:
        f.write(url.read().decode())
    os.system('bedtools ')

    
