from preamble import *


def get_codpy_param_chap2():
    import tensorflow as tf
    return  {'rescale_kernel':{'max': 1500, 'seed':42},
    'debug' : True,
    'sharp_discrepancy':{'max': 1000, 'seed':42},
    'discrepancy':{'max': 1000, 'seed':42},
    'validator_compute': ['accuracy_score','discrepancy_error','inertia'],
    # 'set_codpy_kernel' : kernel_setters.kernel_helper(kernel_setters.set_tensornorm_kernel, 0,1e-8 ,map_setters.set_unitcube_map),
    # 'set_codpy_kernel' : kernel_setters.kernel_helper(kernel_setters.set_gaussian_kernel, 0,1e-8 ,map_setters.set_mean_distance_map),
    'set_codpy_kernel' : kernel_setters.kernel_helper(kernel_setters.set_gaussianper_kernel,2,1e-8,None),
    'rescale': True,
    'sharp_discrepancy:itermax':30,
    'tfRegressor' : {'epochs': 50,
        'batch_size':16,
        'validation_split':0.1,
        'loss':tf.keras.losses.mean_squared_error,
        'optimizer':tf.keras.optimizers.Adam(0.001),
        'layers':[8,64,64,1],
        'activation':['relu','relu','relu','linear'],
        'metrics':['mse']  
    }
    }

def a1a2a5(kwargs=get_codpy_param_chap2()) :
    data_random_generator_ = data_random_generator(fun = my_fun, types=["cart","sto","cart"])
    scenarios_list = kwargs.get('scenarios_list',[ (2, 100*(i**2), 100*(i**2),100*(i**2) ) for i in np.arange(5,1,-1)])
    scenario_generator_ = scenario_generator()
    scenario_generator_.run_scenarios(scenarios_list,data_random_generator_,codpyexRegressor(set_kernel = set_per_kernel),data_accumulator(),data_generator_crop = False, **kwargs)
    results = scenario_generator_.accumulator.get_output_datas().dropna(axis=1)
    df_sup_resultsN = results
    list_results = [(s.z,s.f_z) for s in scenario_generator_.accumulator.predictors]
    list_of_list_results = list_results
    scenario_generator_.run_scenarios(scenarios_list,data_random_generator_,ScipyRegressor(set_kernel = set_per_kernel),data_accumulator(), data_generator_crop = False,**kwargs)
    results = scenario_generator_.accumulator.get_output_datas().dropna(axis=1)
    df_sup_resultsN = pd.concat([df_sup_resultsN, results])
    list_of_list_results = list_of_list_results + list_results
    return list_results,list_of_list_results,df_sup_resultsN



def list_of_predictors(kwargs=get_codpy_param_chap2()):
    kwargs['set_codpy_kernel'] =    kernel_setters.kernel_helper(kernel_setters.set_gaussian_kernel, 0,0 ,map_setters.set_unitcube_map)
    scenarios_list = kwargs.get('scenarios_list',[ (2, 10, i,10 ) for i in np.arange(3,1,-1)])
    scenario_generator_ = scenario_generator()
    scenario_generator_.run_scenarios(scenarios_list,data_blob_generator(),scikitClusterClassifier(),cluster_accumulator(), **kwargs)
    results = scenario_generator_.accumulator.get_output_datas().dropna(axis=1)
    df_unsup_results = results
    preds = [(s) for s in scenario_generator_.accumulator.predictors]
    list_of_predictors = preds[0:2]
    scenario_generator_.run_scenarios(scenarios_list,data_blob_generator(),codpyClusterPredictor(),cluster_accumulator(), **kwargs)
    results = scenario_generator_.accumulator.get_output_datas().dropna(axis=1)
    df_unsup_results = pd.concat([df_unsup_results, results])
    preds = [(s) for s in scenario_generator_.accumulator.predictors]
    list_of_predictors += preds[0:2]
    return list_of_predictors, scenario_generator_,df_unsup_results

def my_fun(x):
    import numpy as np
    from math import pi
    sinss = np.cos(2 * x * pi)
    if x.ndim == 1 : 
        sinss = np.prod(sinss, axis=0)
        ress = np.sum(x, axis=0)
    else : 
        sinss = np.prod(sinss, axis=1)
        ress = np.sum(x, axis=1)
    return ress+sinss



if __name__ == "__main__":
    # list_results,list_of_list_results,df_sup_resultsN = a1a2a5()
    # multi_plot(list_results,plot_trisurf,mp_max_items = 4,mp_ncols = 4, projection='3d')
    list_of_predictors,scenario_generator_,df_unsup_results = list_of_predictors()
    multi_plot(list_of_predictors ,graphical_cluster_utilities.plot_clusters, mp_ncols = 4,xlabel = 'x', ylabel = 'y')
    print(df_unsup_results)



    pass