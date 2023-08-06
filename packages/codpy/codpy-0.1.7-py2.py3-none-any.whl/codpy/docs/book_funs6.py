from preamble import *
plt.close('all')
from clustering import *

MNIST_data_generator_ = MNIST_data_generator()

set_kernel = set_gaussian_kernel

def set_kernel_chap6():
    kernel_setters.kernel_helper(kernel_setters.set_tensornorm_kernel, 2,1e-8 ,map_setters.set_unitcube_map)()

def set_global_chap6():
    codpy_param = {'rescale:xmax': 1000,
    'rescale:seed':42,
    'sharp_discrepancy:xmax':1000,
    'sharp_discrepancy:seed':30,
    'sharp_discrepancy:itermax':5,
    'discrepancy:xmax':500,
    'discrepancy:ymax':500,
    'discrepancy:zmax':500,
    'discrepancy:nmax':2000,
    'validator_compute': ['accuracy_score','discrepancy_error','inertia'],
    'set_codpy_kernel' : kernel_setters.kernel_helper(kernel_setters.set_tensornorm_kernel, 2,1e-8 ,map_setters.set_unitcube_map),
    'rescale' : True
    }
    return codpy_param

class MNISTClusterClassifier(codpyClusterClassifier):
    def copy(self):
        return self.copy_data(MNISTClusterClassifier())
    def predictor(self,**kwargs):
        kwargs['set_codpy_kernel'] = kwargs.get("set_codpy_kernel",self.set_kernel)
        kwargs['rescale'] = kwargs.get("rescale",True)
        x = self.x
        # self.y = alg.sharp_discrepancy(x = x, Ny=self.Ny,**kwargs)
        self.y = alg.match(x = x, Ny=self.Ny,**kwargs)

        if (self.x is self.z):
            self.f_z = self.fx
        else: 
            up = unity_partition(fx = self.fx)
            debug = op.projection(x = self.x,y = self.y,z = self.z,fx = up,**kwargs)
            self.f_z = softmaxindice(debug,axis=1)
        # if len(self.fx) : self.f_z = remap(self.f_z,get_surjective_dictionnary(fx,self.fx))
        pass
    def id(self,name = ""):
        return "codpy"


def housing_scenario():
    data_generator_ = Boston_data_generator()
    x, fx, x, fx, z, fz = data_generator_.get_data(-1, -1, -1, -1)
    length_ = len(x)
    scenarios_list = [ (-1, i, i, -1)  for i in np.arange(length_,20,-(length_-20)/10) ]
    pd_scenarios_list = pd.DataFrame(scenarios_list)
    return scenarios_list, pd_scenarios_list

def MNIST_clustring(scenarios_list = [ (-1, 1000, 2**i,-1) for i in np.arange(7,9,1)],codpy_param = set_global_chap6()):
    from mnist_codpy import show_mnist_pictures
    codpy_param['set_codpy_kernel'] = kernel_setters.kernel_helper(kernel_setters.set_gaussian_kernel, 0,1e-8 ,map_setters.set_standard_mean_map)
    set_kernel = set_gaussian_kernel
    scenario_generator_ = scenario_generator()
    pd_scenarios_list = pd.DataFrame(scenarios_list)
    
    scenario_generator_.run_scenarios(scenarios_list,MNIST_data_generator(),scikitClusterClassifier(set_kernel = set_kernel),cluster_accumulator(),**codpy_param)
    results = scenario_generator_.accumulator.get_output_datas().dropna(axis=1)
    y1 = scenario_generator_.accumulator.get_ys()
    mnist_results = results

    scenario_generator_.run_scenarios(scenarios_list,MNIST_data_generator(),MNISTClusterClassifier(set_kernel = set_kernel),cluster_accumulator(),**codpy_param)
    results = scenario_generator_.accumulator.get_output_datas().dropna(axis=1)
    y2 = scenario_generator_.accumulator.get_ys()
    mnist_results = pd.concat([mnist_results, results])
    data_plot = [y1[n] for n in range(len(y1))] + [y2[n] for n in range(len(y2))]
    f_names = ["K-Means clusters:" +str(len(y1[n])) for n in range(len(y1))] + ["codpy clusters:" +str(len(y2[n])) for n in range(len(y2))]
    multi_plot(data_plot,fun_plot = show_mnist_pictures,mp_ncols = 2, f_names=f_names,mp_max_items = 10)
    return scenario_generator_, mnist_results

