from preamble import *
# from codpy.com.mapping import normal_return
import QuantLib as ql 
import matplotlib.pyplot as plt
import numpy as np
from tqdm import tqdm
import abc
import time
import datetime 
import pandas as pd
import copy
from copy import deepcopy
import matplotlib.pyplot as plt
import statsmodels.api as sm
from stat_tools import *
from scipy.stats import pearsonr
plt.style.use('ggplot')

class Real_historical_generator(time_serie_generator):

    def get_times(**kwargs):
        params = QL_historical_generator.get_params(**kwargs)
        T = params.get("T",None)
        out = []
        today_date = option_param_getter().get_today_date(**kwargs)
        for n in range(T,-1,-1):
            out.append(today_date-datetime.timedelta(days=n))
        return out

    def get_raw_data_csv(**kwargs) : return Real_historical_generator.get_params(**kwargs).get('raw_data_csv',None)
    def get_raw_data(self,**kwargs):
        params = kwargs.get('time_serie_generator')
        # if csv_file is not None and os.path.exists(csv_file): data = pd.read_csv(csv_file,sep=sep, index_col = 0)
        # else: data = Real_historical_generator.get_stocks_data(**kwargs)
        data = Real_historical_generator.get_stocks_data(**kwargs)
        yf_params = time_serie_generator.get_yf_params(**kwargs)
        symbol=params.get('yf_param').get('symbols')[0]
        date_format = yf_params.get('date_format','%d/%m/%Y')
        data = ts_data.interpolate(data,**params, float_fun = lambda x: get_float(x,date_format = date_format))
        samples=np.zeros((1,2,data.shape[0]))
        last_date=data['Date'][-1]
        dates=[]
        for i in range(last_date-data.shape[0]+1,last_date+1):
            dates.append(i)
        samples[0,0,:]=dates

        # samples[0,0,:]=data['Date']
        samples[0,1,:]=data[symbol]
        return samples

    def get_stocks_data(**kwargs):
        yf_params = time_serie_generator.get_yf_params(**kwargs)
        data = ts_data.get_yf_ts_data(**yf_params)
        data.insert(loc=0, column=ts_data.get_time_col(**kwargs), value=get_float(data.index,date_format = ts_data.get_date_format(**kwargs)))
        raw_data_csv = Real_historical_generator.get_raw_data_csv(**kwargs)
        if raw_data_csv is not None and not os.path.exists(raw_data_csv): data.to_csv(raw_data_csv,sep = ts_data.get_sep(**kwargs), index = True)
        return data

class QL_historical_generator(QL_path_generator):

    def get_params(**kwargs) : return kwargs.get('QL_historical_generator',{})
    def get_N(**kwargs) : return QL_historical_generator.get_params(**kwargs).get('N',1)
    def get_T(**kwargs) : return QL_historical_generator.get_params(**kwargs).get('T')
    def get_seed(**kwargs) : return QL_historical_generator.get_params(**kwargs).get('seed',None)

    def get_times(**kwargs):
        params = QL_historical_generator.get_params(**kwargs)
        T = params.get("T",None)
        out = []
        today_date = option_param_getter().get_today_date(**kwargs)
        for n in range(T,-1,-1):
            out.append(today_date-datetime.timedelta(days=n))
        return out

    def get_date_fraction(list,start = None):
        out=[]
        if start is None:
            start=list[0]
        for i in list:
            out.append(ql.Actual365Fixed().yearFraction(date_to_quantlib(start), date_to_quantlib(i)))
        return out

    def get_date_column_name(self,**kwargs):
        return time_serie_generator.get_params(**kwargs).get("time_id","Date")

    def generate(self,**kwargs):
        getter = kwargs['getter']
        Nhist = kwargs.get("Nhist",QL_historical_generator.get_N(**kwargs))
        time_list = kwargs.get("time_list",QL_historical_generator.get_times(**kwargs))
        time_list_float = get_float(time_list)
        fractions=QL_historical_generator.get_date_fraction(time_list)
        process = kwargs.get("process",QL_path_generator.get_process(**kwargs))
        D = kwargs.get("D",QL_path_generator.get_D(**kwargs))
        T=len(time_list)
        out=np.zeros((Nhist,(D+1),T))
        seed = QL_historical_generator.get_seed(**kwargs)
        getter = kwargs['getter']
        ql.Settings.instance().evaluationDate = date_to_quantlib(getter.get_today_date(**kwargs))

        if seed is not None:rng = ql.UniformRandomSequenceGenerator(D * (T-1), ql.UniformRandomGenerator(seed=seed))
        else: rng = ql.UniformRandomSequenceGenerator(D * (T-1), ql.UniformRandomGenerator())
        sequenceGenerator = ql.GaussianRandomSequenceGenerator(rng)
        
        pathGenerator = ql.GaussianMultiPathGenerator(process.get_process(**kwargs),fractions, sequenceGenerator, False)
        def helper(n):
            samplePath = pathGenerator.next()
            values = samplePath.value()
            out[n,0,:] = time_list_float
            out[n,1:,:] = values
            # out[n,1:,:] *= [spot,0.1] / out[n,1:,-1]
        [helper(n) for n in range(0,Nhist,1)]
        return out[:,:,1:]

#################################################################################################################
############################################## Scenarios runners ################################################
#################################################################################################################

### Class to run scenarios of the number of the monte carlo trajectories
class scenarios_N(scenarios_MC):
    def format_output(results):
        xs,fxs,f_xs,errs = np.zeros(len(results)),np.zeros(len(results)),np.zeros(len(results)),np.zeros(len(results))
        for index,r in zip(range(len(results)),results):
                xs[index] = r['N']
                fxs[index]   = r['Thprice']
                f_xs[index]   = r['MCprice']
                errs[index]   = get_relative_mean_squared_error(r['MCprice'],r['Thprice'])
        return xs,fxs,f_xs,errs
    def run_and_format(self,scenarios,**kwargs):
        super().run(scenarios,**kwargs)
        return scenarios_N.format_output(self.results)

