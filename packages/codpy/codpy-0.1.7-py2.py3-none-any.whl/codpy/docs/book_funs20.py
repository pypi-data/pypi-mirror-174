from preamble import *

def get_wilmott_param():
    return  {'rescale_kernel':{'max': 1000, 'seed':42},
    'sharp_discrepancy':{'max': 1000, 'seed':42},
    'discrepancy':{'max': 1000, 'seed':42},
    'validator_compute': ['accuracy_score','discrepancy_error','norm'],
    'set_codpy_kernel' : kernel_setters.kernel_helper(kernel_setters.set_tensornorm_kernel, 2,0 ,map_setters.set_unitcube_map),
    # 'set_codpy_kernel' : kernel_setters.kernel_helper(kernel_setters.set_gaussian_kernel, 0 ,0 ,map_setters.set_standard_min_map),
    # 'set_codpy_kernel' : kernel_setters.kernel_helper(kernel_setters.set_matern_tensor_kernel, 0,0 ,map_setters.set_standard_mean_map),
    'rescale': True,
    }
def get_bgm_means(**kwargs):
    getter = kwargs.get('getter')
    mat = get_float(getter.get_maturity_date(**kwargs))-get_float(getter.get_today_date(**kwargs))
    vols = getter.get_volatility(**kwargs)
    spots = getter.get_spot(**kwargs)
    out = [s*np.exp(-v*v*.5*mat/365) for v,s in zip(vols,spots)]
    return spots

def get_bgm_params(**kwargs):
    # params = {'list_maps':[log_ret],
    params = {'list_maps':[log_ret,log_ret],
    'path_generator':{'process': BSMultiple()},
    'getter':basket_option_param_getter(),
    'funs': {
        'payoff': BasketOption,
        'means' : get_bgm_means,
        'historical_generator': QL_historical_generator,
        'generator': historical_path_generator,
        'MCprice': MonteCarloPricer().price,
        'T': QL_historical_generator.get_T
        },
    'QL_historical_generator': {
        'T': 500,
        },
    }
    return {**kwargs,**params}

def get_params_MC(**kwargs):
    params = {
    'h':4,
    'p':0,
    'debug':True,
    'today_date': datetime.date(2022,6,1),
    'set_codpy_kernel' : kernel_setters.kernel_helper(kernel_setters.set_tensornorm_kernel, 2,0 ,map_setters.set_unitcube_map),
    'alpha' : 0.05,
    'rescale' : True,
    'map':cartesian_map,
    'seed':None,
    'N':10000,
    # 'list_maps':[normal_return],
    # 'inv_list_maps':[inv_normal_return],
    'list_maps':[log_ret],
    'inv_list_maps':[inv_log_ret],
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
        'strike': option_param_getter().get_strike,
        'N': option_param_getter.get_N,
        'T': QL_historical_generator.get_T,
        'Nh': QL_historical_generator.get_N,
        'D': option_param_getter.get_D,
        'maturity_date': option_param_getter().get_maturity_date,
        'risk_free_rate': option_param_getter().get_risk_free_rate
        },
    'QL_historical_generator' : {
        'N':1,
        'T':3047,
        'process':BSM(),
        'seed':111
    },
    'MonteCarloPricer' :{ 'N':10000},
    'path_generator':{
                        'process' : BSM(),
                        'antithetic': False
                     },
    'BasketOption' :{
                    'option_type' : ql.Option.Call,
                    'today_date': datetime.date(2022,6,1),
                    'maturity_date' : datetime.date(2023,6,1),
                    'strike_price' : 110, #108.2,  #108,
                    'risk_free_rate' : 0,
                    'dividend_rate' : 0,
                    'weights':[0.5,0.5],
                    # 'weights':[1],
                    },
    'option' : {
                'option_type' : ql.Option.Call,
                'today_date': datetime.date.today(),
                'maturity_date' : datetime.date(2022, 8, 2),
                'strike_price' : 102,
                },
    'HestonOption' : {
        'option_type' : ql.Option.Call,
        'today_date': datetime.date.today(),
        'maturity_date' : datetime.date(2022,7,30),
        'strike_price' : 100,
        'timesteps':100
        },  
    'Heston':{
                'spot_price' : 100,
                'risk_free_rate' : 0,
                'dividend_rate' : 0,        
                'v0':0.2,
                'kappa':0.8,
                'theta':0.008,
                'rho':0.2,
                'sigma':0.1
            },
    'time_serie_generator' : {
            'yf_param' : {
                'symbols':["^GSPC","^VIX"],
                'begin_date':'01/01/2020',
                'end_date':'19/05/2022',
                'yf_begin_date': '2020-01-01',
                'yahoo_columns': ['Close'],
                'date_format' : '%d/%m/%Y',
                'yahoo_date_format':'%Y-m%-d%',            
                'csv_date_format':'%d/%m/%Y'            
            },
            # 'PnL_csv' : os.path.join(data_path,"PnL","PnL"+".csv"),
            # 'xfx_csv' : os.path.join(data_path,"PnL","xfx"+".csv")
            },
    }    
    return {**kwargs,**params} 

