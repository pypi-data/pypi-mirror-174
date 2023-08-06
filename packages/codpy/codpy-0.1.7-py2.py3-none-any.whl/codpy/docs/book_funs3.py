from preamble import *
plt.close('all')

def get_codpy_param_chap3():
    import tensorflow as tf
    return  {'rescale_kernel':{'max': 1500, 'seed':42},
    'debug' : True,
    'sharp_discrepancy':{'max': 1000, 'seed':42},
    'discrepancy':{'max': 1000, 'seed':42},
    'validator_compute': ['accuracy_score','discrepancy_error','inertia'],
    'set_codpy_kernel' : kernel_setters.kernel_helper(kernel_setters.set_tensornorm_kernel, 2,1e-8 ,map_setters.set_unitcube_map),
    # 'set_codpy_kernel' : kernel_setters.kernel_helper(kernel_setters.set_gaussian_kernel, 0,1e-8 ,map_setters.set_mean_distance_map),
    'rescale': True,
    'sharp_discrepancy:itermax':30,
    }


def my_fun(x):
    import numpy as np
    from math import pi
    coss = np.cos(2 * x * pi)
    if x.ndim == 1 : 
        coss = np.prod(coss, axis=0)
        ress = np.sum(x, axis=0)
    else : 
        coss = np.prod(coss, axis=1)
        ress = np.sum(x, axis=1)
    return ress+coss

def nabla_my_fun(x):
    import numpy as np
    from math import pi
    sinss = np.cos(2 * x * pi)
    if x.ndim == 1 : 
        sinss = np.prod(sinss, axis=0)
        D = len(x)
        out = np.ones((D))
        def helper(d) : out[d] += 2.* sinss * pi*np.sin(2* x[d] * pi) / np.cos(2 * x[d] * pi)
        [helper(d) for d in range(0,D)]
    else:
        sinss = np.prod(sinss, axis=1)
        N = x.shape[0]
        D = x.shape[1]
        out = np.ones((N,D))
        def helper(d) : out[:,d] += 2.* sinss * pi*np.sin(2* x[:,d] * pi) / np.cos(2 * x[:,d] * pi)
        [helper(d) for d in range(0,D)]
    return out


def fun_extrakernel(kwargs = get_codpy_param_chap3()):
    data_random_generator_ = data_random_generator(fun = my_fun,types=["cart","cart","cart"])
    data_accumulator_ = data_accumulator()
    scenarios_list = [ (1, 100, 100 ,100 ) ]
    scenario_generator_ = scenario_generator()

    kwargs['set_codpy_kernel'] = kernel_setters.kernel_helper(kernel_setters.set_gaussianper_kernel,2,1e-8,None)
    scenario_generator_.run_scenarios(scenarios_list,data_random_generator_,codpyexRegressor(**kwargs),data_accumulator_,**kwargs)

    kwargs['set_codpy_kernel'] = kernel_setters.kernel_helper(kernel_setters.set_gaussianper_kernel,0,1e-8,None)
    scenario_generator_.run_scenarios(scenarios_list,data_random_generator_,codpyexRegressor(**kwargs),data_accumulator_,**kwargs)

    kwargs['set_codpy_kernel'] = kernel_setters.kernel_helper(kernel_setters.set_gaussian_kernel,0,1e-8,map_setters.set_standard_mean_map)
    scenario_generator_.run_scenarios(scenarios_list,data_random_generator_,codpyexRegressor(**kwargs),data_accumulator_,**kwargs)

    kwargs['set_codpy_kernel'] = kernel_setters.set_linear_regressor_kernel
    scenario_generator_.run_scenarios(scenarios_list,data_random_generator_,codpyexRegressor(**kwargs),data_accumulator_,**kwargs)

    list_results = [(a,b) for a,b in zip(scenario_generator_.accumulator.get_zs(),scenario_generator_.accumulator.get_f_zs())]
    f_names=["linear / periodic, no map", "periodic, no map","matern kernel, no map", "linear regressor kernel, no map"]
    multi_plot(list_results,plot1D,mp_max_items = -1,f_names=f_names,mp_ncols = len(f_names))

def fun_741(kwargs = get_codpy_param_chap3()):
    set_kernel = set_gaussian_kernel
    scenarios_list = [ (2, 500, i,500 ) for i in np.arange(10,100,5)]
    validator_compute=['discrepancy_error','inertia']
    scenario_generator_ = scenario_generator()
    scenario_generator_.run_scenarios(scenarios_list,data_blob_generator(blob_nb=5),scikitClusterClassifier(set_kernel = set_kernel),cluster_accumulator(),**kwargs)
    scenario_generator_.run_scenarios(scenarios_list,data_blob_generator(blob_nb=5),codpyClusterClassifier(set_kernel = set_kernel),cluster_accumulator(),**kwargs)
    scenario_generator_.run_scenarios(scenarios_list,data_blob_generator(blob_nb=5),MinibatchClusterClassifier(set_kernel = set_kernel),cluster_accumulator(),**kwargs)
    scenario_generator_.compare_plots(axis_field_labels = [("Ny","discrepancy_errors"),("Ny","inertia")])

