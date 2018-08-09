import matplotlib
matplotlib.use('Agg')
import numpy as np 
import matplotlib.pyplot as plt 
from sklearn.manifold import TSNE
from sklearn.decomposition import PCA
import os
from urllib import request
from copy import deepcopy
import matplotlib.cm as cm
'''
np.random.seed(2) 
df = pd.DataFrame(np.random.rand(5,4), columns=['A', 'B', 'C', 'D'])
df.boxplot() #也可用plot.box() 
plt.show()


def boxplot(data,xname,yname):
    sns.set_style("whitegrid")
    group_num = len(x)
    fig,ax = plt.subplot(figsize=(10,10))
    sns.boxplot(x=xname,y=yname,data = data,ax=ax)
    fig.savefig('PLOTS/'+xname+'_'+yname+'.png')
    return True,''

def window(windowlength=10000,genome='hg19'):
    if not os.path.exist('PLOTS/chromsize.txt'):
        url=request.urlopen('http://hgdownload.cse.ucsc.edu/goldenPath/'+genome+'/bigZips/'+genome+'.chrom.sizes')
    with open('PLOTS/chromsize.txt','w') as f:
        f.write(url.read().decode())
    windowfile = 'PLOTS/chrom.window.'+str(windowlength)+'.bed'
    os.system('bedtools makewindows -g plot/chromsize.txt -n '+str(windowlength)+' > '+windowfile)
    return True,windowfile
'''
def point_cluster(data,method='TSNE',outputname):
    #data: DataFrame
    #contains labelname column, samplename column and data
    d = deepcopy(data)
    #print(di)
    d.sort(['chrom','start'])

    windowdata = d.values[3:,]
    position = d.values[:3,]
    label = d.columns[3:]
    #Every sample in a row
    #print(windowdata)
    dim=2
    colors = cm.rainbow(np.linspace(0,1,num_group))

    if method == 'PCA':
        pca = PCA(n_components=dim)
        x_tr = pca.fit_transform(windowdata)
    if method == 'TSNE':
        tsne = TSNE(n_components=dim)
        x_tr = tsne.fit_transform(windowdata)
    fig,ax = plt.subplots(figsize=(7,7))
    xmin = np.min(x_tr[:,0])
    xmax = np.max(x_tr[:,0])
    ymin = np.min(x_tr[:,1])
    ymax = np.max(x_tr[:,1])
    sample_size = x_tr.shape[0]
    plt.xlim(xmin-0.2*np.abs(xmin),xmax+0.2*np.abs(xmax))
    plt.ylim(ymin-0.2*np.abs(ymin),ymax+0.2*np.abs(ymax))
    markers=['o', '^','v','<','>','1','2', '3','4','8','s','P','p', '*','H','h','x','X','D']
    for i in range(len(label)):
        cc = colors[i]
        l = label[i]
        pos = np.where(labels==label)
        ma = markers[i]
        plt.scatter(x_tr[pos,0],x_tr[pos,1],c=cc,alpha=0.8,s=50,marker=ma,label=l)

    if method=='PCA':
        plt.xlabel('PC1',fontsize=13)
        plt.ylabel('PC2',fontsize=13)
    if method=='TSNE':
        plt.xlabel('TSNE1',fontsize=13)
        plt.ylabel('TSNE2',fontsize=13)
    plt.legend(loc='best',fontsize=13)
    plt.savefig(outputname)

def heatmap(data,outputname):
    from seaborn import clustermap 
    d = deepcopy(data)
    d=d.drop(['chrom','start','end'])
    sns_plot=clustermap(data)
    sns_plot.ax_row_dendrogram.set_visible(False)
    sns_plot.savefig(outputname)


if __name__=='__main__':
    d = pd.DataFrame(data=np.arange(64).reshape(8,8))
    d['label']=['a','a','a','b','b','b','c','c']
    d['sample']=['a1','a2','a3','b1','b2','b3','c1','c2']
    print(point_cluster(data=d,labelname='label',samplename='sample'))


    


    



    
