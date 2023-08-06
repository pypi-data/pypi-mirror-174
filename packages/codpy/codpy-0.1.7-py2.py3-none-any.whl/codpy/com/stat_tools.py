import os,sys
import time as time
import codpypyd as cd
from    codpy_tools import *
from    scikit_tools import *
import matplotlib.pyplot as plt
import pylab 
import scipy.stats as stats
import numpy as np
from typing import List, Tuple
import pandera as pa
from pandera.typing import Index, DataFrame, Series

#### global variables
N = 100
D = 1
###

def output(fx,fz, msg = "", plotit = True):
    print("###############",msg,"######################")
    if plotit == True:
        compare_plot(fx,fz)
    print("summary:")
    print(summary((fx,fz)))
    print("#####################################")
    print("KS test:")
    print(ks_testD(fx,fz))
    print("#####################################")
    print("compare_distances:")
    print(compare_distances(fx,fz))
    print("#####################################")


def ecdf(data, idx = 0, reshape=False, fun_permutation = lexicographical_permutation):
    import numpy as np
    if (data.ndim == 2):
        x = data[:,idx]
        x.sort()
    elif (data.ndim == 1):
        x = np.sort(data)
    else:
        raise 'HiThere'
    n = len(x)
    y = np.arange(start = .5/n,stop = 1.,step = 1./n).reshape(n)
    if (reshape): 
        x = x.reshape((len(x),1))
        y = y.reshape((len(y),1))
    return(x,y)

def quantile(fz, idx = 0, reshape=False, fun_permutation = lexicographical_permutation):
    (x,y, permutation) = ecdf(data = fz, idx = idx, reshape=reshape, fun_permutation = lexicographical_permutation)
    return(y,x)

def epsilon(n, alpha=0.05):
   return np.sqrt(1. / (2. * n) * np.log(2. / alpha))


def gendata(type, location = 0, scale = 1, size = (N,D), df=3):
    import scipy
    arg = dist[type]
    switcher = {
        1: np.random.normal(location, scale, size),
        2: np.random.standard_t(df,size)
    }
    return switcher.get(arg, 'nothing')


def plot_ecdf(x,y):
    plt.scatter(x,y)

def QQplot(x,y,fx,fy,idx=0, title = "compare functions"):
    import matplotlib.pyplot as plt
    if x.ndim > 1:
        x = x[x[:,idx].argsort()].reshape(len(x))
    if y.ndim > 1:
        y = y[y[:,idx].argsort()].reshape(len(y))
    if fx.ndim > 1:
        fx = fx[fx[:,idx].argsort()].reshape(len(fx))
    if y.ndim > 1:
        fy = fy[fy[:,idx].argsort()].reshape(len(fy))
    plt.plot(x, fx, marker = 'o',color='red',label='orginal',linewidth=1, markersize=2)
    plt.plot(y, fy, marker = 'o',color='blue',label='extrapolated',linewidth=1, markersize=2)
    pylab.show()


def hist_plot(param: List,ax, **kwargs) -> None:
    """
    author: SMI
    outputs the histogram of list: param.
    """
    from matplotlib import pyplot as plt, cm
    from scipy import stats
    labels = kwargs.get('labels',['labelx', 'labely'])
    label_size = kwargs.get('label_size', 5)
    bins = kwargs.get('bins', 100)
    num_colors = np.shape(param)[0]
    colors = cm.rainbow(np.linspace(0, 1, num_colors))
    
    for i, label, color in zip(param, labels, colors):
        x = get_matrix(i)
        kde_x = stats.gaussian_kde(x.flatten())
        xx = np.linspace(np.min(x), np.max(x), 10000)
        plt.hist(x,bins=bins, density=True, color=color, label=label)
        plt.plot(xx,kde_x(xx))
        plt.legend(loc='upper right', prop={'size': label_size})

def scatter_plot(param: List,ax,**kwargs) -> None:
    x,y = get_matrix(param[0]),get_matrix(param[1])
    N = min(len(x),len(y))
    plt.plot(x[:,0], x[:,1],'o',color = 'blue', label = "True", markersize = 2)
    plt.plot(y[:,0], y[:,1],'o',color = 'red', label = "Sampling", markersize=2, alpha = 0.5)
    plt.legend()