def get_params_BSMultiple(**kwargs):
    BSMultiple={'BSMultiple':{
                'spot_price' : [100., 120.],
                # 'spot_price' : [100.],
                'risk_free_rate' : 0,
                'dividend_rate' : 0,
                'volatility' : [0.1, 0.2],
                'correlation_matrix' : [[1, 0.5 ], 
                                         [0.5, 1, ]],
                # 'correlation_matrix' : [[1]],
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
                        }
                        }
                        ],
                }}
    return {**kwargs,**BSMultiple}

class BasketOptionQuantlibMC(BasketOption):
    def getter(self): return basket_option_param_getter()
    def price(self,**kwargs):
        process = BSMultiple().get_process(**kwargs)
        rng = "pseudorandom"
        numSteps = 1000000
        stepsPerYear = 1
        seed = 43
        engine = ql.MCEuropeanBasketEngine(process, rng, timeStepsPerYear=stepsPerYear, requiredSamples=numSteps, seed=seed)
        getter = self.getter()
        ql.Settings.instance().evaluationDate = date_to_quantlib(getter.get_today_date(**kwargs))
        strike = getter.get_strike(**kwargs)
        option_type = getter.get_option_type(**kwargs)
        exercise = getter.get_exercise(**kwargs)
        vanillaPayoff = ql.PlainVanillaPayoff(option_type, strike)
        payoffAverage = ql.AverageBasketPayoff(vanillaPayoff, getter.get_D(**kwargs))
        basketOptionAverage = ql.BasketOption(payoffAverage, exercise)
        basketOptionAverage.setPricingEngine(engine)
        price=basketOptionAverage.NPV()
        return price

class scenarios_T_multiple(scenarios_MC):
    def format_output(results):
        xs,f_xs = np.zeros(len(results)),np.zeros(len(results))
        for index,r in zip(range(len(results)),results):
                xs[index] = r['T']
                f_xs[index]   = r['MCprice']
        return xs,f_xs
    def run_and_format(self,scenarios,**kwargs):
        super().run(scenarios,**kwargs)
        return scenarios_T_multiple.format_output(self.results)


