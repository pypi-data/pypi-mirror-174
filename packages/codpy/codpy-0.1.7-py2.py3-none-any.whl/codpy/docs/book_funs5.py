from preamble import *
import tensorflow as tf
plt.close('all')
from clustering import *
from housing_prices import *
from radon import *

def set_kernel_chap5():
    kernel_setters.kernel_helper(kernel_setters.set_tensornorm_kernel, 2,1e-8 ,map_setters.set_unitcube_map)()

def set_global_chap5():
    codpy_param = {'rescale:xmax': 1000,
    'rescale:seed':42,
    'sharp_discrepancy:xmax':1000,
    'sharp_discrepancy:seed':30,
    'sharp_discrepancy:itermax':5,
    'discrepancy:xmax':500,
    'discrepancy:ymax':500,
    'discrepancy:zmax':500,
    'discrepancy:nmax':2000,
    'validator_compute': ['accuracy_score','discrepancy_error','norm'],
    'set_codpy_kernel' : kernel_setters.kernel_helper(kernel_setters.set_tensornorm_kernel, 2,1e-8 ,map_setters.set_unitcube_map),
    'rescale' : True
    }
    return codpy_param

def housing_scenario():
    data_generator_ = Boston_data_generator()
    x, fx, x, fx, z, fz = data_generator_.get_data(-1, -1, -1, -1)
    length_ = len(x)
    scenarios_list = [ (-1, i, i, -1)  for i in np.arange(length_,20,-(length_-20)/10) ]
    pd_scenarios_list = pd.DataFrame(scenarios_list)
    return scenarios_list, pd_scenarios_list

def housing(codpy_param = set_global_chap5()):
    data_generator_ = Boston_data_generator()
    x, fx, x, fx, z, fz = data_generator_.get_data(-1, -1, -1, -1)
    length_ = len(x)
    scenarios_list = [ (-1, i, i, -1)  for i in np.arange(length_,20,-(length_-20)/10) ]
    #scenarios_list = [ (-1, 2**(i), -1, 2**(i))  for i in np.arange(5,9,1) ]
    scenario_generator_ = scenario_generator()
    scenario_generator_.run_scenarios(scenarios_list,data_generator_, housing_codpy_extrapolator(**codpy_param), data_accumulator(), **codpy_param)
    results = scenario_generator_.accumulator.get_output_datas().dropna(axis=1)
    df_sup_results = results

    tf_param = {'tfRegressor': {'epochs': 50,
    'batch_size':16,
    'validation_split':0.1,
    'loss':tf.keras.losses.mean_squared_error,
    'optimizer':tf.keras.optimizers.Adam(0.001),
    'layers':[8,64,64,1],
    'activation':['relu','relu','relu','linear'],
    'metrics':['mse']}
    }
    scenario_generator_.run_scenarios(scenarios_list,data_generator_, tfRegressor(**codpy_param), data_accumulator(), **codpy_param,**tf_param)
    results = scenario_generator_.accumulator.get_output_datas().dropna(axis=1)
    df_sup_results = pd.concat([df_sup_results, results])

    scenario_generator_.run_scenarios(scenarios_list,data_generator_, DecisionTreeRegressor(**codpy_param), data_accumulator(), **codpy_param)
    results = scenario_generator_.accumulator.get_output_datas().dropna(axis=1)
    df_sup_results = pd.concat([df_sup_results, results])
    housing_list = df_sup_results

    kwargs = {"mp_max_items" :4, "mp_ncols" : 4 }
    scenario_generator_.compare_plots(
    axis_field_labels = [("Nx","scores"),("Ny","discrepancy_errors"),("Ny","execution_time")],**kwargs)
    return housing_list