### Class to run scenarios of the number observed trajectories with a fixed number of observation per trajectory 
### or for one trajectory with variable number of observations
class scenarios_Nh(scenarios_MC):
    def format_output(results):
        xs,fxs,f_xs,errs = np.zeros(len(results)),np.zeros(len(results)),np.zeros(len(results)),np.zeros(len(results))
        for index,r in zip(range(len(results)),results):
                xs[index] = r['Nh']*r['T']
                fxs[index]   = r['Thprice']
                f_xs[index]   = r['MCprice']
                errs[index]   = get_relative_mean_squared_error(r['MCprice'],r['Thprice'])
        return xs,fxs,f_xs,errs
    def run_and_format(self,scenarios,**kwargs):
        super().run(scenarios,**kwargs)
        return scenarios_Nh.format_output(self.results)

### Class to run scenarios of the maturity date of the option
class scenarios_maturity(scenarios_MC):
    def format_output(results):
        xs,fxs,f_xs,errs = np.zeros(len(results)),np.zeros(len(results)),np.zeros(len(results)),np.zeros(len(results))
        for index,r in zip(range(len(results)),results):
                xs[index] = get_float(r['maturity_date'])
                fxs[index]   = r['Thprice']
                f_xs[index]   = r['MCprice']
                errs[index]   = get_relative_mean_squared_error(r['MCprice'],r['Thprice'])
        return xs,fxs,f_xs,errs
    def run_and_format(self,scenarios):
        super().run(scenarios)
        return scenarios_maturity.format_output(self.results)

### Class to run scenarios over maturity date and the number of observation used to training at the same time
class scenarios_maturity_T(scenarios_MC):
    def format_output(results):
        xs,fxs,f_xs,errs = np.zeros([len(results),2]),np.zeros(len(results)),np.zeros(len(results)),np.zeros(len(results))
        for index,r in zip(range(len(results)),results):
                xs[index,0] = r['Nh']*r['T']
                xs[index,1] = get_float(r['maturity_date'])
                fxs[index]   = r['Thprice']
                f_xs[index]   = r['MCprice']
                errs[index]   = get_relative_mean_squared_error(r['MCprice'],r['Thprice'])
        return xs,fxs,f_xs,errs
    def run_and_format(self,scenarios):
        super().run(scenarios)
        return scenarios_maturity_T.format_output(self.results)

### Class to run scenarios over the risk free rate
class scenarios_risk_free(scenarios_MC):
    def format_output(results):
        xs,fxs,f_xs,errs = np.zeros(len(results)),np.zeros(len(results)),np.zeros(len(results)),np.zeros(len(results))
        for index,r in zip(range(len(results)),results):
                xs[index] = r['risk_free_rate']
                fxs[index]   = r['Thprice']
                f_xs[index]   = r['MCprice']
                errs[index]   = get_relative_mean_squared_error(r['MCprice'],r['Thprice'])
        return xs,fxs,f_xs,errs
    def run_and_format(self,scenarios):
        super().run(scenarios)
        return scenarios_risk_free.format_output(self.results)

class scenarios_vol(scenarios_MC):
    def format_output(results):
        xs,fxs,f_xs,errs = np.zeros(len(results)),np.zeros(len(results)),np.zeros(len(results)),np.zeros(len(results))
        for index,r in zip(range(len(results)),results):
                xs[index] = r['volatility']
                fxs[index]   = r['Thprice']
                f_xs[index]   = r['MCprice']
                errs[index]   = get_relative_mean_squared_error(r['MCprice'],r['Thprice'])
        return xs,fxs,f_xs,errs
    def run_and_format(self,scenarios):
        super().run(scenarios)
        return scenarios_vol.format_output(self.results)

#################################################################################################################
################################################ BSM scenarios ##################################################
#################################################################################################################

def N_codpy_bsm_scenario(**kwargs):
    params=deepcopy(kwargs)
    debug = kwargs.get("debug",False)
    params['path_generator']['process']=BSM()
    params['funs']['N']=option_param_getter.get_N
    scenariosvol, values = ['MonteCarloPricer','N'],[2**i for i in range(7,17)]

    
    params['funs']['generator']=Recurrent_historical_path_generator
    list_scenarios=generate_scenario().generate(scenariosvol,values,params)
    xs_hist,fxs,f_xs_hist,errs_hist = scenarios_N().run_and_format(list_scenarios, debug=debug)

    compare_plot_lists([xs_hist,xs_hist], [f_xs_hist,fxs], labelx = 'Number of paths', labely = "Price", title = "Vanilla option Convergence", listlabels = ["MC", "Codpy","analytic"],**{"figsize":(9,4)})


def N_bsm_scenario(**kwargs):
    params=deepcopy(kwargs)
    debug = kwargs.get("debug",False)
    params['path_generator']['process']=BSM()
    params['funs']['N']=option_param_getter.get_N
    scenariosvol, values = ['MonteCarloPricer','N'],[2**i for i in range(7,17)]

    params['funs']['generator']=QL_path_generator
    list_scenarios=generate_scenario().generate(scenariosvol,values,params)
    xs,fxs,f_xs,errs = scenarios_N().run_and_format(list_scenarios, debug = debug)
    
    params['funs']['generator']=Recurrent_historical_path_generator
    list_scenarios=generate_scenario().generate(scenariosvol,values,params)
    xs_hist,fxs,f_xs_hist,errs_hist = scenarios_N().run_and_format(list_scenarios, debug=debug)

    compare_plot_lists([xs,xs_hist,xs], [f_xs, f_xs_hist,fxs], labelx = 'Number of paths', labely = "Price", title = "Vanilla option Convergence", listlabels = ["MC", "Codpy","analytic"],**{"figsize":(9,4)})

def h_bsm_scenario(**kwargs):
    params=deepcopy(kwargs)
    params['path_generator']['process']=BSM()
    debug = kwargs.get("debug",False)
    params['funs']['generator']=Recurrent_historical_path_generator
    scenariosN, values_h = ['h'],[i for i in range(2,10)]
    list_scenarios=generate_scenario().generate(scenariosN,values_h,params)
    xs,fxs,f_xs,errs = scenarios_Nh().run_and_format(list_scenarios, debug=debug)

    # scenariosN, values = ['funs','generator'],np.repeat(QL_path_generator,len(values_h))
    # list_scenarios=generate_scenario().generate(scenariosN,values,params)
    # xs_hist,fxs,f_xs_hist,errs_hist = scenarios_N().run_and_format(list_scenarios)

    compare_plot_lists([values_h,values_h],[fxs,f_xs], labelx = 'Number of observations', labely = "Price", title = "Vanilla option Convergence", listlabels = ["analytic","MC", "Codpy"],**{"figsize":(9,4)})
    pass