def T_bsm_multiple_scenario(Nsc = 10,**kwargs):
    import openturns as opt

    params=get_bgm_params(**kwargs)
    N = MonteCarloPricer.get_params(**kwargs)['N']
    scenariosN, values = ['QL_historical_generator','T'],[100*i for i in range(1,Nsc)]
    vols = params['getter'].get_volatility(**kwargs)
    spots = params['getter'].get_spot(**kwargs)
    list_scenarios=generate_scenario().generate(scenariosN,values,params)
    xs,f_xs_random = scenarios_T_multiple().run_and_format(list_scenarios)
    list_scenarios=generate_scenario().generate(scenariosN,values,{**params,**{'grid_projection':True, 'random_sequence': opt.SobolSequence}})
    xs,f_xs_low = scenarios_T_multiple().run_and_format(list_scenarios)

    fxs= BasketOptionQuantlibMC(**kwargs).price(**kwargs)
    # fxs=MonteCarloPricer().price(**params)
    vols = np.mean(vols)
    spots = np.mean(spots)
    fxs=[fxs for value in values]
    var = spots*np.sqrt(np.exp(2*vols*vols) - np.exp(vols*vols))
    priceUpperError = np.array([fxs[0]+var/np.sqrt(N) for value in values])
    priceLowerError = np.array([fxs[0]-var/np.sqrt(N) for value in values])
    ObservationUpperError = np.array([fxs[0]+var/np.sqrt(value) for value in values])
    ObservationLowerError = np.array([fxs[0]-var/np.sqrt(value) for value in values])

    plt.plot(xs,f_xs_random,linewidth=4.3,color='#ca5686',label=r'$CodPy \; Price \; with \; random \; prior \; sampling$')
    plt.plot(xs,f_xs_low,linewidth=4.3,color="#4aac88",label=r'$CodPy \; Price \; with \; sharp \; discrepancy \; prior \; sampling$') #377eb8
    plt.plot(xs,fxs,linewidth=3,color='#8a73c9',linestyle = '--',label=r'$Theoretical \; Price$')
    plt.plot(xs,ObservationUpperError,color='#ca7040',linestyle = 'dotted',linewidth=3.5,label=r'$Generated \; trajectories \; size \; statistical \; error$')
    plt.plot(xs,ObservationLowerError,color='#ca7040',linestyle = 'dotted',linewidth=3.5,)
    # plt.plot(xs,priceUpperError,linewidth=3,color='#e41a1c',linestyle = 'dashdot',label=r'$Training \; set \; size \; statistical \; error$')
    # plt.plot(xs,priceLowerError,linewidth=3,color='#e41a1c',linestyle = 'dashdot')
    plt.xlabel("Number of training observations",fontsize=10)
    plt.ylabel("Vanilla option price",fontsize=10)
    plt.ylim(ObservationLowerError[0],ObservationUpperError[0])
    plt.legend(loc='best',fontsize=10)
    plt.show()

    df = pd.DataFrame()
    df['CodpyLow'] =  f_xs_low
    df['CodpyRandom'] =  f_xs_random
    df['Theoretical'] =  fxs
    df['ObservationLower'] = ObservationLowerError
    df['ObservationUpper'] = ObservationUpperError
    df['PriceLower'] = priceLowerError
    df['PriceUppoer'] = priceUpperError
    # df.to_csv(os.path.dirname(__file__)+'\BasketOption.csv')
    pass

def training_set_generation(params_option,results):
    plot_train_test_set(results=results,**params_option)

def european_pnl(params_option,results):
    multiple_scenario_output_amine(results,**params_option)

def european_pnl_error(results):
    codpy_error_matrix = get_codpy_PnL_error_matrix(results,file_name = "codpy_binary_error_matrix.csv").sort_index(axis=0)
    taylor_error_matrix = get_taylor_PnL_error_matrix(results,file_name = "taylor_binary_error_matrix.csv").sort_index(axis=0)
    frames = [codpy_error_matrix, taylor_error_matrix]
    result = pd.concat(frames)
    result.insert(0, "Maturity", ['Codpy error','Taylor error'])
    return result
    

def european_greek(params_option):
    results = single_scenario(**params_option)

    single_scenario_exact_deltas_output_amine(results,**params_option)
    single_scenario_exact_gammas_output_amine(results,**params_option)

def Generated_Google():
    f_z,data,f_x=RegenerateHistory(**get_yf_AAG_params(),N=10)
    plot_trajectories(f_z,f_x,data)
    plt.show()