def fun_part(kwargs = get_codpy_param_chap3()):
    partxxz = op.projection(x,x,z, **kwargs).T
    temp = int(np.sqrt(Nz))
    multi_plot([(z,partxxz[0,:]),(z,partxxz[int(temp/3),:])] + [(z,partxxz[int(temp*2/3),:]),(z,partxxz[temp-1,:])],plot_trisurf,projection='3d',elev = 30, mp_max_items = 4, mp_ncols =  4)

def fun_nabla1(kwargs = get_codpy_param_chap3()):
    nabla_f_x = op.nabla(x=x,y=x,z=z,fx=fx,**kwargs)
    multi_plot([(z,nabla_fz[:,0,:]),(z,nabla_f_x[:,0,:]),(z,nabla_fz[:,1,:]),(z,nabla_f_x[:,1,:])],plot_trisurf,projection='3d', mp_max_items = 4, mp_ncols =  4)

def fun_nablaTnabla(kwargs = get_codpy_param_chap3()):
    f1 = op.nablaT(x,y,x,op.nabla(x,y,x,fx,**kwargs),**kwargs)
    f2 = op.nablaT_nabla(x,y,fx,**kwargs)
    multi_plot([(x,f1),(x,f2)],plot_trisurf,projection='3d')

def fun_NablainvNabla1(kwargs = get_codpy_param_chap3()):
    fz_inv = op.nabla_inv(x,y,x,op.nabla(x,y,x,fx, **kwargs))
    multi_plot([(x,fx),(x,fz_inv)],plot_trisurf,projection='3d')

def fun_NablainvNabla2(kwargs = get_codpy_param_chap3()):
    fz_inv = op.nabla_inv(x,y,z,op.nabla(x,y,x,fx, **kwargs))
    multi_plot([(x,fx),(x,fz_inv)],plot_trisurf,projection='3d')

def fun_Delta1(kwargs = get_codpy_param_chap3()):
    temp = op.nablaT_nabla_inv(x,y,op.nablaT_nabla(x,y,fx, **kwargs), **kwargs)
    multi_plot([(x,fx),(x,temp)],plot_trisurf,projection='3d')

def fun_Delta2(kwargs = get_codpy_param_chap3()):
    temp = op.nablaT_nabla_inv(x,y,fx, **kwargs)
    temp = op.nablaT_nabla(x,y,temp, rescale=True)
    multi_plot([(x,fx),(x,temp)],plot_trisurf,projection='3d')

def fun_Integral(kwargs = get_codpy_param_chap3()):
    temp = op.nablaT(x,y,x,op.nablaT_inv(x,y,x,fx,**kwargs))
    multi_plot([(x,fx),(x,temp)],plot_trisurf,projection='3d',elev = 30)

def LerayT(kwargs = get_codpy_param_chap3()):
    LerayT_fz = op.nabla(x,y,z,op.nabla_inv(x,y,z,nabla_fz,**kwargs))
    multi_plot([(z,nabla_fz[:,0,:]),(z,LerayT_fz[:,0,:]),(z,nabla_fz[:,1,:]),(z,LerayT_fz[:,1,:])],plot_trisurf,projection='3d', mp_max_items = 4, mp_ncols =  4)

def Leray(kwargs = get_codpy_param_chap3()):
    Leray_fz = nabla_fz - op.nabla(x,y,z,op.nabla_inv(x,y,z,nabla_fz,**kwargs))
    multi_plot([(z,nabla_fz[:,0,:]),(z,Leray_fz[:,0,:]),(z,nabla_fz[:,1,:]),(z,Leray_fz[:,1,:])],plot_trisurf, projection='3d', mp_max_items = 4, mp_ncols =  4)

#######global variables
D, Nx,Ny,Nz=2,500,500,500
data_random_generator_ = data_random_generator(fun = my_fun,nabla_fun = nabla_my_fun, types=["cart","cart","cart"])
x,y,z,fx,fy,fz,nabla_fx,nabla_fz,Nx,Ny,Nz =  data_random_generator_.get_raw_data(D=D,Nx=Nx,Ny=Ny,Nz=Nz)



if __name__ == "__main__":
    fun_nabla1()
    fun_741()
    fun_Delta1()
    pass