def Nh_bsm_scenario(**kwargs):
    params=deepcopy(kwargs)
    params['path_generator']['process']=BSM()

    params['funs']['generator']=historical_path_generator
    scenariosN, values = ['QL_historical_generator','N'],[i for i in range(1,7)]
    list_scenarios=generate_scenario().generate(scenariosN,values,params)
    xs,fxs,f_xs,errs = scenarios_Nh().run_and_format(list_scenarios)

    scenariosN, values = ['funs','generator'],np.repeat(QL_path_generator,len(values))
    list_scenarios=generate_scenario().generate(scenariosN,values,params)
    xs_hist,fxs,f_xs_hist,errs_hist = scenarios_N().run_and_format(list_scenarios)

    compare_plot_lists([xs, xs,xs],[fxs, f_xs_hist,f_xs], labelx = 'Number of observations', labely = "Price", title = "Vanilla option Convergence", listlabels = ["analytic","MC", "Codpy"],**{"figsize":(9,4)})
    pass

def T_bsm_scenario(**kwargs):
    params=deepcopy(kwargs)
    params['path_generator']['process']=BSM()

    params['funs']['generator']=Recurrent_historical_path_generator
    scenariosN, values = ['QL_historical_generator','T'],[100*i for i in range(20,70)]
    list_scenarios=generate_scenario().generate(scenariosN,values,params)
    xs,fxs,f_xs,errs = scenarios_Nh().run_and_format(list_scenarios)

    scenariosN, values = ['funs','generator'],np.repeat(QL_path_generator,len(values))
    list_scenarios=generate_scenario().generate(scenariosN,values,params)
    xs_hist,fxs,f_xs_hist,errs_hist = scenarios_N().run_and_format(list_scenarios)

    compare_plot_lists([xs, xs,xs],[fxs, f_xs_hist,f_xs], labelx = 'Number of obeseravations', labely = "Price", title = "Vanilla option Convergence", listlabels = ["analytic","MC", "Codpy"],**{"figsize":(9,4)})
    pass

def maturity_bsm_scenario(**kwargs):
    params=deepcopy(kwargs)
    today_date= kwargs['getter'].get_today_date(**kwargs)
    scenariosMaturity, values = ['option','maturity_date'],[today_date + datetime.timedelta(days=i)  for i in range(10,200,10)]
    list_scenarios=generate_scenario().generate(scenariosMaturity,values,[params])
    xs,fxs,f_xs,errs = scenarios_maturity().run_and_format(list_scenarios)

    params['funs']['generator']=QL_path_generator
    list_scenarios=generate_scenario().generate(scenariosMaturity,values,[params])
    xs_hist,fxs,f_xs_hist,errs_hist = scenarios_maturity().run_and_format(list_scenarios)
    x = [get_float(i) for i in values]
    compare_plot_lists([x, x,x],[fxs, f_xs_hist,f_xs], labelx = 'Maturity', labely = "Price", title = "Vanilla option Convergence", listlabels = ["analytic","MC", "Codpy"],**{"figsize":(9,4)})
    pass

def maturity_T_bsm_scenario(**kwargs):
    params=deepcopy(kwargs)
    today_date= kwargs['getter'].get_today_date(**kwargs)
    scenariosMaturity, values = ['option','maturity_date'],[today_date + datetime.timedelta(days=i)  for i in range(1,100,10)]
    list_scenarios=generate_scenario().generate(scenariosMaturity,values,[params])
    scenariosT, valuesT = ['QL_historical_generator','T'],[100*i for i in range(1,11)]
    list_scenarios=generate_scenario().generate(scenariosT,valuesT,list_scenarios)
    xs,fxs,f_xs,errs = scenarios_maturity_T().run_and_format(list_scenarios)

    multi_plot([(xs,fxs),(xs,f_xs),(xs,errs)],plot_trisurf,projection='3d',elev = 25,azim=-80,linewidth = 0.2,antialiased = True,figsize=(9,9))
    pass

def risk_free_bsm_scenario(**kwargs):
    params=deepcopy(kwargs)
    params['path_generator']['process']=BSM()
    params['funs']['generator']=historical_path_generator
    scenariosRisk, values = ['BSM','risk_free_rate'],[ 0.01*i for i in range(0,21)]
    list_scenarios=generate_scenario().generate(scenariosRisk,values,[params])
    xs,fxs,f_xs,errs = scenarios_risk_free().run_and_format(list_scenarios)

    params['funs']['generator']=QL_path_generator
    list_scenarios=generate_scenario().generate(scenariosRisk,values,[params])
    xs_hist,fxs,f_xs_hist,errs_hist = scenarios_risk_free().run_and_format(list_scenarios)
    x = [get_float(i) for i in values]
    compare_plot_lists([x, x,x],[fxs, f_xs_hist,f_xs], labelx = 'Risk free rate', labely = "Price", title = "Vanilla option Convergence", listlabels = ["analytic","MC", "Codpy"],**{"figsize":(9,4)})
    pass

def vol_bsm_scenario(**kwargs):
    params=deepcopy(kwargs)
    params['path_generator']['process']=BSM()
    params['funs']['generator']=historical_path_generator
    scenariosRisk, values = ['BSM','volatility'],[ 0.01*i for i in range(0,21)]
    list_scenarios=generate_scenario().generate(scenariosRisk,values,[params])
    xs,fxs,f_xs,errs = scenarios_vol().run_and_format(list_scenarios)

    params['funs']['generator']=QL_path_generator
    list_scenarios=generate_scenario().generate(scenariosRisk,values,[params])
    xs_hist,fxs,f_xs_hist,errs_hist = scenarios_vol().run_and_format(list_scenarios)
    x = [get_float(i) for i in values]
    compare_plot_lists([x, x,x],[fxs, f_xs_hist,f_xs], labelx = 'Risk free rate', labely = "Price", title = "Vanilla option Convergence", listlabels = ["analytic","MC", "Codpy"],**{"figsize":(9,4)})
    pass

#################################################################################################################
############################################### Heston scenarios ################################################
#################################################################################################################