def distribution_generee():    
    f_z,data,f_x=RegenerateDistribution(**get_yf_AAG_params())
    scatter_hist(f_x[:,0], f_x[:,2], **get_yf_AAG_params())
    plt.show()
    scatter_hist(f_z[:,0], f_z[:,2], **get_yf_AAG_params())
    plt.show()
    return f_z,data,f_x

def multiple_stats_aggregate(x,z,**kwargs):
    numAssets = z.shape[1]
    f_names = kwargs.get('asset_names',['ASSET'+str(i) for i in range(numAssets)])

    #kwargs['list_maps']= [log_ret for i in range(numAssets)]
    hist_data = pd.DataFrame(x,columns=f_names)
    gen_data = pd.DataFrame(z,columns=f_names)
    if numAssets > 1:
        corr_h = hist_data.corr()
        corr_g = gen_data.corr()
        return table([x], [z], f_names=f_names, format= '{:.1e}'), corr_h, corr_g
    else:
         return table([x], [z], f_names=f_names, format = '{:.1e}')

def table2(fx, fz, **kwargs):
    stats_df, corr_h, corr_g = multiple_stats_aggregate(fx,fz,asset_names=['AAPL', 'AMZN','GOOGL'])
    # print(stats_df)
    # print(corr_h,'\n', corr_g)
    return stats_df, corr_h, corr_g

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
            y = alg.sampler(l,M,**kwargs)
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

def plot1():
    xy, f_x, f_z = data_for_static_dist(**get_wilmott_param(),M=501)
    figure1(xy, **get_wilmott_param())
    table1 = table(f_x, f_z, f_names= ["Gaussian", "t-distribution"])


def figure1(xy, **kwargs):
    f_names=["Gaussian distribution","t-distribution"]
    kwargs = {'labels': ['sampled', 'generated'], 'title': "Gaussian"}
    multi_plot(xy,fun_plot = hist_plot, f_names = f_names, mp_ncols = 2, **kwargs) 

def RGBM(**kwargs):
    historical_generator = kwargs.get("historical_generator",None)
    getter = kwargs.get("getter")
    samples = historical_generator(**kwargs).generate(**kwargs)
    time_list = kwargs.get("time_list",getter.get_instrument(**kwargs).get_times(**kwargs))
    initial_values = kwargs.get("time_list",getter.get_spot(**kwargs))
    time_start = kwargs.get("today_date",getter.get_today_date(**kwargs))

    diffusion_part,linear_part,fx = historical_path_generator.generate_distribution_from_samples_np(samples,sample_times=time_list,initial_values = initial_values,time_start=time_start,**kwargs)
    fz = diffusion_part+linear_part
    return  multiple_stats_aggregate(fx,fz)


if __name__=="__main__":

    # xy, f_x, f_z = data_for_static_dist(**get_wilmott_param(),M=501)
    # figure1(xy, **get_wilmott_param())
    # table1 = table(f_x, f_z, f_names= ["Gaussian", "t-distribution"])
    # print(table1)

    # xy, f_x, f_z = data_for_static_dist(**get_wilmott_param(),M=501, grid_projection=True)
    # figure1(xy, **get_wilmott_param())
    # table1 = table(f_x, f_z, f_names= ["Gaussian", "t-distribution"])
    # print(table1)

    # T_bsm_multiple_scenario(**get_params_BSMultiple(**get_params_MC(**get_wilmott_param())))
    # import re

    f_z,data,f_x=RegenerateHistory(**get_yf_AAG_params())
    # print(table2(f_x,f_z, **get_yf_AAG_params()))
    Generated_Google()
    # f_x,data,f_z = distribution_generee()
    # table2, corr_h, corr_g = table2(f_x,f_z, **get_yf_AAG_params())

    # params_option = option_param_var().get_param()
    # results = maturity_scenario_amine(**params_option)
    # training_set_generation(params_option,results)
    # european_pnl(params_option,results)
    # european_pnl_error(results)
    # european_greek(params_option)
    pass