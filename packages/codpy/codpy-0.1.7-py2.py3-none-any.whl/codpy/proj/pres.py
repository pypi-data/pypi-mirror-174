from preamble import *

def get_time(csv,**kwargs): 
    return np.asarray(get_float(csv.index))

def csv_to_np(csv,**kwargs):
    out = csv.copy()
    out.insert(loc=0, column='Date', value=get_time(out,**kwargs))
    out = out.values.T
    out = out.reshape(1,out.shape[0],out.shape[1])
    return out

def set_fun(x,**kwargs): 
    return kwargs['getter'].set_time_spot(x,**kwargs)


def get_cdnordea_param():
    return  {
        ##codpy specific
        'rescale_kernel':{'max': 2000, 'seed':42},
        'set_codpy_kernel' : kernel_setters.kernel_helper(kernel_setters.set_tensornorm_kernel, 0,1e-8,map_setters.set_unitcube_map),
        'rescale': True,
        'grid_projection': True,


        ## global variables
        'date_format' : '%d/%m/%Y',
        'begin_date':'01/06/2016',
        'end_date':'01/06/2022',
        'today_date':'01/06/2022',
        # 'symbols' : ['GOOGL'],
        # 'symbols' : ['AAPL','GOOGL'],
        'symbols' : ['AAPL','GOOGL','AMZN']
}

def generative_methods(kwargs = get_cdnordea_param()):
    params= {}
    kwargs['set_codpy_kernel'] = kernel_setters.kernel_helper(kernel_setters.set_tensornorm_kernel, 0,1e-8,map_setters.set_unitcube_map)
    def graphic(**kwargs):
        f_names=["Gaussian distribution","t-distribution"]
        multi_plot(kwargs['xy'],fun_plot = hist_plot, f_names = f_names, mp_ncols = 2,labels= ['sampled', 'generated']) 
    def data_for_static_dist(D = 1, **kwargs):
        import scipy
        N = kwargs.get('N', 1000)
        degf = kwargs.get('degf', 3)
        labels = kwargs.get('f_names')
        left = np.random.normal(5., 1., (int(N/2),D))
        right = np.random.normal(-5., 1., (int(N/2),D))
        left_ = scipy.stats.t.rvs(100, -5., 1.,  (int(N/2),D))
        right_ = scipy.stats.t.rvs(100, 5., 1., (int(N/2),D))
        gaussr = pd.DataFrame(np.concatenate((left,right)))
        studr = pd.DataFrame(np.concatenate((left_,right_)))
        xy, ys, ls = [], [], []
        for l in gaussr, studr:
            y = alg.sampler(l,**kwargs)[0]
            xy += [(l,y)]
            ys += [y]
            ls += [l]
        return xy, ls, ys
    xy, f_x, f_z = data_for_static_dist(M=501,**kwargs)
    table1 = stats_df(f_x, f_z, f_names= ["Gaussian", "t-distribution"])
    params['graphic']=graphic
    params['xy']=xy
    params['table']=table1
    return {**kwargs,**params}

def retrieve_market_data(kwargs = get_cdnordea_param()):
    symbols = kwargs['symbols']
    begin_date = kwargs['begin_date']
    end_date = kwargs['end_date']
    date_format = kwargs['date_format']
    params= {
            'yf_param' : {
                'symbols':symbols,
                'begin_date':begin_date,
                'end_date':end_date,
                'yf_begin_date': begin_date,
                'yahoo_columns': ['Close'],
                'date_format' : date_format,
                'yahoo_date_format': '%Y-%m-%d',            
                'csv_date_format': date_format,            
                'csv_file' : os.path.join(data_path,'-'.join(symbols)+'-'+begin_date.replace('/','-')+"-"+end_date.replace('/','-')+".csv"),
            },
        }
    params['data'] = ts_data.get_yf_ts_data(**params['yf_param'])
    params['table1'] = df_summary(params['data'])

    def graphic(**params):
        params['data'].plot(rot=45),plt.show()
    params['graphic']=graphic

    return {**params,**kwargs}

def basket_values(values,**kwargs):
    basket_values = basket_option_param_getter().get_instrument(**kwargs).basket_value(values = values,weights = kwargs['BasketOption']['weights'],**kwargs)
    return basket_values
def payoff(values,**kwargs):
    if isinstance(values,pd.DataFrame): values = csv_to_np(values,**kwargs).squeeze().T
    out = basket_option_param_getter().get_instrument(**kwargs).f(x = values[:,1:],**kwargs)
    return out
    
