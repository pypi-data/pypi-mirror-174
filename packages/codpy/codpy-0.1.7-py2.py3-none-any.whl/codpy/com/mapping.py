import pandas as pd
import numpy as np
from codpy_tools import *
from copy import deepcopy

def inverse(fun):
    inverse_switchDict = {'moment_cartesian_map':inv_moment_cartesian_map,'cartesian_map':inv_cartesian_map,'normal_return':inv_normal_return,'log_ret':inv_log_ret,'log_return':inv_log_return}
    def default_inverse(fun):
        assert(False)
    method = inverse_switchDict.get(fun.__name__,default_inverse)
    return method

def Id(x,**kwargs): return x

def cartesian_map(x,**kwargs):
    out=x.copy()
    list_maps=kwargs.get('list_maps')
    time_list = list(kwargs.get('times',None))
    for i in range(0,len(list_maps)):
        out[:,i,:]=list_maps[i](x[:,i,:],**{'times':time_list})   
    return out

def moment_cartesian_map(x,**kwargs):
    out = cartesian_map(x,kwargs)
    return out

def inv_cartesian_map(x,**kwargs):
    out=x.copy()
    list_maps=kwargs.get('list_maps')
    D = len(list_maps)
    time_list = list(kwargs.get('times',None))
    initial_values = kwargs.get('initial_values',None)
    mean = kwargs.get('mean',np.repeat(None,D))
    for i in range(0,len(list_maps)):
        out[:,i,:]=inverse(list_maps[i])(x[:,i,:],mean = mean[i], times = time_list,initial_values = initial_values[i])         
    return out

def inv_moment_cartesian_map(x,**kwargs):
    out = inv_cartesian_map(x,**kwargs)
    return out

#################################################################################################################
################################################ Normal returns #################################################
#################################################################################################################

def normal_return(x,**kwargs):
    axis = 1
    out = np.diff(x,axis)
    out = np.concatenate([np.zeros((x.shape[0],1)),out],axis=axis)
    times = np.array(kwargs.get('times',None))
    times = np.sqrt(np.diff(times))
    if times is not None:
        def helper(n):
            if len(times.shape)==1:
                if axis==0 : out[n,:] /= times[n]
                else : out[:,n] /= times[n]
            else:
    
                if axis==0 : out[n,:] /= times[n,:]
                else : out[:,n] /= times[:,n]
        [helper(n) for n in range(0,out.shape[1]-1)]
    return out

# def inv_normal_return(x,**kwargs):
#     out = x.copy()
#     axis = 1
#     D = x.shape[0]
#     T = x.shape[1]
#     times = list(kwargs.get('times',None))
#     if times is not None:
#         times = np.sqrt(np.diff(times))
#         def helper(n):
#             if len(times.shape)==1:
#                 if axis==0 : out[n,:] *= times[n]
#                 else : out[:,n] *= times[n]
#             else:
#                 if axis==0 : out[n,:] *= times[n,:]
#                 else : out[:,n] *= times[:,n]
#         [helper(n) for n in range(0,len(times))]
#     out = np.cumsum(out,axis = axis)
#     initial_values = kwargs.get('initial_values',None)
#     if initial_values is not None: 
#         def helper(t): out[:,t] *= initial_values
#         [helper(t) for t in range(0,T)]
#     return out

#################################################################################################################
################################################## Log returns ##################################################
#################################################################################################################

def log_ret(x,**kwargs):
    if (x.ndim == 3):
        out = np.concatenate( [log_ret(x[n],**kwargs).reshape([1,x.shape[1],x.shape[2]]) for n in range(0,x.shape[0])],axis = 0)
        return out
    x = np.log(x)
    out = normal_return(x,**kwargs)
    return get_matrix(out)    

def inv_log_ret(x,**kwargs):
    times = list(kwargs.get('times',None))
    mean = kwargs.get('mean',None)
    # linear_kernel = kernel_setters.kernel_helper(setter = kernel_setters.set_linear_regressor_kernel,polynomial_order = 2,regularization = 1e-8)
    # y = op.projection(x=x,y=x,z=x,fx=x, set_codpy_kernel=linear_kernel)
    out = inv_normal_return(x,times = times,mean=mean,initial_values = 0.)
    initial_values = kwargs.get('initial_values',None)
    T = x.shape[1]
    out = initial_values*np.exp(out)
    return out

#################################################################################################################
######################################### Mean adjusted returns #################################################
#################################################################################################################