def chi2t_plot():
    from scipy import stats
    import numpy as np
    import matplotlib.pyplot as plt

    x = np.linspace(0, 10, 100)
    fig,ax = plt.subplots(1,1)

    linestyles = [':', '--', '-.', '-']
    df = [1, 2, 3, 4]
    for dfi, ls in zip(df, linestyles):
        ax.plot(x, stats.chi2.pdf(x, dfi), linestyle=ls)

    plt.xlim(0, 10)
    plt.ylim(0, 1)

    plt.xlabel("Pearson's cumulative test statistic" )
    plt.ylabel('p-value')
    plt.title('Chi-Square Distribution')
    plt.show()

def chi2test(fx,fz):
    #goodness_of_fit_test
    import scipy
    import pandas as pd
    k = fx.shape[0]
    chisq = (fx-fz) ** 2 / fz
    stat = chisq.sum(axis = 0)
    degf = k - 1
    pvalue = stats.chi2.cdf(stat,df=degf)
    df = {'statistic': stat, 'p-value': pvalue}    
    df = pd.DataFrame(df) 
    return df   

# from collections import namedtuple
# ks_test_output = namedtuple('ks_test', ('statistic', 'pvalue'))

def ks_testD(x,y,**kwargs):
    x,y, = get_matrix(x),get_matrix(y)
    alpha = kwargs.get("alpha",.05)
    Nx,Ny,D = x.shape[0],y.shape[0],x.shape[1]
    ks = []
    thsld = []
    for i in range(0,D):
        z = stats.ks_2samp(x[:,i],y[:,i])
        ks    += [z[1]]
        # thsld += [np.sqrt(-np.log(alpha/2)*(1+Nx/Ny)/(2*Ny))]
        thsld += [0.05]
    return ks, thsld


def codpy_distance(p,q, type, rescale = True):
    if(type == 'H'):
        return hellinger(p,q)
    elif(type == 'D'):
        import codpypyd as cd
        return op.discrepancy(p,q, rescale = rescale)

def cdfs_compare_plot(fx,fz,**kwargs):
    import matplotlib.pyplot as plt
    # fig = plt.figure()
    fx,fz = np.sort(fx.flatten()),np.sort(fz.flatten())
    max_ = max(fx.shape[0],fz.shape[0])
    x,z = np.arange(start = 0, stop = max_, step = max_/fx.shape[0]),np.arange(start = 0, stop = max_, step = max_/fz.shape[0])
    compare_plot_lists(listfxs=[fx,fz],listxs=[x,z],**kwargs)

def compare_plot_pdf(x,z,labels,title,**kwargs):
    import seaborn as sns
    title = kwargs.get('title',None)
    xlim = kwargs.get('xlim',None)
    kde = kwargs.get('kde',False)
    pdf=pd.DataFrame({labels[1]:z,labels[0]:x})
    sns.displot(pdf,kde=kde)
    if xlim is not None:plt.xlim(xlim[0],xlim[1])
    if title is not None: plt.title(title,fontsize = 8)
    plt.show()


def compare_plot(fx,fz,title="compare distribution",labelx='fx-axis:',labelz='fz-axis:', max = 9):
    import matplotlib.pyplot as plt
    import numpy as np
    import math
    dim = np.shape(fx)[1]
    count = 0
    max = min(math.factorial(dim-1),max)
    if (dim == 1):cdfs_compare_plot(fx,fz,title,labelx,labelz)
    elif (dim == 2):
        fig = plt.figure(figsize=(max * 7, 7))
        fig.suptitle(title)
        plt.scatter(x = fz[:,0],y = fz[:,1],color = 'red',alpha = .5)
        plt.scatter(x = fx[:,0],y = fx[:,1],color = 'blue',alpha = .5)
        plt.xlabel(labelx)
        plt.ylabel(labelz)
        plt.show()           
    else:
        fig = plt.figure(figsize=(max * 7, 7))
        fig.suptitle(title)
        for i in range(0,dim):
            for j in range(i+1, dim):
                count = count + 1
                if count> max:
                    break
                fig.add_subplot(1, max, count)
                plt.scatter(x = fx[:,i],y = fx[:,j],color = 'blue')
                plt.scatter(x = fz[:,i],y = fz[:,j],color = 'red')
                plt.xlabel(labelx + str(i))
                plt.ylabel(labelz + str(j))
        plt.show()           

def experiment(Num,N,D, M = N):
    import numpy as np
    H = []
    Dis = []
    for i in range(1,Num):
        p  = cdf('norm',gendata('norm',0,1, (N, D)))
        q  = cdf('norm',gendata('norm',0,1, (M, D)))
        h = codpy_distance(p,q,'H')
        d = codpy_distance(p,q,'D') 
        H.append(h)
        Dis.append(d)
    return(np.mean(H), np.mean(Dis))    

