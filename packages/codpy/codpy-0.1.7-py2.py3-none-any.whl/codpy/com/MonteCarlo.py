import abc
from cmath import isinf
import numpy as np
from codpy_tools import *
from mapping import *
# import openturns as ot
class StochasticProcess(abc.ABC):
    @abc.abstractmethod
    def get_process(self,**kwargs):
        pass


class path_generator(abc.ABC):
    def __init__(self,**kwargs):
        pass
    def get_param(**kwargs): return kwargs.get('path_generator')
    @abc.abstractmethod
    def generate(self,N,payoff,**kwargs):
        pass

    def get_process(**kwargs) : return path_generator.get_param(**kwargs).get('process')
    def get_D(**kwargs) : return path_generator.get_process(**kwargs).get_process(**kwargs).factors()



class payoff(abc.ABC):
    @abc.abstractmethod
    def f(self,x):
        pass
    @abc.abstractmethod
    def get_times(self,**kwargs):
        pass

class pricer(abc.ABC):
    @abc.abstractmethod
    def price(self,**kwargs):pass
    def nabla(self,**kwargs):return FD.nabla(fun = self.price, **kwargs)
    def hessian(self,**kwargs):return FD.hessian(fun = self.price, **kwargs)

    def nablas(self, values,**kwargs): 
        out = get_matrix(FD.nablas(x = values,fun = self.price, **kwargs))
        return out

    def hessians(self, values,**kwargs): 
        out = FD.hessians(fun = self.price,x = values,**kwargs)
        return out
    def prices(self,set_fun, values,**kwargs): 
        copy_kwargs = copy.deepcopy(kwargs)
        values = values.copy() #??
        def helper(v,**k): 
            k = set_fun(v,**k)
            return self.price(**k) 
        if isinstance(values,list): out = [helper(v,**copy_kwargs) for v in get_matrix(values)]
        elif isinstance(values,np.ndarray): out = [helper(values[n],**copy_kwargs) for n in range(0,values.shape[0]) ]
        elif isinstance(values,pd.DataFrame): return self.prices(set_fun, values.values,**copy_kwargs)
        out = np.array(out)

        return out
    def pnls(self,set_fun, x,z,**kwargs): 
        left = self.prices(set_fun, x,**kwargs)
        right = self.prices(set_fun, z,**kwargs)
        pnls = right[:min(len(left),len(right))] - left[:min(len(left),len(right))]

        # from QL_tools import BasketOptionClosedFormula
        # spot = BasketOptionClosedFormula.get_spot_basket(x= z[:,1:],**kwargs)
        # spot,toto,p = lexicographical_permutation(spot,pnls.copy())
        # plt.plot(spot,toto)
        # plt.show()

        # grad = op.nabla(x=x[:,:,0], y=x[:,:,0], z=x[:,:,0], fx=pnls, rescale = True,**kwargs)

        return pnls

class MonteCarloPricer(pricer):

    def get_params(**kwargs) :  return kwargs.get('MonteCarloPricer',{})
    def get_N(**kwargs): return MonteCarloPricer.get_params(**kwargs)['N']

    def price(self,payoff,generator,**kwargs):
        initial_values = kwargs['getter'].get_spot(**kwargs)
        x=generator.generate(payoff=payoff,initial_values = initial_values,**kwargs)
        if isinstance(generator,historical_path_generator): y=payoff.f(x[:,1:,1:],**kwargs)
        else:  y=payoff.f(x)
        out = np.mean(y)
        return out