def N_heston_scenario(**kwargs):
    params=deepcopy(kwargs)
    params['list_maps']=[Id,log_ret,normal_return]
    # params['inv_list_maps']=[inv_log_ret,inv_normal_return]
    params['path_generator']['process']=Heston()
    params['QL_historical_generator']['process']=Heston()
    params['funs']['payoff']=HestonOption
    params['funs']['Thprice']=HestonClosedFormula().price
    params['funs']['N']=Heston_param_getter.get_N

    scenariosN, values = ['MonteCarloPricer','N'],[2**i for i in range(7,15)]

    params['funs']['generator']=QL_path_generator
    list_scenarios=generate_scenario().generate(scenariosN,values,params)
    xs,fxs,f_xs,errs = scenarios_N().run_and_format(list_scenarios,**kwargs)
    
    params['funs']['generator']=historical_path_generator
    list_scenarios=generate_scenario().generate(scenariosN,values,params)
    xs_hist,fxs,f_xs_hist,errs_hist = scenarios_N().run_and_format(list_scenarios,**kwargs)

    compare_plot_lists([xs,xs_hist,xs], [f_xs, f_xs_hist,fxs], labelx = 'Number of paths', labely = "Price", title = "Vanilla option Convergence", listlabels = ["MC", "Codpy","analytic"],**{"figsize":(9,4)})


def Nh_heston_scenario(**kwargs):
    params=deepcopy(kwargs)
    params['list_maps']=[log_ret,normal_return]
    params['inv_list_maps']=[inv_log_ret,inv_normal_return]
    params['path_generator']['process']=Heston()
    params['QL_historical_generator']['process']=Heston()
    params['funs']['payoff']=HestonOption
    params['funs']['Thprice']=HestonClosedFormula().price

    params['funs']['generator']=historical_path_generator
    scenariosN, values = ['QL_historical_generator','N'],[i for i in range(1,8)]
    list_scenarios=generate_scenario().generate(scenariosN,values,[params])
    xs,fxs,f_xs,errs = scenarios_Nh().run_and_format(list_scenarios)

    scenariosN, values = ['funs','generator'],np.repeat(QL_path_generator,len(values))
    list_scenarios=generate_scenario().generate(scenariosN,values,[params])
    xs_hist,fxs,f_xs_hist,errs_hist = scenarios_N().run_and_format(list_scenarios)
    compare_plot_lists([xs, xs,xs],[fxs, f_xs_hist,f_xs], labelx = 'Number of observation', labely = "Price", title = "Vanilla option Convergence", listlabels = ["analytic","MC", "Codpy"],**{"figsize":(9,4)})
    pass

def T_heston_scenario(**kwargs):

    params=deepcopy(kwargs)
    params['list_maps']=[log_ret,normal_return]
    params['inv_list_maps']=[inv_log_ret,inv_normal_return]
    params['path_generator']['process']=Heston()
    params['QL_historical_generator']['process']=Heston()
    params['funs']['payoff']=HestonOption
    params['funs']['Thprice']=HestonClosedFormula().price
    
    params['funs']['generator']=historical_path_generator
    scenariosN, values = ['QL_historical_generator','T'],[100*i for i in range(1,10)]
    list_scenarios=generate_scenario().generate(scenariosN,values,[params])
    xs,fxs,f_xs,errs = scenarios_Nh().run_and_format(list_scenarios)

    scenariosN, values = ['funs','generator'],np.repeat(QL_path_generator,len(values))
    list_scenarios=generate_scenario().generate(scenariosN,values,[params])
    xs_hist,fxs,f_xs_hist,errs_hist = scenarios_N().run_and_format(list_scenarios)
    compare_plot_lists([xs, xs,xs],[fxs, f_xs_hist,f_xs], labelx = 'Number of observations', labely = "Price", title = "Vanilla option Convergence", listlabels = ["analytic","MC", "Codpy"],**{"figsize":(9,4)})
    pass

def maturity_heston_scenario(**kwargs):

    params=deepcopy(kwargs)
    params['list_maps']=[log_ret,normal_return]
    params['inv_list_maps']=[inv_log_ret,inv_normal_return]
    params['path_generator']['process']=Heston()
    params['QL_historical_generator']['process']=Heston()
    params['funs']['payoff']=HestonOption
    params['funs']['maturity_date']=Heston_param_getter().get_maturity_date
    params['funs']['Thprice']=HestonClosedFormula().price
    today_date= kwargs['getter'].get_today_date(**kwargs)
    scenariosMaturity, values = ['HestonOption','maturity_date'],[today_date + datetime.timedelta(days=i)  for i in range(1,200,10)]

    params['funs']['generator']=historical_path_generator
    list_scenarios=generate_scenario().generate(scenariosMaturity,values,[params])
    xs,fxs,f_xs,errs = scenarios_maturity().run_and_format(list_scenarios)

    params['funs']['generator']=QL_path_generator
    list_scenarios=generate_scenario().generate(scenariosMaturity,values,[params])
    xs_hist,fxs,f_xs_hist,errs_hist = scenarios_maturity().run_and_format(list_scenarios)
    compare_plot_lists([xs, xs,xs],[fxs, f_xs_hist,f_xs], labelx = 'Maturity', labely = "Price", title = "Vanilla option Convergence", listlabels = ["analytic","MC", "Codpy"],**{"figsize":(9,4)})
    pass


def maturity_T_heston_scenario(**kwargs):
    params=deepcopy(kwargs)
    params['list_maps']=[log_ret,normal_return]
    params['inv_list_maps']=[inv_log_ret,inv_normal_return]
    params['path_generator']['process']=Heston()
    params['QL_historical_generator']['process']=Heston()
    params['funs']['payoff']=HestonOption
    params['funs']['maturity_date']=Heston_param_getter().get_maturity_date
    params['funs']['Thprice']=HestonClosedFormula().price
    today_date= kwargs['getter'].get_today_date(**kwargs)
    scenariosMaturity, values = ['HestonOption','maturity_date'],[today_date + datetime.timedelta(days=i)  for i in range(1,200,10)]
    scenariosT, valuesT = ['QL_historical_generator','T'],[100*i for i in range(1,4)]

    params['funs']['generator']=historical_path_generator
    list_scenarios=generate_scenario().generate(scenariosMaturity,values,[params])
    list_scenarios=generate_scenario().generate(scenariosT,valuesT,list_scenarios)

    xs,fxs,f_xs,errs = scenarios_maturity_T().run_and_format(list_scenarios)

    multi_plot([(xs,fxs),(xs,f_xs),(xs,errs)],plot_trisurf,projection='3d',elev = 25,azim=-80,linewidth = 0.2,antialiased = True,figsize=(9,9))
    pass

