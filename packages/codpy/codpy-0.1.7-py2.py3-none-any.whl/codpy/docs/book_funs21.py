from preamble import *
from pytorch_operators import *
plt.close('all')

def my_fun_torch(x):
    import numpy as np
    from math import pi
    type_ = type(x)
    if not isinstance(x,torch.Tensor) : 
        x = torch.tensor(x, requires_grad=True)
    sinss = torch.cos(2 * x * pi)
    if x.dim() == 1 : 
        sinss = torch.prod(sinss, dim=0)
        ress = torch.sum(x, dim=0)
    else : 
        sinss = torch.prod(sinss, dim=1)
        ress = torch.sum(x, dim=1)
    return ress+sinss


def set_global_chap4():
    D,Nx,Ny,Nz=2,500,500,500
    data_random_generator_ = data_random_generator(fun = my_fun,nabla_fun = nabla_my_fun, types=["cart","cart","cart"])
    x,y,z,fx,fy,fz,nabla_fx,nabla_fz,Nx,Ny,Nz =  data_random_generator_.get_raw_data(D=D,Nx=Nx,Ny=Ny,Nz=Nz)

def testAAD(f,x):
    y = f(x)
    gradf=AAD.gradient(f,x)
    grad1 = gradf[:,0]
    gradf = AAD.hessian(f,x)
    grad2 = gradf[:,0]
    aa = x.detach().numpy()[:,0]
    yy = y.detach().numpy()[:,0]
    title_list = ["cubic", "1st derivative", "2nd derivative"]
    multi_plot([(aa,yy),(aa,grad1), (aa,grad2)], plotD,mp_ncols = 3, f_names=title_list, mp_max_items = 4)

def get_param21():
    return {
        'PytorchRegressor':
        {'epochs': 500,
        'layers': [128,128,128,128],
        'loss': nn.MSELoss(),
        'activations': [nn.ReLU(),nn.ReLU(),nn.ReLU(),nn.ReLU()],
        'optimizer': torch.optim.Adam,
        },
        'codpy_param':
        {
        #'set_codpy_kernel': kernel_setters.kernel_helper(kernel_setters.set_gaussian_kernel, 2 ,1e-8 ,map_setters.set_unitcube_mean_map),
        # 'set_codpy_kernel': kernel_setters.kernel_helper(kernel_setters.set_linear_regressor_kernel, 3 ,1e-8 ,None),
        #'set_codpy_kernel':  kernel_setters.kernel_helper(kernel_setters.set_multiquadricnorm_kernel, 2 ,1e-8 ,map_setters.set_unitcube_mean_map),
        'set_codpy_kernel':kernel_setters.kernel_helper(kernel_setters.set_gaussianper_kernel,2,1e-8,None),
        'rescale' : True,
        }}

def benchmark_gradient(x,z,fx,**kwargs):
    fun = kwargs.get('fun')
    nabla_fz = AAD.gradient(fun,z)
    fz = fun(z).detach().numpy()
    D = x.shape[1]
    # x,y,z,fx,fy,fz,Nx,Ny,Nz = data_random_generator(**kwargs).get_raw_data(D=1,Nx=500,Ny=500,Nz=500)    
    pytorch_grad1 = elapsed_time(lambda : pytorch.nabla(x=x,y=x,z=z,fx=fx,**kwargs),msg="torch nabla:")
    pytorch_grad2 = elapsed_time(lambda : pytorch.nabla(x=x,y=x,z=z,fx=fx,**kwargs),msg="torch nabla:")
    pytorch_f_z =  elapsed_time(lambda : pytorch.projection(x=x,y=x,z=z,fx=fx,**kwargs),msg="torch projection:")

    codpy_grad = elapsed_time(lambda : op.nabla(x=x,y=x,z=z,fx=fx,**kwargs),msg="codpy nabla:")
    codpy_f_z = elapsed_time(lambda : op.projection(x=x,y=x,z=z,fx=fx,**kwargs),msg="codpy projection:")

    rmse_delta_codpy = get_relative_mean_squared_error(codpy_grad,nabla_fz)
    rmse_delta_pytorch = get_relative_mean_squared_error(pytorch_grad1,nabla_fz)
    print("RMSE delta codpy:",rmse_delta_codpy)
    print("RMSE delta pytorch:",rmse_delta_pytorch)

    list_results = [(x,fx),(z,fz),(z,pytorch_f_z),(z,codpy_f_z),(z,nabla_fz[:,0,:]),(z,codpy_grad[:,0,:]),(z,pytorch_grad1[:,0]),(z,pytorch_grad2[:,0])]
    f_names=["training set","ground truth values","Pytorch f","Codpy f","exact grad","codpy grad","pytorch grad-1","pytorch grad-2"]
    if D==1: multi_plot(list_results,plot1D,mp_max_items = len(list_results), mp_ncols = 4,f_names=f_names)
    else: multi_plot(list_results,plot_trisurf,projection='3d', mp_ncols = 4, mp_max_items = len(list_results),f_names=f_names,elev = 25,azim=-80,linewidth = 0.2,antialiased = True,figsize=(9,9))
    #else: multi_plot(list_results,plot_trisurf,projection='3d', mp_ncols = len(list_results), mp_max_items = len(list_results),f_names=["exact","pytorch","codpy"],antialiased = True,figsize=(9,9))