def german_credit(codpy_param = set_global_chap6()):
    scenarios_list = [(-1, -1, i,-1) for i in range(10, 21,10)]
    scenario_generator_ = scenario_generator()
    pd_scenarios_list = pd.DataFrame(scenarios_list)
    scenario_generator_.run_scenarios(scenarios_list,german_credit_data_generator(),scikitClusterPredictor(set_kernel = set_kernel),cluster_accumulator(),**codpy_param)
    results = scenario_generator_.accumulator.get_output_datas().dropna(axis=1)
    german_credit_results = results
    list_of_predictors = [scenario_generator_.predictor]
    scenario_generator_.run_scenarios(scenarios_list,german_credit_data_generator(),codpyClusterPredictor(set_kernel = set_kernel),cluster_accumulator(),**codpy_param)
    results = scenario_generator_.accumulator.get_output_datas().dropna(axis=1)
    german_credit_results = pd.concat([german_credit_results, results])
    list_of_predictors += [scenario_generator_.predictor]
    multi_plot(list_of_predictors ,graphical_cluster_utilities.plot_clusters, mp_ncols = 4)
    return scenario_generator_, german_credit_results

def credit_card_marketing(codpy_param = set_global_chap6()):
    scenarios_list = [(-1, -1, i,-1) for i in np.arange(2,21,3)]
    scenario_generator_ = scenario_generator()
    scenario_generator_.run_scenarios(scenarios_list,credit_card_data_generator(),scikitClusterPredictor(set_kernel = set_kernel),cluster_accumulator(),**codpy_param)
    results = scenario_generator_.accumulator.get_output_datas().dropna(axis=1)
    marketing_results = results
    preds = [(s) for s in scenario_generator_.accumulator.predictors]
    list_of_predictors = preds[0:2]

    scenario_generator_.run_scenarios(scenarios_list,credit_card_data_generator(),scikitClusterPredictor(set_kernel = set_kernel),cluster_accumulator(),**codpy_param)
    results = scenario_generator_.accumulator.get_output_datas().dropna(axis=1)
    marketing_results = pd.concat([marketing_results, results])
    preds = [(s) for s in scenario_generator_.accumulator.predictors]
    list_of_predictors += preds[0:2]

    multi_plot(list_of_predictors ,graphical_cluster_utilities.plot_clusters, mp_ncols = 4)
    return scenario_generator_, marketing_results

def credit_card_fraud(codpy_param = set_global_chap6()):
    #scenarios_list = [( -1, -, i,-1 ) for i in np.arange(15,100,15)]
    scenarios_list = [( -1, 1000, i,-1 ) for i in np.arange(15,100,15)]
    scenario_generator_ = scenario_generator()
    scenario_generator_.run_scenarios(scenarios_list,credit_card_fraud_data_generator(),scikitClusterClassifier(set_kernel = set_kernel),cluster_accumulator(),**codpy_param)
    results = scenario_generator_.accumulator.get_output_datas().dropna(axis=1)
    list_of_predictors = [scenario_generator_.predictor]
    fraud_results = results
    scenario_generator_.run_scenarios(scenarios_list,credit_card_fraud_data_generator(),codpyClusterClassifier(set_kernel = set_kernel),cluster_accumulator(),**codpy_param)
    results = scenario_generator_.accumulator.get_output_datas().dropna(axis=1)
    list_of_predictors += [scenario_generator_.predictor]
    fraud_results = pd.concat([fraud_results, results])
    title_list = ["MMD:CodPy", "k-means"]
    multi_plot(list_of_predictors,add_confusion_matrix.plot_confusion_matrix,mp_ncols = 2, f_names=title_list, mp_max_items = 4)
    return scenario_generator_, fraud_results

def stocks_clustering(codpy_param = set_global_chap6()):
    scenarios_list = [(-1, -1, i,-1) for i in range(10, 21,10)]
    scenario_generator_ = scenario_generator()

    scenario_generator_.run_scenarios(scenarios_list,company_stock_movements_data_generator(),scikitClusterPredictor(set_kernel = set_kernel),cluster_accumulator(),**codpy_param)
    results = scenario_generator_.accumulator.get_output_datas().dropna(axis=1)
    idx = scenario_generator_.predictor.get_map_cluster_indices()
    stocks_results = results

    scenario_generator_.run_scenarios(scenarios_list,company_stock_movements_data_generator(),scikitClusterPredictor(set_kernel = set_kernel),cluster_accumulator(),**codpy_param)
    results = scenario_generator_.accumulator.get_output_datas().dropna(axis=1)
    idx2 = scenario_generator_.predictor.get_map_cluster_indices()
    stocks_results = pd.concat([stocks_results, results])
    return scenario_generator_, idx, idx2, stocks_results


if __name__ == "__main__":
    # scenario_generator_, mnist_results = MNIST_clustring()
    # print(mnist_results)
    # german_credit()
    credit_card_fraud()
    # credit_card_marketing()
    # stocks_clustering()
    pass