def risk_free_heston_scenario(**kwargs):

    params=deepcopy(kwargs)
    params['list_maps']=[log_ret,normal_return]
    params['inv_list_maps']=[inv_log_ret,inv_normal_return]
    params['path_generator']['process']=Heston()
    params['QL_historical_generator']['process']=Heston()
    params['funs']['payoff']=HestonOption
    params['funs']['Thprice']=HestonClosedFormula().price
    params['funs']['risk_free_rate']=Heston_param_getter().get_risk_free_rate  

    params['funs']['generator']=historical_path_generator
    scenariosRisk, values = ['Heston','risk_free_rate'],[ 0.01*i for i in range(0,21)]
    list_scenarios=generate_scenario().generate(scenariosRisk,values,[params])
    xs,fxs,f_xs,errs = scenarios_risk_free().run_and_format(list_scenarios)

    params['funs']['generator']=QL_path_generator
    list_scenarios=generate_scenario().generate(scenariosRisk,values,[params])
    xs_hist,fxs,f_xs_hist,errs_hist = scenarios_risk_free().run_and_format(list_scenarios)
    compare_plot_lists([xs, xs,xs],[fxs, f_xs_hist,f_xs], labelx = 'Number of observations', labely = "Price", title = "Vanilla option Convergence", listlabels = ["analytic","MC", "Codpy"],**{"figsize":(9,4)})
    pass

#################################################################################################################
################################################ Stats functions ################################################
#################################################################################################################

def compare_plot_pdf(x,z,labels,title):
    import seaborn as sns
    pdf=pd.DataFrame({labels[1]:z,labels[0]:x})
    # sns.set_context("paper", rc={"font.size":8,"axes.titlesize":8,"axes.labelsize":5})   
    sns.displot(pdf,kde=True,height=3, aspect=1)
    plt.title(title,fontsize = 8)
    plt.show()


def test_statistics(x,z,alpha):
    ## Central tendencies
    stats = central_tendency_stats(x,z,["Quantlib","Codpy"])
    ## Kolmogrov-Smirnov test
    Kolmogorov_Smirnov=Kolmogorov_Smirnov_test(x.reshape(x.shape[0],1),z.reshape(z.shape[0],1),0.01)

    Distances=pd.DataFrame()
    Distances['Hellinger distance']=[hellinger(x,z)]
    Distances['Discrepancy distance']=[op.discrepancy(x.reshape(x.shape[0],1), z.reshape(z.shape[0],1), **get_params_MC())]
    
    return stats,Kolmogorov_Smirnov,Distances 

def plot_samples(N,timesteps,**kwargs):
    payoff = kwargs.get('funs').get('payoff')
    payoff = payoff(**kwargs)
    kwargs['MonteCarloPricer']['N']=N
    kwargs['historical_generator']=QL_historical_generator(**kwargs)
    today_date= kwargs['getter'].get_today_date(**kwargs)
    time_list=[i for i in range(int(today_date),int(today_date)+timesteps+1)]
    f_z = Recurrent_historical_path_generator().generate(N,payoff,time_list,**kwargs)
    x=pd.DataFrame(f_z[:,1,:].T)
    x.plot(legend=False,figsize=(9, 5))
    plt.show()

def test_mapping(map_list=None,**kwargs):
    N = option_param_getter.get_N(**kwargs)
    samples=QL_historical_generator(**kwargs).generate(**kwargs)
    if map_list==None:
        original=pd.DataFrame(samples[0,1:,:].T,index=samples[0,0,:],columns=['Historical observation'])
        original.plot(figsize=(8.5,3.5))
        plt.show()
    else:
        kwargs['list_maps']=map_list
        time_list = get_float(QL_historical_generator.get_times(**kwargs))
        mapping = kwargs.get("map",None)
        samples[:,1:,:] = mapping(samples[:,1:,:],**kwargs, times = time_list)
        mapped=pd.DataFrame(samples[0,1:,:].T,index=samples[0,0,:])
        mapped.plot(figsize=(9,4),legend=False)
        plt.axhline(y=0, color='b', linestyle='-',alpha=0.7)
        plt.show()

#################################################################################################################
################################################## BSM tests ####################################################
#################################################################################################################

def generate_bsm_samples(**kwargs):
    payoff = kwargs.get('funs').get('payoff')
    payoff = payoff(**kwargs)
    N = option_param_getter.get_N(**kwargs)
    kwargs['historical_generator']=QL_historical_generator(**kwargs)
    today_date= kwargs['getter'].get_today_date(**kwargs)
    timelist=[int(get_float(today_date)),int(0.5*get_float(today_date)+0.5*get_float(payoff.maturity_date)),int(get_float(payoff.maturity_date))]
    # timelist=[int(get_float(payoff.today_date)),int(get_float(payoff.maturity_date))]
    # timelist=[i for i in range(int(get_float(payoff.today_date)),int(get_float(payoff.maturity_date))+1,1)]

    futureSamples=QL_path_generator().generate(N=N,payoff=payoff,time_list=payoff.get_times(**kwargs),**kwargs)
    f_z = historical_path_generator().generate(N,payoff,time_list=timelist,**kwargs)
    x = futureSamples[:,0,-1]
    z = f_z[:,1,-1]
    return x,z, f_z[:,1,:]

def bsm_stats(**kwargs):
    alpha=kwargs.get('alpha',0.05)
    payoff = kwargs.get('funs').get('payoff')
    payoff = payoff(**kwargs)
    risk_free_rate = kwargs['BSM']['risk_free_rate']
    volatility = kwargs['BSM']['volatility']
    x,z,full_z=generate_bsm_samples(**kwargs)

    # timelist=[int(get_float(payoff.today_date)),int(get_float(payoff.maturity_date))]
    # log_full_z = log_ret(full_z,**kwargs, times = timelist)[:,1:]
    # means = np.mean(log_full_z,axis=0)

    ## Q-Q plots
    qq_plot(x,z,["Quantlib","Codpy"],"None")
    ## Histograme et pdf
    compare_plot_pdf(x.T,z.T,["Quantlib","Codpy"],"None")
    
    stats,Kolmogorov_Smirnov,Distances=test_statistics(x,z,alpha)
    return stats,Kolmogorov_Smirnov,Distances