def confidence_ellipse(x, y, ax, n_std=3.0, facecolor='none', **kwargs):
    from matplotlib.patches import Ellipse
    import matplotlib.transforms as transforms
    if x.size != y.size:
        raise ValueError("x and y must be the same size")
    cov = np.cov(x, y)
    pearson = cov[0, 1]/np.sqrt(cov[0, 0] * cov[1, 1])
    ell_radius_x = np.sqrt(1 + pearson)
    ell_radius_y = np.sqrt(1 - pearson)
    ellipse = Ellipse((0, 0), width=ell_radius_x * 2, height=ell_radius_y * 2,facecolor=facecolor, **kwargs)
    scale_x = np.sqrt(cov[0, 0]) * n_std
    mean_x = np.mean(x)
    scale_y = np.sqrt(cov[1, 1]) * n_std
    mean_y = np.mean(y)
    transf = transforms.Affine2D() \
        .rotate_deg(45) \
        .scale(scale_x, scale_y) \
        .translate(mean_x, mean_y)

    ellipse.set_transform(transf + ax.transData)
    return ax.add_patch(ellipse)

def scatter_hist(x, y, **kwargs):
    from scipy import stats
    figsize=kwargs.get('figsize',(9, 9))
    width_ratios=kwargs.get('width_ratios',(7, 3))
    height_ratios=kwargs.get('height_ratios',(3, 7))
    left=kwargs.get('left',0.1)
    right=kwargs.get('right',0.9)
    bottom=kwargs.get('bottom',0.1)
    top=kwargs.get('top',0.9)
    wspace=kwargs.get('wspace',0.05)
    hspace=kwargs.get('hspace',0.05)
    labelx=kwargs.get('labelx','axis1')
    labely=kwargs.get('labely','axis2')

    fig = kwargs.get('fig',plt.figure(figsize=figsize))
    gs = fig.add_gridspec(2, 2,  width_ratios=width_ratios, height_ratios=height_ratios, left=left, right=right, bottom=bottom, top=top,wspace=wspace, hspace=hspace)
    ax = fig.add_subplot(gs[1, 0])
    ax_histx = fig.add_subplot(gs[0, 0], sharex=ax)
    ax_histy = fig.add_subplot(gs[1, 1], sharey=ax)
    ax_histx.tick_params(axis="x", labelbottom=False)
    ax_histy.tick_params(axis="y", labelleft=False)

    s = kwargs.get('s',2.5)
    c = kwargs.get('c','blue')
    ax.scatter(x, y,s=s,c=c)

    n_std = kwargs.get('n_std',3.0)
    edgecolor = kwargs.get('edgecolor','red')
    linewidth = kwargs.get('linewidth',3)
    label=str(n_std) + 'sigma'
    confidence_ellipse(x, y, ax, n_std=n_std,edgecolor=edgecolor,label=label,linewidth=linewidth)
    # ax.scatter(np.mean(x), np.mean(y), c=s, s=5)
    ax.legend()
    ax.set_xlabel(labelx)
    ax.set_ylabel(labely)
    # bins = int(len(x)/100)
    kde_x = stats.gaussian_kde(x)
    xx = np.linspace(np.min(x), np.max(x), 10000)
    yy = np.linspace(np.min(y), np.max(y), 10000)
    kde_y = stats.gaussian_kde(y)
    bins = kwargs.get('bins',100)
    ax_histx.hist(x,bins=bins,color = c,density=True)
    ax_histx.plot(xx,kde_x(xx))
    ax_histy.hist(y,bins=bins,color = c,density=True, orientation='horizontal')
    ax_histy.plot(kde_y(yy),yy)
    plt.show()

##########################################################################################################################################################
##########################################################################################################################################################
############################################################## Data frame statistics ########################################################
##########################################################################################################################################################
def df_summary(df: DataFrame, **kwargs) :
    """
    author: SMI
    The function outputs summuary statistics.
    """
    out = pd.DataFrame(columns = ['Mean', 'Variance', 'Skewness', 'Kurtosis'], index = df.columns)
    F = kwargs.get('format', "{:.2g}")
    assert isinstance(df, pd.DataFrame), "Data is not pandas data frame."
    out['Mean'] = df.mean(axis=0)
    out['Variance'] = df.skew(axis=0)
    out['Skewness'] = df.var(axis=0)
    out['Kurtosis'] = df.kurtosis(axis=0)
    # format = kwargs.get('format', "{:.2g}")
    format = kwargs.get('format', None)
    if F is not None: out.style.format(format)
    return out