def get_instrument_param(kwargs = retrieve_market_data()):
    from dateutil.relativedelta import relativedelta
    from dateutil import parser
    dim = len(kwargs['symbols'])
    def basket_values(values,**kwargs):
        basket_values = basket_option_param_getter().get_instrument(**kwargs).basket_value(values = values,weights = kwargs['BasketOption']['weights'],**kwargs)
        return basket_values
    spot_ = kwargs['data'].values.T[:,-1]
    spot_ = np.mean(spot_)
    params = {
    'getter':basket_option_param_getter(),
    'BasketOption' : {
                'weights': np.repeat(1./dim,dim),
                'option_type' :     ql.Option.Call,
                'maturity_date' : get_date(kwargs['end_date']) + relativedelta(days=30),
                'strike_price' : spot_*1.05,
                },
    }
    out = {**params,**kwargs}

    out['basket_values'] = basket_values
    out['payoff'] = payoff

    def graphic(**out):
        payoff_values = out['payoff'](values =out['data'], **out)
        basket_values_ = out['basket_values'](values =out['data'], **out)
        strike = out['getter'].get_strike(**out)
        basket_values_ = (basket_values_/strike - 1.)*100 

        figure2 = pd.DataFrame(np.array([basket_values_,payoff_values]).T, columns=['basket values','payoff values'] )
        plot1D(figure2,labelx = 'basket values (%K)', labely= 'payoff values')
        plt.show()
    out['graphic'] = graphic
    return out

def get_pricer_param(kwargs = get_instrument_param()):
    import itertools
    spots = kwargs['data'].values[-1,:]
    params = {
    'BSMultiple':  {
                'BSMs': [ 
                    {
                    'BSM':{
                    'spot_price' : spots[n],
                    'risk_free_rate' : 0,
                    'dividend_rate' : 0, 
                    'volatility' : 0.25,
                    }}  for n in range(len(spots))                  
                    ],
                'correlation_matrix' : kwargs['data'].corr()
                }
    }
    def pricer(values,**kwargs):
        if isinstance(values,pd.DataFrame): values = csv_to_np(values,**kwargs).squeeze().T
        out= kwargs['getter'].get_closed_formula().prices(values = values,set_fun = set_fun,**kwargs)
        return out
    out = {**params,**kwargs}
    out['pricer'] = pricer

    def graphic(**out):
        pricer_values = get_matrix(out['pricer'](values =out['data'], **out))
        times = get_matrix(np.array(get_time(out['data'],**out)))
        basket_values = get_matrix(out['basket_values'](values =out['data'], **out))
        values = np.concatenate([times,pricer_values],axis=1)
        figure2 = pd.DataFrame(values, columns=['basket values','pricer values'])
        plot1D(figure2,labelx = 'times days', labely= 'pricer values')
        plt.show()
    out['graphic'] = graphic
    return out


def get_model_param(kwargs = get_pricer_param()):
    params = {
        'map':cartesian_map,
        'seed':None,
        'list_maps':np.repeat(log_ret,len(kwargs['symbols']))
    }
    def transform(values,**kwargs):
        times =get_time(values,**kwargs)
        values_ = get_matrix(values).T
        values_ = values_.reshape((1,)+values_.shape)
        out = pd.DataFrame(kwargs['map'](values_,times =times,**kwargs).squeeze().T,columns = values.columns) 
        return out
    out = {**params,**kwargs}
    out['transform'] = transform
    out['transform_h'] = transform(out['data'],**out)

    def graphic(**params):
        transform_h = params['transform'](params['data'],**params)
        dim = len(params['symbols'])
        if dim == 1: multi_plot([[transform_h.values[:,0]]],mp_figsize=(3,3),fun_plot = hist_plot, labelx=params['symbols'][0], mp_ncols = 1, **kwargs) 
        else : scatter_hist(transform_h.values[:,0], transform_h.values[:,1], labelx=params['symbols'][0],labely = params['symbols'][1],figsize=(5,5),**params)

    out['graphic'] = graphic

    return out

def get_generated_param(kwargs = get_model_param()):
    def graphic(**params):
        transform_g = kwargs['transform_g']
        dim = len(params['symbols'])
        if dim == 1: multi_plot([[transform_g.values[:,0]]],mp_figsize=(3,3),fun_plot = hist_plot, labelx=params['symbols'][0], mp_ncols = 1, **kwargs) 
        else : scatter_hist(transform_g.values[:,0], transform_g.values[:,1],figsize=(5,5), labelx=params['symbols'][0],labely = params['symbols'][1],**params)

    kwargs['transform_g'] = alg.sampler(fx=kwargs['transform_h'],M=1000,**kwargs)[0]
    kwargs['graphic'] = graphic

    return kwargs