#################################################################################################################
################################################ Heston tests ###################################################
#################################################################################################################

def generate_heston_samples(**kwargs):
    payoff = kwargs.get('funs').get('payoff')
    payoff = payoff(**kwargs)
    N = option_param_getter.get_N(**kwargs)
    kwargs['list_maps']=[Id,log_ret,normal_return]
    kwargs['inv_list_maps']=[Id,inv_log_ret,inv_normal_return]
    kwargs['path_generator']['process']=Heston()
    kwargs['QL_historical_generator']['process']=Heston()
    kwargs['historical_generator']=QL_historical_generator(**kwargs)

    # timelist=[int(get_float(payoff.today_date)),int(0.5*get_float(payoff.today_date)+0.5*get_float(payoff.maturity_date)),int(get_float(payoff.maturity_date))]
    timelist=[i for i in range(int(get_float(today_date)),int(get_float(payoff.maturity_date))+1,1)]
    
    futureSamples=QL_path_generator().generate(N=N,payoff=payoff,time_list=payoff.get_times(**kwargs),**kwargs)
    f_z = Recurrent_historical_path_generator().generate(N,payoff,time_list=timelist,**kwargs)
    x_price = futureSamples[:,0,-1]
    z_price = f_z[:,1,-1]
    x_vol= futureSamples[:,1,-1]
    z_vol= f_z[:,2,-1]
    return x_price,z_price,x_vol,z_vol

def heston_stats(**kwargs):
    alpha=kwargs.get('alpha',0.05)
    x_price,z_price,x_vol,z_vol=generate_heston_samples(**kwargs)
    ## Q-Q plots
    qq_plot(x_price,z_price,["Quantlib","Codpy"],'None')
    ## Histograme et pdf
    compare_plot_pdf(x_price.T,z_price.T,["Quantlib","Codpy"],'None')

    ## Q-Q plots
    qq_plot(x_vol,z_vol,["Quantlib","Codpy"],'None')
    ## Histograme et pdf
    compare_plot_pdf(x_vol.T,z_vol.T,["Quantlib","Codpy"],'None')

    return test_statistics(x_price,z_price,alpha),test_statistics(x_vol,z_vol,alpha)


#################################################################################################################
########################################### Multi assets tests ##################################################
#################################################################################################################


def generate_multiple_bsm_samples(**kwargs):
    payoff = kwargs.get('funs').get('payoff')
    payoff = payoff(**kwargs)
    N = option_param_getter.get_N(**kwargs)
    kwargs['historical_generator']=QL_historical_generator(**kwargs)
    timelist=kwargs.get('timelist')
    futureSamples=QL_path_generator().generate(N=N,payoff=payoff,time_list=payoff.get_times(**kwargs),**kwargs)
    f_z = historical_path_generator().generate(N,payoff,time_list=timelist,**kwargs)
    # x1 = futureSamples[:,0,-1]
    # x2 = futureSamples[:,1,-1]
    # z1 = f_z[:,1,-1]
    # z2 = f_z[:,2,-1]
    return futureSamples,f_z

def Multiple_bsm_correlation(**kwargs):
    N=100
    kwargs['funs']['payoff']=BasketOption
    kwargs['list_maps']=[log_ret,log_ret]
    kwargs['getter']=basket_option_param_getter()
    kwargs['path_generator']['process']=BSMultiple()
    kwargs['QL_historical_generator']['process']=BSMultiple()
    timelist= [i for i in range(int(get_float(datetime.date.today())),int(get_float(datetime.date.today()))+100,1)]
    kwargs['timelist']= timelist
    kwargs['MonteCarloPricer']['N']=N
    kwargs['historical_generator']=QL_historical_generator(**kwargs)
    historical_generator = kwargs.get("historical_generator",None)
    ## historical series correlation
    mapping = kwargs.get("map",None)
    samples = historical_generator.generate(**kwargs)
    samples =  mapping(samples[:,1:,:],**kwargs, times = samples[0,0,:])
    x_hist = samples[0,0,1:]
    y_hist = samples[0,1,1:]
    corr_hist, _ = pearsonr(x_hist, y_hist)

    ## transformed correlation
    transformed_corr=get_log_normal_corr(**kwargs)

    ## Generated series correlation
    futureSamples,f_z=generate_multiple_bsm_samples(**kwargs)
    f_z[:,1:,:] = mapping(f_z[:,1:,:],**kwargs, times = timelist)
    x = f_z[0,1,1:]
    y = f_z[0,2,1:]
    corr0, _ = pearsonr(x, y)
    
    c=[]
    for i in range(N):
        x = f_z[i,1,1:]
        y = f_z[i,2,1:]
        corr, _ = pearsonr(x, y)
        c.append(corr)
    m=np.mean(c)

    print('Transformed correlation : ',transformed_corr)
    print('Historical log returns statistical correlation : ',corr_hist)
    print('Correlation found on one generated series (2000 historical observations | 1000 timesteps into the future): ',corr0)
    print('Mean of correlation on 100 generated series : ',m)
    pass

def get_log_normal_corr(**kwargs):
    corr_matrix=np.array(kwargs['BSMultiple']['correlation_matrix'])
    vol_vector = np.diag(kwargs['BSMultiple']['volatility'])
    covariance_matrix=np.dot(np.dot(vol_vector,corr_matrix),vol_vector)
    a=covariance_matrix[0,0]
    b=covariance_matrix[0,1]
    c=covariance_matrix[1,1]
    correlation=(np.exp(b)-1)/np.sqrt((np.exp(a)-1)*(np.exp(c)-1))
    return correlation


def Multiple_bsm_stats(**kwargs):
    alpha=kwargs.get('alpha',0.05)
    kwargs['funs']['payoff']=BasketOption
    kwargs['list_maps']=[log_ret,log_ret]
    kwargs['getter']=basket_option_param_getter()
    kwargs['path_generator']['process']=BSMultiple()
    kwargs['QL_historical_generator']['process']=BSMultiple()

    x1,x2,z1,z2,futureSamples,f_z=generate_multiple_bsm_samples(**kwargs)

    ## Q-Q plots
    qq_plot(x1,z1,["Quantlib","Codpy"],"None")
    qq_plot(x2,z2,["Quantlib","Codpy"],"None")
    ## Histograme et pdf
    compare_plot_pdf(x1.T,z1.T,["Quantlib","Codpy"],"None")
    compare_plot_pdf(x2.T,z2.T,["Quantlib","Codpy"],"None")

    stats1,Kolmogorov_Smirnov1,Distances1=test_statistics(x1,z1,alpha)
    stats2,Kolmogorov_Smirnov2,Distances2=test_statistics(x2,z2,alpha)

    return stats1,Kolmogorov_Smirnov1,Distances1

        
