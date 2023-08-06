from numpy import left_shift
from preamble import *

plt.close('all')

def get_codpy_param_chap4():
    return  {'rescale_kernel':{'max': 1000, 'seed':42},
    'sharp_discrepancy':{'max': 1000, 'seed':42},
    'discrepancy':{'max': 1000, 'seed':42},
    'validator_compute': ['accuracy_score','discrepancy_error','norm'],
    # 'set_codpy_kernel' : kernel_setters.kernel_helper(kernel_setters.set_tensornorm_kernel, 0,0 ,map_setters.set_unitcube_map),
    # 'set_codpy_kernel' : kernel_setters.kernel_helper(kernel_setters.set_gaussian_kernel, 0 ,0 ,map_setters.set_standard_min_map),
    'set_codpy_kernel' : kernel_setters.kernel_helper(kernel_setters.set_matern_tensor_kernel, 0,0 ,map_setters.set_standard_mean_map),
    'rescale': True,
    }

def set_kernel_chap4():
    kernel_setters.kernel_helper(kernel_setters.set_tensornorm_kernel, 2,1e-8 ,map_setters.set_unitcube_map)()

def set_global_chap4():
    D,Nx,Ny,Nz=2,500,500,500
    data_random_generator_ = data_random_generator(fun = my_fun,nabla_fun = nabla_my_fun, types=["cart","cart","cart"])
    x,y,z,fx,fy,fz,nabla_fx,nabla_fz,Nx,Ny,Nz =  data_random_generator_.get_raw_data(D=D,Nx=Nx,Ny=Ny,Nz=Nz)

def cost(M): return np.trace(M)

def data_for_static_dist(D = 1, **kwargs):
    import scipy
    N = kwargs.get('N', 1000)
    degf = kwargs.get('degf', 3)
    labels = kwargs.get('f_names')
    left = np.random.normal(5., 1., (int(N/2),D))
    right = np.random.normal(-5., 1., (int(N/2),D))
    left_ = scipy.stats.t.rvs(100, -5., 1.,  (int(N/2),D))
    right_ = scipy.stats.t.rvs(100, 5., 1., (int(N/2),D))
    gaussr = np.concatenate((left,right))
    studr = np.concatenate((left_,right_))
    xy, ys, ls = [], [], []
    if D >= 2:
        dists = [np.random.normal(size = (N, D)),np.random.standard_t(degf,size = (N, D))]
        for l in dists:
            y = alg.sampler(l,**kwargs)[0]
            xy += [(l,y)]  
            ys += [y]
            ls += [l]
            #ds += [compare_distances(x,y)]
    for l in gaussr, studr:
        y = alg.sampler(l,**kwargs)[0]
        xy += [(l,y)]
        ys += [y]
        ls += [l]
    return xy, ls, ys

def LSAP_example():
    N=16
    D = 2
    left = np.random.normal(-3., 1., (int(N/2),D))
    right = np.random.normal(3., 1., (int(N/2),D))
    x0 = np.concatenate( (left,right) )
    y0 = np.random.rand(len(x0),D)
    x,y,permutation = alg.reordering(x=x0,y=y0, set_codpy_kernel = None, distance = "norm2")
    reordering_plot(x0,y0,x,y,plot_fun = graph_plot)
    return x0, y0

def LSAP_ext():
    N=32
    M=16
    D = 2
    left = np.random.normal(-3., 1., (int(N/2),D))
    right = np.random.normal(3., 1., (int(N/2),D))
    x0 = np.concatenate( (left,right) )
    y0 = np.random.rand(M,D)
    x,y,permutation = alg.reordering(x=x0,y=y0, set_codpy_kernel = None, distance = "norm2")
    reordering_plot(x0,y0,x,y,plot_fun = graph_plot)


def figure1D(xy, **kwargs):
    f_names=["Gaussian distribution","t-distribution"]
    kwargs = {'labels': ['sampled', 'generated'], 'title': "Gaussian"}
    multi_plot(xy,fun_plot = hist_plot, f_names = f_names, mp_ncols = 2, **kwargs) 

def figure2D(xy, **kwargs):
    f_names="Gaussian","t-distribution", "Gaussian bimodal", "t-bimodal"
    kwargs = {'labels': ['sampled', 'generated'], 'title': "Gaussian"}
    multi_plot(xy,fun_plot = scatter_plot, f_names = f_names, mp_ncols = 2, **kwargs) 

if __name__ == "__main__":
    set_global_chap4()
    xy, f_x, f_z = data_for_static_dist(**get_codpy_param_chap4(), N=1000, M=501,f_names = ["Gaussian bimodal", "t-bimodal"])
    figure1D(xy, **get_codpy_param_chap4())
    table1 = table(f_x, f_z, xy, f_names = ["Gaussian bimodal", "t-bimodal"])
    print(table1)
    xy, f_x, f_z = data_for_static_dist(D=2, N=1000, M=501,**get_codpy_param_chap4(), f_names = ["Gaussian","t-distribution", "Gaussian bimodal", "t-bimodal"])
    figure2D(xy, **get_codpy_param_chap4())
    #kwargs = {'f_names':["Gaussian bimodal", "t-bimodal"]}
    # xy, f_x, f_z = data_for_static_dist(**get_codpy_param_chap4(), **kwargs)
    # figure1D(xy, **get_codpy_param_chap4())
    print(table(f_x, f_z, xy, **get_codpy_param_chap4()))