def generated_paths(params = get_model_param()):
    def graphic(**params):
        f_z,data,f_x=RegenerateHistory(**params,Nz=10)
        plot_trajectories(f_z,f_x,data,symbols = params['symbols']),plt.show()
    params['graphic'] = graphic
    return params

def get_var_data(horizon=10,kwargs = get_model_param()):
    getter = kwargs['getter']
    params = {
        'Nz':500,
        'H':5,
    }
    out = {**params,**kwargs}
    columns = out['data'].columns

    def np_to_csv(np,columns = columns,**kwargs):
        values = np.squeeze()
        values,index= values[:,1:],values[:,0]
        out = pd.DataFrame(values,columns = columns,index = index)  
        return out

    def random_sample(shape,**kwargs):
        import sobol
        return sobol.sample(dimension=shape[1], n_points=shape[0])

    samples = csv_to_np(out['data'],**out)
    sample_times=get_float(getter.get_today_date(**out))+horizon
    VaRData = historical_path_generator().generate_from_samples(
        samples = samples,
        sample_times=[sample_times],
        initial_values = getter.get_spot(**out),
        time_start=getter.get_today_date(**out),
        random_sample = random_sample,
        **out).squeeze()
    sample_times=get_float(getter.get_today_date(**out))+out['H']

    TestData = historical_path_generator().generate_from_samples(
        samples = samples,
        sample_times=[sample_times],
        initial_values = getter.get_spot(**out),
        time_start=getter.get_today_date(**out),**out)

    sample_times=get_float(getter.get_today_date(**out))+1
    TestData[:,0,:] = sample_times
    out['TestData'] = np_to_csv(TestData,**out)  
    values= VaRData[:,1:]
    index = np.repeat(sample_times,values.shape[0])
    VaRData = pd.DataFrame(values,columns = columns,index = index)
    index = index+1.
    VarDataPlus = pd.DataFrame(values,columns = columns,index = index)
    index = index-2.
    VarDataMinus = pd.DataFrame(values,columns = columns,index = index)
    out['VaRData'] = pd.concat([VaRData,VarDataPlus,VarDataMinus])
    def fun(x,**kwargs): 
        out= np.ndarray([x.shape[0],2])
        out[:,0],out[:,1] = get_time(x,**kwargs),kwargs['getter'].get_closed_formula().get_spot_basket(x,**kwargs)
        return out

    def graphic(**out):
        strike = getter.get_strike(**out)
        baskets = basket_values(values = TestData[:,1:],**kwargs)
        baskets = (baskets/strike - 1.)*100 
        multi_plot( [[out['data'],out['TestData']],[out['VaRData'],out['TestData']] ],
            plot_confidence_levels,
            f_names = ["Hist. training / test set","VaR training / test set"],
            labelx = 'basket values',labely = 'time',
            listlabels = [],
            mp_figsize=(5,5),
            fun = fun,
            loc = 'upper left',prop={'size': 3},mp_ncols=2,**out)
    out['graphic'] = graphic
    return out

def predict_prices(kwargs = get_var_data()):
    getter = kwargs['getter']
    def taylor(values,**kwargs): 
        time_spot_ = kwargs['getter'].get_time_spot(**kwargs)
        fx =  kwargs['pricer'](values = time_spot_,**kwargs)
        taylor_explanation = {}
        out = alg.taylor_expansion(x=time_spot_, y=time_spot_,z=values, fx=fx, nabla = getter.get_closed_formula(**kwargs).nabla, hessian = getter.get_closed_formula(**kwargs).hessian,taylor_order = 2,taylor_explanation=taylor_explanation,**kwargs)
        return out

    def plot_helper(xfx,**kwargs):
        spot_baskets, pnls = xfx[0],xfx[1]
        compare_plot_lists(spot_baskets, pnls, **kwargs)

    def codpy(values,**kwargs):
        x = csv_to_np(kwargs['VaRData']).squeeze().T
        fx = get_matrix(kwargs['pricer'](x,**kwargs))
        fx_variate =  get_matrix(kwargs['payoff'](x,**kwargs))
        fz_variate =  get_matrix(kwargs['payoff'](values,**kwargs))
        fx -= fx_variate
        out = op.projection(x = x,y = x,z = values, fx = fx,**kwargs)
        out += fz_variate
        return out

    params = {
        'taylor':taylor,
        'codpy':codpy,
    }
    out = {**params,**kwargs}

    def graphic(**out):
        labelx = 'Basket Values (% K)'
        labely = 'Option Values (USD)'
        maturity_date = [get_float(getter.get_maturity_date(**out)) - get_float(getter.get_today_date(**out))]
        f_names = ["exact-Taylor-codpy"]
        TestData = csv_to_np(out['TestData'],**out).squeeze().T
        strike = getter.get_strike(**out)
        baskets = basket_values(values = TestData[:,1:],**kwargs)
        baskets = (baskets/strike - 1.)*100 
        plot_datas = [[
            [baskets,baskets,baskets],
            [out['pricer'](TestData,**out),out['taylor'](TestData,**out),out['codpy'](TestData,**out)],
        ]]
        title_fig = ["Exact", "Taylor", "codpy"]
        multi_plot(plot_datas,plot_helper,f_names = f_names,labelx = labelx,labely = labely,listlabels =title_fig,mp_figsize=(9,4),loc = 'upper left',prop={'size': 3},mp_ncols=2,**out)
    out['graphic'] = graphic
    return out