#################################################################################################################
################################## Historical Data augementation tests ##########################################
#################################################################################################################

def real_test(**kwargs):
    payoff = kwargs.get('funs').get('payoff')
    payoff = payoff(**kwargs)
    N = option_param_getter.get_N(**kwargs)
    kwargs['historical_generator']=QL_historical_generator(**kwargs)
    last_date=int(get_float(datetime.date(2022,3,7)))
    prediction_date=int(get_float(datetime.date(2022,4,22)))
    middle=int(0.5*last_date+0.5*prediction_date)
    # timelist=[last_date,middle,prediction_date]
    timelist=[i for i in range(last_date,prediction_date+1,1)]
    kwargs['MonteCarloPricer']['N']=10000
    samples=Real_historical_generator().get_raw_data(**kwargs)
    initial_value=samples[0,1,-1]
    kwargs['BSM']['spot_price']=initial_value
    f_z = historical_path_generator().generate_from_samples(samples,sample_times=timelist,**kwargs)
    real_value=4271.78
    codpy_value=np.mean(f_z[:,1,:])
    error= real_value-codpy_value
    pass
    # timelist=[int(get_float(payoff.today_date)),int(0.5*get_float(payoff.today_date)+0.5*get_float(payoff.maturity_date)),int(get_float(payoff.maturity_date))]


def test_augementation(real=True,**kwargs):
    
    ## Getting the parameters ready
    payoff = kwargs.get('funs').get('payoff')
    payoff = payoff(**kwargs)
    N = 10
    kwargs['MonteCarloPricer']['N']=N
    kwargs['historical_generator']=QL_historical_generator(**kwargs)
    risk_free_rate = kwargs['BSM']['risk_free_rate']
    volatility = kwargs['BSM']['volatility']
    # kwargs['path_generator']['process']=Heston()
    # kwargs['QL_historical_generator']['process']=Heston()

    ## Getting the data (real historical data or synthetic data from Lognormal or Heston models)
    if real==False:
        historical_generator = kwargs.get("historical_generator",None)
        samples = historical_generator.generate(**kwargs)
    else:
        samples=Real_historical_generator().get_raw_data(**kwargs)

    ## Generating new data with out generator
    timelist=samples[0,0,:].tolist()
    initial_value=samples[0,1,0]
    kwargs['BSM']['spot_price']=initial_value
    f_z = historical_path_generator().generate_from_samples(samples,sample_times=timelist,**kwargs)

    ## Obtaining the asset prices (x : real prices | z : our generated prices)
    x = samples[0,1,:]
    z = f_z[0,1,:]
    
    ## Plotting the asset prices
    data_price=pd.DataFrame()
    data_price['Real']= x
    for i in range(N):
        data_price[str(i)]=f_z[i,1,:]
    data_price.plot()

    ## Calculating log returns of the prices 
    x_returns=log_ret(x.reshape((x.shape[0],1)).T,**kwargs, times = timelist)[0,1:]
    z_returns=log_ret(z.reshape((z.shape[0],1)).T,**kwargs, times = timelist)[0,1:]

    ## Calculating log returns statistics
    expected_mean = (risk_free_rate - (volatility**2)/2) *(1/365)
    stats,Kolmogorov_Smirnov,Distances = test_statistics(x_returns,z_returns,0.01)

    ## Plotting Auto Correlation function 
    sm.graphics.tsa.plot_acf(x_returns, lags=40)
    sm.graphics.tsa.plot_acf(z_returns, lags=40)
    plt.show()

    ## Plotting Log returns
    data_returns=pd.DataFrame()
    data_returns['Real']=x_returns
    data_returns['Generated']=z_returns
    data_returns['Real'].plot()
    data_returns['Generated'].plot()

    ## Plotting log returns PDF
    compare_plot_pdf(x_returns.T,z_returns.T,["Real","Codpy"],"PDF")

    return x,z