def MNIST(codpy_param = set_global_chap5()):
    set_mnist_kernel = kernel_setters.kernel_helper(kernel_setters.set_gaussian_kernel, 0,1e-8 ,map_setters.set_standard_mean_map)
    codpy_param['set_codpy_kernel'] = set_mnist_kernel
    MNIST_data_generator_ = MNIST_data_generator()
    scenarios_list = [ (784, 2**(i), 2**(i-2), 10000)  for i in np.arange(5,9,1)]
    pd_scenarios_list = pd.DataFrame(scenarios_list)
    tf_param = {'tfClassifier' : {'epochs': 10,
    'batch_size':16,
    'validation_split':0.1,
    'loss': tf.keras.losses.SparseCategoricalCrossentropy(from_logits=True),
    'optimizer':tf.keras.optimizers.Adam(0.001),
    'activation':['relu',''],
    'layers':[128,10],
    'metrics':[tf.keras.metrics.SparseCategoricalAccuracy()]} }
    scenario_generator_ = scenario_generator()
    scenario_generator_.run_scenarios(scenarios_list,MNIST_data_generator_,tfClassifier(set_kernel = set_mnist_kernel),data_accumulator(),
    **codpy_param,**tf_param)
    results = scenario_generator_.accumulator.get_output_datas().dropna(axis=1)
    df_sup_results = results
    multi_plot([scenario_generator_.predictor] ,add_confusion_matrix.plot_confusion_matrix,title='')
    scenario_generator_.run_scenarios(scenarios_list,MNIST_data_generator_,codpyexRegressor(set_kernel = set_mnist_kernel), data_accumulator(), **codpy_param)
    results = scenario_generator_.accumulator.get_output_datas().dropna(axis=1)
    df_sup_results = pd.concat([df_sup_results, results])
    scenario_generator_.run_scenarios(scenarios_list,
    MNIST_data_generator_, SVC(set_kernel = set_mnist_kernel), data_accumulator(), **codpy_param)
    results = scenario_generator_.accumulator.get_output_datas().dropna(axis=1)
    df_sup_results = pd.concat([df_sup_results, results])
    scenario_generator_.run_scenarios(scenarios_list,
                                  MNIST_data_generator_,
                                  DecisionTreeClassifier(set_kernel = set_mnist_kernel),
                                  data_accumulator(), **codpy_param)
    results = scenario_generator_.accumulator.get_output_datas().dropna(axis=1)
    df_sup_results = pd.concat([df_sup_results, results])

    scenario_generator_.run_scenarios(scenarios_list,
                                  MNIST_data_generator_,
                                  AdaBoostClassifier(set_kernel = set_mnist_kernel),
                                  data_accumulator(), **codpy_param)
    results = scenario_generator_.accumulator.get_output_datas().dropna(axis=1)
    df_sup_results = pd.concat([df_sup_results, results])
    scenario_generator_.run_scenarios(scenarios_list,
                                  MNIST_data_generator_,
                                  RandomForestClassifier(set_kernel = set_mnist_kernel),
                                  data_accumulator(), **codpy_param)
    results = scenario_generator_.accumulator.get_output_datas().dropna(axis=1)
    df_sup_results = pd.concat([df_sup_results, results])
    mnist_list = df_sup_results
    return scenario_generator_, mnist_list

def SPECT():
    codpy_param = {'rescale:xmax': 1000,
    'rescale:seed':42,
    'sharp_discrepancy:xmax':1000,
    'sharp_discrepancy:seed':30,
    'sharp_discrepancy:itermax':5,
    'discrepancy:xmax':500,
    'discrepancy:ymax':500,
    'discrepancy:zmax':500,
    'discrepancy:nmax':2000,
    'validator_compute': ['accuracy_score']}
    scenarios_list = [ (-1, -1, -1, -1 ) ]
    scenario_generator_,data_accumulator_ = scenario_generator(),data_accumulator(**codpy_param)
    scenario_generator_.run_scenarios(scenarios_list,sub_radon_generator(**codpy_param),sub_radon_predictor_exact(**codpy_param),data_accumulator_,**codpy_param)
    scenario_generator_.run_scenarios(scenarios_list,sub_radon_generator(**codpy_param),sub_radon_predictor_SART(**codpy_param),data_accumulator_,**codpy_param)
    scenario_generator_.run_scenarios(scenarios_list,sub_radon_generator(**codpy_param),sub_radon_predictor_back(**codpy_param),data_accumulator_,**codpy_param)
    results = scenario_generator_.accumulator.get_output_datas().dropna(axis=1)
    return results


if __name__ == "__main__":
    # set_global_chap5()
    MNIST()
    pass