def differentialMlBenchmarks(D,N):
    set_kernel = kernel_setters.kernel_helper(kernel_setters.set_gaussianper_kernel,2,1e-8,None)
    x,y,z,fx,fy,fz,Nx,Ny,Nz = data_random_generator(fun = my_fun_torch, types=["cart","cart","cart"]).get_raw_data(D=D,Nx=N,Ny=N,Nz=N)    
    benchmark_gradient(x = x, z=z, fx=fx,set_codpy_kernel = set_kernel, rescale = True,**get_param21(),fun = my_fun_torch, types=["cart","cart","cart"])


def taylor_test(**kwargs):
    numbers = kwargs.get("numbers",(1, 500, 500, 500 ))
    scenarios = ts_scenario_generator()
    function = kwargs.get('function',my_fun)
    random_generator = kwargs.get('random_generator',AAD_data_random_generator)
    generator_ = [random_generator(fun = function, types=["sto","sto","sto"], **kwargs),random_generator(fun = function, types=["sto","sto","sto"], **kwargs)]
    predictor_ = [pytorch_taylor(**kwargs,set_data = False), codpy_taylor(**kwargs,set_data = False)]
    dic_kwargs = [{ "numbers":numbers, "generator":generator,"predictor":predictor, **predictor.get_new_params(**kwargs)} for generator,predictor in zip(generator_,predictor_)]
    scenarios.run_scenarios(dic_kwargs, data_accumulator())
    # return scenarios
    x,z,fx,f_z, fz = scenarios.accumulator.get_xs()[0], scenarios.accumulator.get_zs()[0], scenarios.accumulator.get_fxs()[0], scenarios.accumulator.get_f_zs(), scenarios.accumulator.get_fzs()[0]
    f_zaad = f_z[0]
    f_zk = f_z[1]
    order = kwargs.get('taylor_order', [])
    D = numbers[0]
    list_results,f_names = [ (z,fz),(z,f_zk),(z,f_zaad)], ["z, fz (AAD ord.)" +str(order),"Codpy ord." + str(order),"Pytorch ord."  + str(order)]
    if D==1: multi_plot(list_results,plot1D,mp_max_items = len(list_results),mp_ncols = 3,f_names=f_names)
    else: multi_plot(list_results,plot_trisurf,projection='3d', mp_ncols = 4, mp_max_items = len(list_results),f_names=f_names,elev = 25,azim=-80,linewidth = 0.2,antialiased = True,figsize=(9,9))



if __name__ == "__main__":
    differentialMlBenchmarks(D=1,N=500)
    taylor_test(**get_param21(),taylor_order = 2)
    taylor_test(**get_param21(),taylor_order = 2,numbers = (2, 500, 500, 500 ), Z_min=-1.1,Z_max=1.1,)

    pass