def get_params_MC():
    params = {
    'h':1,
    'p':1,
    'debug':True,
    # 'getter':option_param_getter(),
    # 'getter':Heston_param_getter(),
    'getter':yf_param_getter(),
    'today_date': datetime.date(2022,5,11),
    # 'today_date': datetime.date.today(),
    'set_codpy_kernel' : kernel_setters.kernel_helper(kernel_setters.set_tensornorm_kernel, 3,0 ,map_setters.set_unitcube_map),
    # 'set_codpy_kernel' : kernel_setters.kernel_helper(kernel_setters.set_tensornorm_kernel, 2,1e-8 ,map_setters.set_mean_distance_map),
    # 'set_codpy_kernel' : kernel_setters.kernel_helper(kernel_setters.set_gaussian_kernel, 2,0 ,map_setters.set_mean_distance_map),
    # 'set_codpy_kernel' : kernel_setters.kernel_helper(kernel_setters.set_matern_tensor_kernel, 0,1e-8 ,map_setters.set_unitcube_map),
    # 'set_codpy_kernel' : kernel_setters.kernel_helper(kernel_setters.set_linear_regressor_kernel, 2,1e-8 ,None),
    'alpha' : 0.05,
    'rescale' : True,
    'map':cartesian_map,
    'seed':None,
    # 'list_maps':[normal_return],
    # 'inv_list_maps':[inv_normal_return],
    'list_maps':[log_ret,log_ret,log_ret],
    # 'inv_list_maps':[inv_log_ret],
    'historical_generator':QL_historical_generator,
    'generator':historical_path_generator,
    'funs':{
        'payoff':option,
        'historical_generator':QL_historical_generator,
        'generator':historical_path_generator,
        'MCprice': MonteCarloPricer().price,
        'Thprice': OptionClosedFormula().price, 
        'volatility': option_param_getter().get_volatility,
        'spot': option_param_getter().get_spot,
        'N': option_param_getter.get_N,
        'T': QL_historical_generator.get_T,
        'Nh': QL_historical_generator.get_N,
        'D': option_param_getter.get_D,
        'maturity_date': option_param_getter().get_maturity_date,
        'risk_free_rate': option_param_getter().get_risk_free_rate
        },
    'QL_historical_generator' : {
        'N':1,
        'T':300,
        'process':BSM(),
        'seed':None
    },
    'MonteCarloPricer' :{ 'N':10000},
    'path_generator':{
                        'process' : BSM(),
                        'antithetic': False
                     },
    'BSM':{
        'spot_price' : 100,
        'risk_free_rate' : 0,
        'dividend_rate' : 0,
        'volatility' : 0.05,
          },
    'BSMultiple':{
                'spot_price' : [100., 120.],
                'risk_free_rate' : 0,
                'dividend_rate' : 0,
                'spot_price' : [100., 110.],
                'volatility' : [0.1, 0.2],
                'correlation_matrix' : [[1, 0.5 ], 
                                        [0.5, 1, ]],
                'BSMs':[ 
                        {'BSM':{
                        'spot_price' : 100,
                        'risk_free_rate' : 0,
                        'dividend_rate' : 0,
                        'volatility' : 0.1,
                        }},
                        
                        {'BSM':{
                        'spot_price' : 120,
                        'risk_free_rate' : 0,
                        'dividend_rate' : 0,
                        'volatility' : 0.2,
                        }}],
                },
    'BasketOption' :{
                    'option_type' : ql.Option.Call,
                    'today_date': datetime.date.today(),
                    'maturity_date' : datetime.date(2023,5,11),
                    'strike_price' : 105,
                    'risk_free_rate' : 0,
                    'dividend_rate' : 0,
                    'number_of_assets':2,
                    'weights':[0.5,0.5],
                    },
    'option' : {
                'option_type' : ql.Option.Call,
                'maturity_date' : datetime.date(2023,5,11),
                'strike_price' : 100,
                },
    'HestonOption' : {
        'option_type' : ql.Option.Call,
        'maturity_date' : datetime.date(2023,5,11),
        'strike_price' : 100,
        # 'timesteps':100
        },  
    'Heston':{
                'spot_price' : 100,
                'risk_free_rate' : 0,
                'dividend_rate' : 0,        
                'v0':0.1,
                'kappa':2,
                'theta':0.0225,
                'rho':-0.5,
                'sigma':0.25
            },
    'time_serie_generator' : {
            'yf_param' : {
                'symbols':["^GSPC"],
                'begin_date':'07/03/2018',
                'end_date':'07/03/2022',
                'yf_begin_date': '2018-03-07',
                'yahoo_columns': ['Close'],
                'date_format' : '%d/%m/%Y',
                'yahoo_date_format':'%Y-m%-d%',            
                'csv_date_format':'%d/%m/%Y'            
            },
            'PnL_csv' : os.path.join(data_path,"PnL","PnL"+".csv"),
            'xfx_csv' : os.path.join(data_path,"PnL","xfx"+".csv")
            },
    }    
    return {**params,**get_codpy_param()}                      

def get_yf_AAG_params():
    symbols = ['AAPL','GOOGL','AMZN']
    begin_date = '2016-01-02'
    end_date = '2022-01-01'
    yf_param= {
            'yf_param' : {
                'symbols':symbols,
                'begin_date':begin_date,
                'end_date':end_date,
                'yf_begin_date': begin_date,
                'yahoo_columns': ['Close'],
                'date_format' : '%Y-%m-%d',
                'yahoo_date_format':'%Y-%m-%d',            
                'csv_date_format':'%Y-%m-%d',            
                'csv_file' : os.path.join(data_path,'-'.join(symbols)+'-'+begin_date.replace('/','-')+"-"+end_date.replace('/','-')+".csv"),
            },
        }
    return {**get_params_MC(),**yf_param}
        

def RegenerateHistory(**kwargs):
    #params = kwargs.get("time_serie_generator")
    data = kwargs.get("data",ts_data.get_yf_ts_data(**kwargs['yf_param']))
    data.dropna(inplace=True)
    date_format = kwargs.get("date_format",'%d/%m/%Y')
    timelist = kwargs.get("timelist",[ get_float(x,date_format = date_format) for x in data.index ])


    samples=np.zeros((1,data.shape[1]+1,data.shape[0]))
    samples[0,1:,:]= data.values.T
    samples[0,0,:] = timelist
    initial_values = samples[0,1:,0]
    time_start= timelist[0]
    kwargs['Nz'] = kwargs.get('Nz',10)

    f_z = historical_path_generator().generate_from_samples(samples = samples,sample_times=timelist,initial_values = initial_values,time_start=time_start,**kwargs)

    return f_z,data,samples

def plot_trajectories(fz,fx,data,**kwargs):
    symbol = kwargs['symbols'][0]
    paths=pd.DataFrame(fz[:,1,:].T)
    paths.set_index(data.index,inplace=True)
    paths.plot(colormap='tab20b')
    name = 'Real '+ symbol
    paths[name] = fx[:,1,:].T
    # paths.plot(colormap='tab20b',y=[i for i in range(fz.shape[0]+1)])
    paths[name].plot(color='red',legend='Real '+ symbol,linewidth=3, rot=45)


def RegenerateDistribution(**kwargs):
    data = ts_data.get_yf_ts_data(**kwargs['yf_param'])
    data.dropna(inplace=True)
    sep,csv_file,begin_date,end_date,date_format,csv_date_format,time_col,select_columns=ts_data.get_param(**kwargs['yf_param'])
    timelist = [ get_float(x,date_format = csv_date_format) for x in data.index ]
    samples=np.zeros((1,data.shape[1]+1,data.shape[0]))
    samples[0,1:,:]= data.values.T
    samples[0,0,:] = timelist
    initial_values = samples[0,1:,0]
    time_start= timelist[0]
    diffusion_part,linear_part,f_x = historical_path_generator.generate_distribution_from_samples_np(samples[:,:,:],sample_times=timelist,initial_values = initial_values,time_start=time_start,**kwargs)
    f_z = diffusion_part+linear_part
    return f_z,data,f_x


if __name__ == "__main__":

    f_z,data,f_x=RegenerateHistory(**get_yf_AAG_params(),N=10)
    plot_trajectories(f_z,f_x,data)

    f_z,data,f_x=RegenerateDistribution(**get_yf_AAG_params())
    scatter_hist(f_x[:,0], f_x[:,2])
    scatter_hist(f_z[:,0], f_z[:,2])

    pass