def inv_normal_return(x,**kwargs):
    out = x.copy()
    axis = 1
    D = x.shape[0]
    T = x.shape[1]
    times = list(kwargs.get('times',None))
    mean = kwargs.get('mean',None)
    if times is not None:
        times = np.sqrt(np.diff(times))
        def helper(n):
            if len(times.shape)==1:
                if axis==0 : out[n,:] *= times[n]
                else : out[:,n] *= times[n]
            else:
                if axis==0 : out[n,:] *= times[n,:]
                else : out[:,n] *= times[:,n]
        
        [helper(n) for n in range(0,len(times))]
    out = np.cumsum(out,axis = axis)
    if mean is not None:
        out -= np.mean(out, axis = 0)+mean       
    initial_values = kwargs.get('initial_values',None)
    if initial_values is not None: 
        def helper(t): out[:,t] += initial_values
        [helper(t) for t in range(0,T)]
    return out



#################################################################################################################
############################################## Old log returns ##################################################
#################################################################################################################

def log_return(x,**kwargs):
    import xarray
    log_return_switchDict = { pd.DataFrame: lambda x,**kwargs :  log_return_dataframe(x,**kwargs),
                                        xarray.core.dataarray.DataArray: lambda x,**kwargs :  log_return_xarray(x,**kwargs) }
    def log_return_dataframe(x,**kwargs):
        out = x
        columns = kwargs.get("columns",None)
        if columns is not None:
            cols = get_starting_cols(x.columns, columns)
            out[cols] = log_return_np(out[cols].values,**kwargs)
        else:   
            out = pd.DataFrame(log_return_np(out.values,**kwargs), columns = out.columns, index = x.index)
        return out    
    type_debug = type(x)
    def log_return_np(x,**kwargs):
        if (x.ndim == 3):
            out = np.concatenate( [log_return_np(x[n],**kwargs).reshape([1,x.shape[1],x.shape[2]]) for n in range(0,x.shape[0])],axis = 0)
            return out
        if (x.ndim == 1):return log_return_np(get_matrix(x),axis=0,**kwargs)
        axis = kwargs.get('axis',1)
        x = np.log(x)
        D = x.shape[1]
        otheraxis = (axis+1)%2
        out = np.diff(x,axis = axis)
        out = np.concatenate([ out, np.zeros( [out.shape[0],1] )],axis = 1)
        times = list(kwargs.get('times',None))
        if times is not None:
            times = np.sqrt(np.diff(times))
            def helper(n):
                if axis==0 : out[n,:] /= times[n]
                else : out[:,n] /= times[n]
            [helper(n) for n in range(0,len(times))]
        return get_matrix(out)
    def log_return_xarray(x,**kwargs):
        index_string = kwargs.get("axis","N")
        index_time = kwargs.get("index","time")
        indexes = x[index_string]
        out = x
        for index in indexes:
            mat = log_return_np(x[index_string==int(index)].values,axis = 1,**kwargs)
            out[index_string==int(index)] = mat
        return out

    method = log_return_switchDict.get(type_debug,log_return_np)
    return method(x,**kwargs)



def inv_log_return(x,**kwargs):
    inv_log_return_switchDict = { pd.DataFrame: lambda x,**kwargs :  inv_log_return_dataframe(x,**kwargs) }
    def inv_log_return_dataframe(x,**kwargs):
        out = x
        columns = kwargs.get("columns",None)
        if columns is not None:
            cols = get_starting_cols(x.columns, columns)
            out[cols] = inv_log_return_np(out[cols].values,**kwargs)
        else:   
            out = pd.DataFrame(inv_log_return_np(out.values,**kwargs), columns = out.columns, index = x.index)
        return out    
    def inv_log_return_np(x,**kwargs):
        if (x.ndim == 3):
            out = x.copy()
            def helper(n): out[n] = inv_log_return_np(x[n],**kwargs)                 
            [helper(n) for n in range(0,x.shape[0])]
            return out
        out = x.copy()
        axis = 1
        D = x.shape[0]
        T = x.shape[1]
        otheraxis = (axis+1)%2

        times = kwargs.get('times',None)
        if times is not None:
            times = get_float(times)
            times = np.sqrt(np.diff(times))
            def helper(n):
                if axis==0 : out[n,:] *= times[n]
                else : out[:,n] *= times[n]
            [helper(n) for n in range(0,len(times))]

        out = np.cumsum(out,axis = axis)
        out = np.exp(out)
        initial_values = kwargs.get('initial_values',None)
        if initial_values is not None: 
            def helper(t): out[:,t] *= initial_values
            [helper(t) for t in range(0,T)]
        return out

    type_debug = type(x)
    method = inv_log_return_switchDict.get(type_debug,inv_log_return_np)
    return method(x,**kwargs)