class historical_path_generator(path_generator):

    def generate_distribution_from_samples_np(**kwargs):
        from QL_tools import option_param_getter
        # seed=kwargs.get("seed",np.random.randint(low = 0,high = 1e+8))
        samples = kwargs['samples']
        sample_times = kwargs['sample_times']
        mapping = kwargs.get("map",None)
        N,D,T = samples.shape[0],samples.shape[1],samples.shape[2]
        mapped_samples=np.zeros((N,D,T))
        if mapping is not None: 
            time_list = list(set(samples[:,0,:].flatten()))
            time_list.sort()
            mapped_samples[:,0,:] = samples[:,0,:]
            mapped_samples[:,1:,:] = mapping(samples[:,1:,:],**kwargs, times = time_list)
        xm = mapped_samples[0,1:,:].T
        x,y,z = alg.get_xyz(fx=xm,**kwargs)


        linear_kernel = kernel_setters.kernel_helper(setter = kernel_setters.set_linear_regressor_kernel,polynomial_order = 2,regularization = 1e-8,set_map = map_setters.set_unitcube_map)
        linear_part = op.projection(x=x,y=y,z=x,fx=xm,set_codpy_kernel=linear_kernel,rescale=True)
        quadratic_part = xm - linear_part
        linear_part = op.projection(x=x,y=y,z=z,fx=xm,set_codpy_kernel=linear_kernel,rescale=True)
        testxm,testx,testz,testl,testq = xm.mean(axis=0),x.mean(axis=0),z.mean(axis=0),linear_part.mean(axis=0),quadratic_part.mean(axis=0)

        set_codpy_kernel = kernel_setters.kernel_helper(kernel_setters.set_matern_tensor_kernel, 0,0 ,map_setters.set_standard_mean_map)
        diffusion_part = alg.sampler(fx= quadratic_part, x=x,y=y,z=z,M = kwargs['Nz'] * len(sample_times), set_codpy_kernel = set_codpy_kernel, rescale = True)[0]
        # out = linear_part + diffusion_part
        # scatter_hist(xm[:,0], xm[:,2], **kwargs)
        # scatter_hist(out[:,0], out[:,2], **kwargs)
        # print( table([xm], [out], f_names=['AAPL', 'AMZN','GOOGL'], format= '{:.1e}') )
        mean = kwargs.get("mean",None)
        if mean is not None:
            linear_part += mean-linear_part.mean(axis=0)


        return diffusion_part,linear_part,mapped_samples[0,1:,:]

    def generate_from_samples(self,**kwargs):
        def generate_from_samples_dataframe(**kwargs):
            samples = kwargs['samples']
            pd_samples = np.ndarray((1,samples.shape[1]+1,samples.shape[0]))
            pd_samples[0,0,:] = get_float(samples.index)
            pd_samples[0,1:,:] = samples.values.T
            out = generate_from_samples_np(**kwargs)
            out = pd.DataFrame(out[:,1:,0],columns = samples.columns,index = out[:,0,0])
            return out
        
        def generate_from_samples_np(**kwargs):
            samples = kwargs['samples']
            sample_times = kwargs['sample_times']
            # kwargs['N'] = kwargs.get('N',10)*len(sample_times)
            diffusion_part,linear_part,fx = historical_path_generator.generate_distribution_from_samples_np(**kwargs)
            out = diffusion_part+linear_part
            # out += fx.mean(axis=0) - out.mean(axis=0)
            out = out
            mean = fx.mean(axis=0)

            payoff_times=get_float(sample_times)

            N = kwargs.get("Nz",samples.shape[0])
            D = samples.shape[1]
            T = len(payoff_times)

            from QL_tools import option_param_getter
            getter = kwargs.get('getter',option_param_getter())
            mapping = kwargs.get("map",None)
            f_z = np.zeros([N,D,T])
            def helper(n,d) : f_z[n,d,:] = payoff_times
            [helper(n,d) for n in np.arange(N) for d in np.arange(D)]
            def helper(n) : f_z[n,1:,:] = out[n*T:(n+1)*T].T
            [helper(n) for n in np.arange(N)]
            if mapping is not None: 
                time_start = get_float(kwargs.get('time_start',getter.get_today_date(**kwargs)))
                payoff_times.insert(0,time_start)
                f_z[:,1:,:] = inverse(mapping)(f_z[:,1:,:],**kwargs, times = payoff_times, mean = mean)
            return f_z
            
        import pandas 
        samples = kwargs['samples']
        generate_from_samples_switchDict = { pandas.core.frame.DataFrame: generate_from_samples_dataframe }
        type_debug = type(samples)
        method = generate_from_samples_switchDict.get(type_debug,generate_from_samples_np)
        return method(**kwargs)

    def generate(self,payoff,time_list=None,**kwargs):
        historical_generator = kwargs.get("historical_generator",None)
        samples = historical_generator.generate(**kwargs)
        if time_list is None: time_list = payoff.get_times(**kwargs)
        # return historical_generator.generate(**kwargs,time_list=time_list)
        return self.generate_from_samples(samples=samples,sample_times=time_list,**kwargs)



class Recurrent_historical_path_generator(historical_path_generator):
    def generate_from_samples(self,samples,sample_times,**kwargs):
        mapping = kwargs.get("map",None)
        if mapping is not None: 
            mapped_samples=np.zeros((samples.shape[0],samples.shape[1],samples.shape[2]-1))
            time_list = list(set(samples[:,0,:].flatten()))
            time_list.sort()
            mapped_samples= mapping(samples,**kwargs, times = time_list)
            x,fx=ts_format(mapped_samples,**kwargs)
        else: x,fx = ts_format(samples,**kwargs)

        return super().generate_from_samples(samples,sample_times,x=x,fx=fx,**kwargs)

def remove_mean(A):
    mean = np.mean(A[:,1,:])
    A[:,1,:] = A[:,1,:] - mean
    return A,mean

def split(A,h):
    out=np.zeros((int(A.shape[2]/h),A.shape[1],h))
    for i in range(int(A.shape[2]/h)):
        out[i,:,:]=A[0,:,i*h:(i+1)*h]
    return out