get_stats_df_switchDict = {
                        np.ndarray : lambda x, **kwargs: np.array([get_float(z, **kwargs) for z in x]),
                        }
def stats_df(dfx, dfy, **kwargs) -> DataFrame:
    def transf(df1, df2,**kwargs):
        if isinstance(df1,list):return [transf(x,y) for x,y in zip(df1,df2)]
        format = kwargs.get('format', "{:.2g}")
        return str(format.format(df1))+'(' + format.format(df2) + ')'
    def distance(xy):
        dist = []
        for i in xy:
            temp = compare_distances(i[0],i[1])
            dist+= [temp.to_numpy().flatten()]
        dist = pd.DataFrame(dist, columns= temp.columns).T
        dist.columns = df.columns
        return dist.T
    if isinstance(dfx,list): return [stats_df(fx, fy, **kwargs) for (fx,fy) in zip(dfx, dfy)]
    out = pd.DataFrame()
    summaryx = df_summary(dfx)
    summaryy = df_summary(dfy)
    ks_df, thrsld = ks_testD(dfx, dfy)

    out['Mean'] = transf(summaryx.Mean.to_list(), summaryy.Mean.to_list())
    out['Variance'] = transf(summaryx.Variance.to_list(), summaryy.Variance.to_list())
    out['Skewness'] = transf(summaryx.Skewness.to_list(), summaryy.Skewness.to_list())
    out['Kurtosis'] = transf(summaryx.Kurtosis.to_list(), summaryy.Kurtosis.to_list())
    out['KS test'] = transf(ks_df, thrsld)
    out.index = dfx.columns
    return out

def hellinger(x, y):
    if scipy.sparse.issparse(x) and scipy.sparse.issparse(y):
        x = x.toarray()
        y = y.toarray()
    return np.sqrt(0.5 * ((np.sqrt(x) - np.sqrt(y))**2).sum())

def kl_div(x,y):
    import torch
    import torch.nn.functional as F
    return F.kl_div(torch.Tensor(x).log_softmax(0), torch.Tensor(y).softmax(0)).detach().numpy()

def compare_distances(p,q):
    import pandas as pd
    KL = kl_div(p,q)
    D = codpy_distance(p,q,'D') 
    df = {'KL': [KL], 'MMD': [D]} 
    df = pd.DataFrame(df)     
    return df



def qq_plot(x,z,labels,title,figsize=(8, 6)):
    x = x.copy()
    x.sort()
    z= z.copy()
    z.sort()
    plt.figure(figsize=figsize)
    plt.plot(x,label=labels[0])
    plt.plot(z,label=labels[1])
    plt.legend()
    plt.title(title)
    plt.axis("image")
    plt.axis("tight")
    plt.show()


#def hellinger(p,q, idx = 0):
#     # p,q are two distribution functions
#     import scipy
#     import numpy
#     if len(p) != len(q): return float('NaN')
#     (xp,yp) = ecdf(p)
#     (xq,yq) = ecdf(q)
#     (xpb,ypb) = (xp.copy(),yp.copy())
#     min = numpy.amin((xp,xq))
#     numpy.insert(arr = xpb, obj = 0, values = (min))
#     min = numpy.amin((yp,yq))
#     numpy.insert(arr = ypb, obj = 0, values = (min))
#     max = numpy.amax((xp,xq))
#     numpy.append(xpb,[max])
#     max = numpy.amax((yp,yq))
#     numpy.append(ypb,[max])

#     fun = scipy.interpolate.interp1d(x=xp,y=yp,axis=0,bounds_error=False,fill_value=(0.,1.))
#     from scipy.linalg import norm
#     sqrt2 = np.sqrt(2)
#     H = np.sqrt(fun(xq))
#     H = H-np.sqrt(yq)
#     H = norm(H) / sqrt2
#     #df = {'H(p;q)': [H]} 
#     return H

if __name__ == "__main__":
    print("OK")
    #N = 1000
    #D = 1
    #print(experiment(1000,N,D))
    #random_sample = np.random.multinomial(100, fx[:,0])
    # N = 500
    # M = 1000
    # D = 2
    N = 1000
    D = 10
    print(test(N,D, 'min'))