def predict_greeks(kwargs = predict_prices()):

    def plot_helper(xfx,**kwargs):
        x, fx = xfx[0],xfx[1]
        compare_plot_lists(x, fx, **kwargs)
    def codpy_nabla(values,**k): 
        x = csv_to_np(k['VaRData']).squeeze().T
        fx = get_matrix(k['pricer'](x,**k))
        out = op.nabla(x=x, y=x, z=values, fx=fx,  **k).squeeze()
        # fx = get_matrix(k['payoff'](x,**k))
        # fx_variate =  get_matrix(kwargs['payoff'](x,**k))
        # fx -= fx_variate 
        # nabla_fz_variate = k['getter'].get_instrument(**k).nabla_f(values).squeeze()
        # xbaskets,zbaskets = np.zeros([x.shape[0],2]),np.zeros([values.shape[0],2])
        # xbaskets[:,1],xbaskets[:,0] = basket_values(values = x[:,1:],**kwargs),x[:,0]
        # zbaskets[:,1],zbaskets[:,0] = basket_values(values = values[:,1:],**kwargs),values[:,0]
        # out = op.nabla(x=xbaskets, y=xbaskets, z=zbaskets, fx=fx,  **k).squeeze()
        # out =np.concatenate([out[:,[0]],out[:,[1]] @ get_matrix(k['getter'].get_weights(**k)).T], axis = 1)
        # out += nabla_fz_variate 
        return out

    def taylor_delta(self,**k): 
        getter = k['getter']
        x =  getter.get_time_spot(**k)
        z =  csv_to_np(k['TestData']).T.squeeze()
        delta = k['getter'].get_closed_formula().nablas(values = x,set_fun = set_fun,**k)
        gamma = k['getter'].get_closed_formula().hessians(values = x,set_fun = set_fun,**k)
        indices = np.repeat(0,z.shape[0])
        deltas= delta[indices]
        gammas = gamma[indices]
        product_ = np.reshape([gammas[n] @ deltas[n] for n in range(gammas.shape[0])],deltas.shape)
        f_z = delta  + product_
        return f_z


    def graphic(**out):
        dim = len(out['symbols'])
        getter = out['getter']
        labelx = 'Basket Values (% K)'
        labely = 'Values'
        listlabels = ['Exact','Codpy','Taylor']
        TestData = csv_to_np(out['TestData'],**out).squeeze().T
        exact_nabla_ = getter.get_closed_formula(**kwargs).nablas(TestData,set_fun = set_fun,**out)
        codpy_nabla_ = out['codpy_nabla'](TestData,**out).squeeze()
        taylor_delta_ = taylor_delta(TestData,**out).squeeze()

        f_names = ["Theta"]+["Delta-"+out['symbols'][n] for n in range(0,dim)]
        strike = getter.get_strike(**out)
        baskets = basket_values(values = TestData[:,1:],**kwargs)
        baskets = (baskets/strike - 1.)*100 
        plot_datas = [
            [
                [baskets,baskets,baskets],
                [exact_nabla_[:,n],codpy_nabla_[:,n],taylor_delta_[:,n]]
            ] for n in range(0,dim+1)
        ]
        title_fig = ["Exact-codpy-taylor"]
        multi_plot(plot_datas,plot_helper,f_names = f_names,labelx = labelx,labely = labely,listlabels =listlabels,mp_figsize=(9,4),loc = 'upper left',prop={'size': 4},mp_ncols=2,**out)
        pass

    kwargs['graphic'] = graphic
    kwargs['codpy_nabla'] = codpy_nabla
    return kwargs

if __name__=="__main__":
    params = get_var_data()
    params['graphic'](**params)

    pass
