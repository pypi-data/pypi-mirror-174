from preamble import *


currentdir = os.path.dirname(os.path.realpath(__file__))

class PnL_time_series_generator(time_serie_generator):

    def get_params(**kwargs) : return kwargs.get('PnL_time_series_generator',{})
    def get_H(**kwargs) : return int(PnL_time_series_generator.get_params(**kwargs)['H'])
    def get_sep(**kwargs) : return PnL_time_series_generator.get_params(**kwargs).get('sep',";")
    def get_xfx_csv(**kwargs) : return PnL_time_series_generator.get_params(**kwargs).get('xfx_csv',None)
    def get_raw_data_csv(**kwargs) : return PnL_time_series_generator.get_params(**kwargs).get('raw_data_csv',None)

    def get_raw_data(self,**kwargs):
        params = time_serie_generator.get_params(**kwargs)
        csv_file = PnL_time_series_generator.get_raw_data_csv(**kwargs)
        sep = PnL_time_series_generator.get_sep(**kwargs)
        if csv_file is not None and os.path.exists(csv_file): data = pd.read_csv(csv_file,sep=sep, index_col = 0)
        else: data = PnL_time_series_generator.get_stocks_data(**kwargs)
        yf_params = time_serie_generator.get_yf_params(**kwargs)
        date_format = yf_params.get('date_format','%d/%m/%Y')
        data = ts_data.interpolate(data,**params, float_fun = lambda x: get_float(x,date_format = date_format))
        return data

    def get_stocks_data(**kwargs):
        yf_params = time_serie_generator.get_yf_params(**kwargs)
        data = ts_data.get_yf_ts_data(**yf_params)

        # sep,yf_csv_date_format,time_col = ts_data.get_param(**yf_params)

        data.insert(loc=0, column=ts_data.get_time_col(**kwargs), value=get_float(data.index,date_format = ts_data.get_date_format(**kwargs)))

        raw_data_csv = PnL_time_series_generator.get_raw_data_csv(**kwargs)
        if raw_data_csv is not None and not os.path.exists(raw_data_csv): data.to_csv(raw_data_csv,sep = ts_data.get_sep(**kwargs), index = True)
        return data
    
    def get_x_shifted(self, x,**kwargs): 
        Shift = PnL_time_series_generator.get_H(**kwargs)
        shifted_cols = list(map(lambda x:x+"_shift", x.columns))
        x_shifted = x.shift(periods = -Shift).dropna()
        x_shifted.columns = shifted_cols
        return x_shifted

    def get_data(self, D=0,Nx=0,Ny=0,Nz=0, **kwargs):
        from sklearn.model_selection import train_test_split
        params = time_serie_generator.get_params(**kwargs)
        xfx_csv = PnL_time_series_generator.get_xfx_csv(**kwargs)
        sep = PnL_time_series_generator.get_sep(**kwargs)
        Shift = PnL_time_series_generator.get_H(**kwargs)
        x = self.get_raw_data(**kwargs)
        shifted_cols = list(map(lambda x:x+"_shift", x.columns))
        x_shifted = x.shift(periods = -Shift).dropna()
        x_shifted.columns = shifted_cols
        xfx = pd.concat([x_shifted,x], axis = 1).dropna()
        if xfx_csv is not None and not os.path.exists(xfx_csv): xfx.to_csv(xfx_csv,sep = sep, index = True)
        x,x_shifted = xfx.iloc[:,int(len(xfx.columns)/2):],xfx.iloc[:,:int(len(xfx.columns)/2)]
        test_size = time_serie_generator.get_test_size(**kwargs)
        fx = PnL_time_series_generator.PnL(x,x_shifted, **kwargs)
        z,fz = xfx,fx
        if test_size is not None: 
            x, a, fx, a = train_test_split(xfx, fx, test_size = test_size, shuffle=False)
        else: x, z, fx, fz = xfx, xfx, fx,fx
        return x, fx,x, fx,z, fz




class option_param:

    def get_var_data(v,**k):
        raw_data = PnL_time_series_generator().get_raw_data(**k)
        newk = {**k,**{'historical_data':raw_data}}
        out = option_param.historical_data_shifted(v,**newk)
        newk = {**newk,**{'historical_data_shifted':out}}
        out = option_param().sample_times(**newk)
        sample_times = out[0]
        newk = {**newk,**{'sample_times':out}}
        days = k.get("days",None)
        newk['grid_projection'] = True
        newk['days'] = 2*days
        out = option_param().generated_data(**newk,seed = 42)
        N = out.shape[0]
        lower_shift,upper_shift = out.copy(),out.copy()
        lower_shift[:,0,:] -= 1.
        upper_shift[:,0,:] += 1.
        out = np.concatenate([lower_shift,out,upper_shift])
        return pd.DataFrame(out[:,:,0],columns = raw_data.columns)

    def get_var_values(self,**k): 
        x =  k['var_data']
        return k['getter'].get_closed_formula().prices(values =x, set_fun = option_param.set_fun_helper,**k)
        pass

    def get_historical_data(self,**k):
        return PnL_time_series_generator().get_raw_data(**k)

    def historical_data_shifted(v,**k):
        out = PnL_time_series_generator().get_x_shifted(x = k['historical_data'],**k)
        return out
    def set_fun_helper(v,**kwargs):  return basket_option_param_getter().set_spot_today_date(values=v[1:],time=datetime.date.fromordinal(int(v[0])),**kwargs)
    def set_spot(self,**kwargs):  
        getter = kwargs.get('getter')
        spot = self.get_last_variable(**kwargs)[1:]
        return getter.set_spot(spot,**kwargs) 
             

    def spots(self,**kwargs):  
            z = kwargs['generated_data']
            getter = kwargs.get('getter')
            historical_data_shifted = kwargs.get('historical_data_shifted')
            spot = get_matrix(self.get_last_variable(**kwargs))
            x = z.copy() 
            x[:,0,:] = historical_data_shifted.values[-1,0]
            def helper(n):x[n,:,:] = spot
            [helper(n) for n in range(0,x.shape[0])]
            return x
    def generated_pnls(self,**kwargs):  
            z,x = kwargs['generated_data'],kwargs['spots']
            getter = kwargs.get('getter')
            return getter.get_closed_formula().pnls(**kwargs, z=z,x =x, set_fun = option_param.set_fun_helper)
    def historical_pnls(self,**kwargs):  
            z,x = kwargs['historical_data_shifted'].values[:, :, np.newaxis],kwargs['historical_data'].values[:, :, np.newaxis]
            getter = kwargs.get('getter')
            out= getter.get_closed_formula().pnls(**kwargs, z=z,x =x, set_fun = option_param.set_fun_helper)
            return out
    def sample_times(self,**k):  
        #out = get_date(k.get('historical_data').values[-1,0])
        out = k.get('getter').get_today_date(**k) + datetime.timedelta(days = PnL_time_series_generator.get_H(**k))
        # out += datetime.timedelta(days = PnL_time_series_generator.get_H(**k))
        return [out]
    def generated_data(self,**k):  
        days = k.get("days",None)
        if days is not None: k['sample_times'][0] += datetime.timedelta(days=days)
        getter = k.get('getter')
        time_start = getter.get_today_date(**k)
        initial_values = getter.get_spot(**k)
        samples =  PnL_time_series_generator().get_raw_data(**k)
        out = historical_path_generator().generate_from_samples(samples = samples,time_start=time_start,initial_values=initial_values,**k)
        if days is not None: out[:,0,:] -= days
        return out

    def basket_values(self,**k):  
        out = k['getter'].get_closed_formula().get_spot_basket(x= k['generated_data'][:,1:,:],**k)
        return out

    def get_last_basket_value(self,**k): 
        return k['getter'].get_closed_formula().get_spot_basket(x = self.get_last_variable(**k)[1:],**k)
    def get_last_variable(self,**k): 
        raw_data = PnL_time_series_generator().get_raw_data(**k)
        variables = raw_data.iloc[-1,:]
        return variables.values
    def get_last_value(self,**k): 
        variables = self.get_last_variable(**k)
        # getter = k.get('getter')
        # strike = getter.get_strike(**k)
        # spot = getter.get_spot(**k)
        value= k['getter'].get_closed_formula().price(**k, x =variables, set_fun = option_param.set_fun_helper)
        return value

    def codpy_pnl(self,**k): 
        x =  k['historical_data'].values.copy()
        fx =  get_matrix(k['historical_prices']).copy()
        fx_variate =  get_matrix(k['historical_payoffs']).copy()
        z =  k['generated_data'][:,:,0].copy()
        fz_variate =  get_matrix(k['generated_payoffs']).copy()
        fx -= fx_variate

        out = op.projection(x = x,y = x,z = z, fx = fx,**k)

        fz = get_matrix(k['generated_prices'].copy())-fz_variate
        listlabels = ["fz","fx","out"]
        # compare_plot_lists(listxs = (z[:,1],x[:,1],z[:,1]), listfxs = (fz,fx,out),listlabels=listlabels)
        # compare_plot_lists(listxs = (x[:,1]), listfxs = (fx),listlabels=listlabels)
        # plt.plot(fx)
        # plt.show()

        out += fz_variate
        out -= self.get_last_value(**k)
        return out
    def get_indices(self,x,z,**k): return np.repeat(x.shape[0]-PnL_time_series_generator.get_H(**k),z.shape[0])

    def exact_nabla(self,**k): 
        generated_data =  np.squeeze(k['generated_data'])
        return k['getter'].get_closed_formula().nablas(values = generated_data,setter = option_param.set_fun_helper,**k)

    def exact_hessian(self,**k): 
        generated_data =  np.squeeze(k['generated_data'])
        return k['getter'].get_closed_formula().hessians(values = generated_data,setter = option_param.set_fun_helper,**k)

    def codpy_nabla(self,**k): 
        x =  k['historical_data'].values
        z =  k['generated_data'][:,:,0]
        fx_variate =  get_matrix(k['historical_payoffs']).copy()
        fx = get_matrix(k['historical_prices'].copy())-fx_variate # Prix - Payoff : Fonction qui converge vers 0 
        nabla_fz_variate = k['getter'].get_instrument(**k).nabla_f(z) # Nabla(Payoff)
        out = op.nabla(x=x, y=x, z=z, fx=fx, **k) # Nabla(Prix - Payoff)
        out += nabla_fz_variate # Nabla(Prix - Payoff) + Nabla(Payoff) = Nabla(Prix) : Ressemblance avec la methode controle variate
        return out

    def codpy_hessian(self,**k): 
        x =  k['historical_data'].values
        z =  k['generated_data'][:,:,0]
        N_X,N_Z,D = x.shape[0],z.shape[0],x.shape[1]

        hessian_fx_variate = k['getter'].get_closed_formula().hessians(values = x,setter = option_param.set_fun_helper,**k)
        hessian_fx_variate = hessian_fx_variate.reshape([N_X, D * D])

        out = op.projection(x=x, y=x, z=z, fx=hessian_fx_variate, **k).reshape(N_Z,D,D,1)
        return out


    def codpy_taylor(self,**k): 

        historical_prices = get_matrix(k['historical_prices'])
        x =  k['historical_data'].values.copy()
        fx =  get_matrix(k['historical_prices']).copy()
        fx_variate =  get_matrix(k['historical_payoffs']).copy()
        z =  k['generated_data'][:,:,0].copy()
        fz_variate =  get_matrix(k['generated_payoffs']).copy()
        fx -= fx_variate
        fz = get_matrix(k['generated_prices'].copy())-fz_variate

        indices = self.get_indices(x=x,z=z,**k)
        taylor_explanation = {}

        nabla_fx_variate = option_param.nabla(x=x,fun = option_param.payoff,**k)
        def local_nabla(x, y, z, fx, **kwargs):
            out = op.nabla(x=x, y=y, z=x, fx=fx, **kwargs)
            out[:,:,0] += nabla_fx_variate
            return out
        out = alg.taylor_expansion(x=x, y=x,z=z, fx=fx, taylor_order = 1,indices=indices,taylor_explanation=taylor_explanation,nabla = local_nabla,**k)

        # out = alg.taylor_expansion(x=x, y=x,z=z, fx=fx, taylor_order = 1,indices=indices,taylor_explanation=taylor_explanation,**k)
        indices = taylor_explanation['indices']
        fz = get_matrix(k['generated_prices'].copy())-fz_variate
        listlabels = ["fz","fx","out"]
        compare_plot_lists(listxs = (z[:,1],x[:,1],z[:,1]), listfxs = (fz,fx,out),listlabels=listlabels)

        # out += fz_variate
        # out -= historical_prices[-PnL_time_series_generator.get_H(**k)]
        return out

    def delta_taylor(self,**k): 
        x =  get_matrix(self.get_last_variable(**k)).T
        z =  np.squeeze(k['generated_data'])
        deltas = k['getter'].get_closed_formula().nablas(values = x,setter = option_param.set_fun_helper,**k)
        fdelta =  deltas[0][1]
        gammas = k['getter'].get_closed_formula().hessians(values = x,setter = option_param.set_fun_helper,**k)
        fgamma = gammas[0,1,1]
        indices = self.get_indices(x=x,z=z,**k)
        taylor_explanation = {}
        xo= x[indices]
        fxo = np.empty(len(z))
        fxo.fill(fdelta)
        gamma = np.empty(len(z))
        gamma.fill(fgamma)
        deltax = get_data(z - xo)
        deltax = deltax[:,1]
        # fx = fdelta[1]
        # grad = op.nabla_test(x=x, y=x, z=x, fx = fx, **k)
        # if grad.ndim >= 3:  grad= get_matrix(np.squeeze(grad))
        # if len(indices) : grad = grad[indices]
        product_ = np.reshape([np.dot(gamma[n],deltax[n]) for n in range(gamma.shape[0])],(len(gamma),1))
        f_z = fxo  + product_
        return f_z,taylor_explanation

    def payoff(x,**k):
        getter = k.get("getter")
        if x.ndim == 2: x = x.ravel()
        date_ = datetime.datetime.strftime(get_date(x[0]), '%d/%m/%Y')
        newk = getter.set_today_date(date_,**k)
        newk = getter.set_spot(x[1:],**newk)
        out = BasketOption(**newk).f(x)
        # print("x:",x,",price:",price)
        return out
    def price(x,**k):
        getter = k.get("getter")
        date_ = datetime.datetime.strftime(get_date(x[0]), '%d/%m/%Y')
        newk = getter.set_today_date(date_,**k)
        newk = getter.set_spot(x[1:],**newk)
        price = k['getter'].get_closed_formula().price(**newk)
        # print("x:",x,",price:",price)
        return price
    def nabla(x,fun = None,**kwargs): 
        out = get_matrix(kwargs['getter'].get_closed_formula().nabla(values = x,setter = option_param.set_fun_helper,**kwargs)).T
        out[:,0] /= 365.
        return out
    def hessian(x,fun = None,**kwargs): 
        out = kwargs['getter'].get_closed_formula().hessian(values = x,setter = option_param.set_fun_helper,**kwargs)
        out[:,0,:] /= 365.
        out[:,:,0] /= 365.
        return out

    def exact_taylor(self,**k): 
        x =  get_matrix(self.get_last_variable(**k)).T
        fx =  self.get_last_value(**k)
        z =  np.squeeze(k['generated_data'])
        indices = self.get_indices(x=x,z=z,**k)
        taylor_explanation = {}
        out = alg.taylor_expansion(x=x, y=x,z=z, fx=fx, nabla = option_param.nabla, hessian = option_param.hessian,taylor_order = 2,indices=indices,taylor_explanation=taylor_explanation,**k)
        out[:,0] -=fx
        return out,taylor_explanation

    def historical_prices(self,**k): 
        x =  k['historical_data']
        out = k['getter'].get_closed_formula().prices(values =x, set_fun = option_param.set_fun_helper,**k)
        # historical_time_test = x.values[:,0]
        # historical_time_test = historical_time_test.reshape((3,5)).T
        # historical_prices_test = out.copy()
        # historical_prices_test = historical_prices_test.reshape((3,5)).T
        return out
    def generated_prices(self,**k): 
        x =  k['generated_data']
        return k['getter'].get_closed_formula().prices(values =x, set_fun = option_param.set_fun_helper,**k)
        pass
    def historical_payoffs(self,**k): 
        x =  k['historical_data']
        out =  k['getter'].get_instrument(**k).f(x =x.values[:,1:])
        return out
    def generated_payoffs(self,**k): 
        x =  k['generated_data']
        out =  k['getter'].get_instrument(**k).f(x =x[:,1:])
        return out

    def get_codpy_param(self):
        return  {'rescale_kernel':{'max': 1500, 'seed':42},
        'debug' : True,
        'sharp_discrepancy':{'max': 1000, 'seed':42},
        'discrepancy':{'max': 1000, 'seed':42},
        'validator_compute': ['accuracy_score','discrepancy_error','norm'],
        # 'set_codpy_kernel' : kernel_setters.kernel_helper(kernel_setters.set_linear_regressor_kernel, 2,1e-8 , map_setters.set_unitcube_map),
        'set_codpy_kernel' : kernel_setters.kernel_helper(kernel_setters.set_tensornorm_kernel, 2,1e-8 ,map_setters.set_unitcube_map),
        # 'set_codpy_kernel' : kernel_setters.kernel_helper(kernel_setters.set_tensornorm_kernel, 0,0 ,map_setters.set_unitcube_mean_map),
        # 'set_codpy_kernel' : kernel_setters.kernel_helper(kernel_setters.set_matern_tensor_kernel, 0 ,1e-8 ,map_setters.set_standard_mean_map),
        # 'set_codpy_kernel' : kernel_setters.kernel_helper(kernel_setters.set_gaussian_kernel, 3 ,1e-8 ,map_setters.set_standard_min_map),
        'rescale': True,
        }
    def get_maturity_date(self,**k): return  k['getter'].get_maturity_date(**k)
    def get_strike(self,**k): return  k['getter'].get_strike(**k)



    def get_funs(self):
        funs = {
        'funs':{
            self.set_spot:None,
            'historical_data':self.get_historical_data,
            'historical_data_shifted':self.historical_data_shifted,
            'sample_times':self.sample_times,
            'generated_data':self.generated_data,
            'spots': self.spots,
            'historical_payoffs':self.historical_payoffs,
            'generated_payoffs':self.generated_payoffs,
            'generated_pnls':self.generated_pnls,
            'historical_pnls':self.historical_pnls,
            'generated_basket_values':self.basket_values,
            'historical_prices': self.historical_prices,
            'exact_nabla':self.exact_nabla,
            'exact_hessian':self.exact_hessian,
            'generated_prices': self.generated_prices,
            'codpy_nabla':self.codpy_nabla,
            'codpy_hessian':self.codpy_hessian,
            'codpy_pnls':self.codpy_pnl,
            'exact_taylor_pnls':self.exact_taylor,
            'taylor_delta':self.delta_taylor,
            'maturity_date': self.get_maturity_date,
            'strike': self.get_strike
            }
        }
        return funs
    def get_global_param(self):
        params = {
        'days' : 4,
        'today_date': global_param['end_date'],
        'map':log_return,
        'grid_projection' : False,
        'time_serie_generator' : {
            'yf_param' : {
                'symbols':global_param['symbols'],
                'begin_date':global_param['begin_date'],
                'end_date':global_param['end_date'],
                'yahoo_columns': global_param['yahoo_columns'],
                'yf_begin_date': global_param['yf_begin_date'],
                'csv_file' : os.path.join(data_path,"PnL",'-'.join(global_param['symbols'])+'-'+global_param['begin_date'].replace('/','-')+"-"+global_param['end_date'].replace('/','-')+".csv"),
                'date_format' : '%d/%m/%Y',
                'yahoo_date_format':'%Y-m%-d%',            
                'csv_date_format':'%d/%m/%Y'            
            },
            'PnL_csv' : os.path.join(data_path,"PnL","PnL"+".csv"),
            'xfx_csv' : os.path.join(data_path,"PnL","xfx"+".csv")
            },
        'PnL_time_series_generator' : {
            'H': global_param['H'],
            'raw_data_csv' : os.path.join(data_path,"PnL","PnL_time_series_generator-"+'-'.join(global_param['symbols'])+'-'+global_param['begin_date'].replace('/','-')+"-"+global_param['end_date'].replace('/','-')+".csv"),
        },
        'N':500,
        'MonteCarloPricer' :{ 'N':500},
        'QL_historical_generator' : {
        'N':1,
        'T':3047,
        'process':BSM(),
        'seed':111
        },
        }
        return params

    def get_asset_param(self):
        from dateutil.relativedelta import relativedelta
        from dateutil import parser
        params = {
        'getter':basket_option_param_getter(),
        'BasketOption' : {
                    'weights': global_param['weights'],
                    'option_type' :     ql.Option.Call,
                    'maturity_date' : get_date(global_param['end_date']) + relativedelta(days=10),
                    # 'strike_price' : 6100.,
                    'strike_price' : 4050.,
                    # 'strike_price' : 1.,
                    },
        }
        return params

    def get_process_param(self):
        params = {
        'BSMultiple':  {
                    'BSMs': [ 
                        {
                        'BSM':{
                        'spot_price' : 4101,
                        'risk_free_rate' : 0,
                        'dividend_rate' : 0, 
                        'volatility' : 0.25,
                        }},
                        # {
                        # 'BSM':{
                        # 'spot_price' : 7533,
                        # 'risk_free_rate' : 0,
                        # 'dividend_rate' : 0,
                        # 'volatility' : 0.25,
                        # }},
                        # {
                        # 'BSM':{
                        # 'spot_price' : 3756.07006835937,
                        # 'risk_free_rate' : 0,
                        # 'dividend_rate' : 0.01,
                        # 'volatility' : 0.2,
                        # }}
                        ],
                    # 'correlation_matrix' : [[1, 0, 0], 
                    #                         [0, 1, 0],
                    #                         [0, 0, 1]]
                    # 'correlation_matrix' : [[1, 0], 
                    #                         [0, 1]]
                    'correlation_matrix' : [[1]]
                    },
        'path_generator':{'process' : BSMultiple()},
        }
        return params


    def get_param(self):
        return {**self.get_codpy_param(),**self.get_funs(),**self.get_process_param(),**self.get_asset_param(),**self.get_global_param()}

class option_param_var(option_param):
    def get_historical_data(self,**k):
        return self.get_var_data(**k)

    def get_indices(self,x,z,**k): 
        if x.shape[0] == 1: 
            return np.repeat(0,z.shape[0])
        return []

class Binary_param(option_param_var):
    
    
    def get_asset_param(self):
        from dateutil.relativedelta import relativedelta
        from dateutil import parser
        params = {
        'getter':basket_binary_param_getter(),
        'BasketBinary' : {
                    'weights': global_param['weights'],
                    'option_type' :     ql.Option.Call,
                    'maturity_date' : get_date(global_param['end_date']) + relativedelta(days=30),
                    'strike_price' : 4101.,
                    # 'strike_price' : 1.,
                    },
        }
        return params
    


class scenarios_PnL(scenarios_MC):
    def format_output(results):
        maturities,spot_baskets,exact_pnls,codpy_pnls,codpy_taylor_pnls,exact_taylor_pnls,strikes = [],[],[],[],[],[],[]
        for index,r in zip(range(len(results)),results):
                maturities.append(str(r['maturity_date']))
                strikes.append(str(r['strike']))
                b,p,c,e = r['generated_basket_values'],r['generated_pnls'],r['codpy_pnls'],r['exact_taylor_pnls']
                min_ = min(len(b),len(p))
                spot_baskets.append(b[:min_])
                exact_pnls.append(p[:min_])
                codpy_pnls.append(c[:min_])
                exact_taylor_pnls.append(e[0][:min_])
        return spot_baskets,exact_pnls,codpy_pnls,exact_taylor_pnls,maturities,strikes


def single_scenario_error_output(results,**kwargs):
    spot_baskets,exact_pnls,codpy_pnls,exact_taylor_pnls,maturities,strikes = scenarios_PnL.format_output(results)
    spot_baskets,exact_pnls,codpy_pnls,exact_taylor_pnls = spot_baskets[0].ravel(),exact_pnls[0].ravel(),codpy_pnls[0].ravel(),exact_taylor_pnls[0].ravel()
    error_codpy = exact_pnls-codpy_pnls
    error_exact_taylor = exact_pnls-exact_taylor_pnls
    f_names = ["error codpy","error exact taylor","error delta","error gamma" ]
    labelx = 'basket values'
    labely = 'PnL'
    multi_plot([[spot_baskets,error_codpy],[spot_baskets,error_exact_taylor]],plotD_strike_spot,f_names = f_names,labelx = labelx,labely = labely,**kwargs)


def single_scenario_exact_deltas_output(results,**kwargs):
    spot_baskets,exact_pnls,codpy_pnls,exact_taylor_pnls,maturities,strikes = scenarios_PnL.format_output(results)
    generated_data = results[0]['generated_data'][:,:,0]
    codpy_nabla = results[0]['codpy_nabla']
    exact_nabla = results[0]['exact_nabla']
    exact_nabla[:,0] /= 365.
    codpy_nabla[:,0] /= 365.
    thetas = [exact_nabla[:,0],codpy_nabla[:,0,0]]
    deltas = [exact_nabla[:,1],codpy_nabla[:,1,0]]
    spot_baskets = [spot_baskets[0].copy(),spot_baskets[0].copy()]

    def plot_helper(xfx,**kwargs):
        spot_baskets, values = xfx[0],xfx[1]
        compare_plot_lists(spot_baskets, values, **kwargs)
        params = option_param()
        ax = kwargs['ax']
        spot = params.get_last_basket_value(**kwargs)
        strike = kwargs['getter'].get_strike(**kwargs)
        ax.axvline(x=spot, linewidth=1.0, color = "c", label="spot")
        ax.axvline(x=strike, linewidth=1.0, color = "m", label="strike")
        ax.legend(loc = 'upper left',prop={'size': 6})


    f_names = ["Delta","Theta"]
    labelx = 'basket values'
    labely = 'values'
    listlabels = ["exact","codpy"]
    multi_plot([[spot_baskets,deltas],[spot_baskets,thetas]],plot_helper,f_names = f_names,labelx = labelx,labely = labely,listlabels = listlabels,loc = 'upper left',prop={'size': 3},mp_ncols=2,**kwargs)

def single_scenario_exact_deltas_output_amine(results,**kwargs):
    spot_baskets,exact_pnls,codpy_pnls,exact_taylor_pnls,maturities,strikes = scenarios_PnL.format_output(results)
    generated_data = results[0]['generated_data'][:,:,0]
    codpy_nabla = results[0]['codpy_nabla']
    exact_nabla = results[0]['exact_nabla']
    exact_nabla[:,0] /= 365.
    # codpy_nabla[:,0] /= 12.
    taylor_delta = results[0]['taylor_delta']
    thetas = [exact_nabla[:,0],codpy_nabla[:,0,0]]
    # deltas = [exact_nabla[:,1],codpy_nabla[:,1,0]]
    deltas = [exact_nabla[:,1],codpy_nabla[:,1,0],(taylor_delta[0])[:,1]]

    spot_baskets = [spot_baskets[0].copy(),spot_baskets[0].copy()]

    def plot_helper(xfx,**kwargs):
        spot_baskets, values = xfx[0],xfx[1]
        compare_plot_lists(spot_baskets, values, **kwargs)
        params = option_param()
        ax = kwargs['ax']
        spot = params.get_last_basket_value(**kwargs)
        strike = kwargs['getter'].get_strike(**kwargs)
        spot = (spot/strike - 1)*100
        strike = (strike/strike - 1)*100
        ax.axvline(x=spot, linewidth=1.0, color = "c", label="spot")
        ax.axvline(x=strike, linewidth=1.0, color = "m", label="strike")
        ax.legend(loc = 'upper left',prop={'size': 6})
        ax.ticklabel_format(axis="y", style="sci", scilimits=(0,0))


    spot_strike = np.array([(((spot_baskets[0])[i]/float(strikes[0])) - 1)*100 for i in range(len(spot_baskets[0]))])
    spot_basket_strike_delta = np.array([spot_strike,spot_strike,spot_strike])
    spot_basket_strike_theta = np.array([spot_strike,spot_strike])
    # spot_basket_strike = np.array([spot_strike,spot_strike])
    f_names = ["Delta","Theta"]
    labelx = 'Values (% K)'
    labely = 'Values (USD)'
    listlabels = ["exact","codpy","taylor"]
    # print (time.time() - start)
    multi_plot([[spot_basket_strike_delta,deltas],[spot_basket_strike_theta,thetas]],plot_helper,f_names = f_names,labelx = labelx,labely = labely,listlabels = listlabels,loc = 'upper left',prop={'size': 3},mp_ncols=2,**kwargs)

def single_scenario_exact_delta_output_amine(results,**kwargs):
    spot_baskets,exact_pnls,codpy_pnls,exact_taylor_pnls,maturities,strikes = scenarios_PnL.format_output(results)
    generated_data = results[0]['generated_data'][:,:,0]
    codpy_nabla = results[0]['codpy_nabla']
    exact_nabla = results[0]['exact_nabla']
    exact_nabla[:,0] /= 365.
    taylor_delta = results[0]['taylor_delta']
    # thetas = [exact_nabla[:,0],codpy_nabla[:,0,0]]
    deltas = [exact_nabla[:,1],codpy_nabla[:,1,0],(taylor_delta[0])[:,1]]
    spot_baskets = [spot_baskets[0].copy()]

    def plot_helper(xfx,**kwargs):
        spot_baskets, values = xfx[0],xfx[1]
        compare_plot_lists(spot_baskets, values, **kwargs)
        params = option_param()
        ax = kwargs['ax']
        spot = params.get_last_basket_value(**kwargs)
        strike = kwargs['getter'].get_strike(**kwargs)
        spot = (spot/strike - 1)*100
        strike = (strike/strike - 1)*100
        ax.axvline(x=spot, linewidth=1.0, color = "c", label="spot")
        ax.axvline(x=strike, linewidth=1.0, color = "m", label="strike")
        ax.legend(loc = 'upper left',prop={'size': 6})
        ax.ticklabel_format(axis="y", style="sci", scilimits=(0,0))
        

    spot_strike = np.array([(((spot_baskets[0])[i]/float(strikes[0])) - 1)*100 for i in range(len(spot_baskets[0]))])
    spot_basket_strike = np.array([spot_strike,spot_strike,spot_strike])

    f_names = ["Delta"]
    labelx = 'Values (% K)'
    labely = 'Values (USD)'
    listlabels = ["exact","codpy","taylor"]
    multi_plot([[spot_basket_strike,deltas]],plot_helper,f_names = f_names,labelx = labelx,labely = labely,listlabels = listlabels,loc = 'upper left',prop={'size': 3},mp_ncols=2,**kwargs)


def single_scenario_exact_gammas_output(results,**kwargs):
    spot_baskets,exact_pnls,codpy_pnls,exact_taylor_pnls,maturities,strikes = scenarios_PnL.format_output(results)
    generated_data = results[0]['generated_data'][:,:,0]
    historical_data = results[0]['historical_data'].values
    historical_prices = results[0]['historical_prices']

    codpy_hessians = np.squeeze(results[0]['codpy_hessian'])
    # exact_hessians =     k['getter'].get_closed_formula().hessians(values = historical_data,setter = option_param.set_fun_helper,**kwargs)
    exact_hessians =     results[0]['exact_hessian']

    codpy_hessians = np.squeeze(results[0]['codpy_hessian'])
    thetas = [exact_hessians[:,0,0],codpy_hessians[:,0,0]]
    gammas = [exact_hessians[:,1,1],codpy_hessians[:,1,1]]
    crossed = [exact_hessians[:,0,1],codpy_hessians[:,1,0]]

    # thetas = exact_hessians[:,0,0]
    # gammas = exact_hessians[:,1,1]
    # crossed = exact_hessians[:,0,1]

    spot_baskets = [spot_baskets[0].copy(),spot_baskets[0].copy()]

    def plot_helper(xfx,**kwargs):
        spot_baskets, values = xfx[0],xfx[1]
        compare_plot_lists_ax_amine(spot_baskets, values, **kwargs)
        params = option_param()
        ax = kwargs['ax']
        spot = params.get_last_basket_value(**kwargs)
        strike = kwargs['getter'].get_strike(**kwargs)
        ax.axvline(x=spot, linewidth=1.0, color = "c", label="spot")
        ax.axvline(x=strike, linewidth=1.0, color = "m", label="strike")
        ax.legend(loc = 'upper left',prop={'size': 6})


    f_names = ["thetas","gammas","cross sensis"]
    labelx = 'basket values'
    labely = 'values'
    listlabels = ["exact","codpy"]

    # multi_plot([[historical_data,historical_prices],[historical_data,thetas],[historical_data,gammas],[historical_data,crossed]],plotD,projection='3d',loc = 'upper left',prop={'size': 3},mp_ncols=2,**kwargs)

    multi_plot([[spot_baskets,thetas],[spot_baskets,gammas],[spot_baskets,crossed]],plot_helper,f_names = f_names,labelx = labelx,labely = labely,listlabels = listlabels,loc = 'upper left',prop={'size': 3},**kwargs)
    pass

def single_scenario_exact_gammas_output_amine(results,**kwargs):
    spot_baskets,exact_pnls,codpy_pnls,exact_taylor_pnls,maturities,strikes = scenarios_PnL.format_output(results)
    generated_data = results[0]['generated_data'][:,:,0]
    historical_data = results[0]['historical_data'].values
    historical_prices = results[0]['historical_prices']

    codpy_hessians = np.squeeze(results[0]['codpy_hessian'])
    # exact_hessians =     k['getter'].get_closed_formula().hessians(values = historical_data,setter = option_param.set_fun_helper,**kwargs)
    exact_hessians =     results[0]['exact_hessian']

    codpy_hessians = np.squeeze(results[0]['codpy_hessian'])
    thetas = [exact_hessians[:,0,0],codpy_hessians[:,0,0]]
    gammas = [exact_hessians[:,1,1],codpy_hessians[:,1,1]]
    crossed = [exact_hessians[:,0,1],codpy_hessians[:,1,0]]

    # thetas = exact_hessians[:,0,0]
    # gammas = exact_hessians[:,1,1]
    # crossed = exact_hessians[:,0,1]

    spot_baskets = [spot_baskets[0].copy(),spot_baskets[0].copy()]

    def plot_helper(xfx,**kwargs):
        spot_baskets, values = xfx[0],xfx[1]
        compare_plot_lists(spot_baskets, values, **kwargs)
        params = option_param()
        ax = kwargs['ax']
        spot = params.get_last_basket_value(**kwargs)
        strike = kwargs['getter'].get_strike(**kwargs)
        spot = (spot/strike - 1)*100
        strike = (strike/strike - 1)*100
        ax.axvline(x=spot, linewidth=1.0, color = "c", label="spot")
        ax.axvline(x=strike, linewidth=1.0, color = "m", label="strike")
        ax.legend(loc = 'upper left',prop={'size': 6})
        ax.ticklabel_format(axis="y", style="sci", scilimits=(0,0))

    spot_strike = np.array([(((spot_baskets[0])[i]/float(strikes[0])) - 1)*100 for i in range(len(spot_baskets[0]))])
    spot_basket_strike = np.array([spot_strike,spot_strike])

    # f_names = ["Thetas","Gammas","Cross sensis"]
    f_names = ["Gammas","Time/Spot"]
    labelx = 'Values (% K)'
    labely = 'Values (USD)'
    listlabels = ["exact","codpy"]

    # multi_plot([[historical_data,historical_prices],[historical_data,thetas],[historical_data,gammas],[historical_data,crossed]],plotD,projection='3d',loc = 'upper left',prop={'size': 3},mp_ncols=2,**kwargs)

    # multi_plot([[spot_basket_strike,thetas],[spot_basket_strike,gammas],[spot_basket_strike,crossed]],plot_helper,f_names = f_names,labelx = labelx,labely = labely,listlabels = listlabels,loc = 'upper left',prop={'size': 3},**kwargs)
    multi_plot([[spot_basket_strike,gammas],[spot_basket_strike,crossed]],plot_helper,f_names = f_names,labelx = labelx,labely = labely,listlabels = listlabels,loc = 'upper left',prop={'size': 3},**kwargs)

    pass

def plotD_strike_spot(param,ax,**kwargs):
    out = plotD(param,ax,**kwargs)
    params = option_param()
    spot = params.get_last_basket_value(**kwargs)
    strike = kwargs['getter'].get_strike(**kwargs)
    ax.axvline(x=spot, linewidth=1.0, color = "c", label="spot")
    ax.axvline(x=strike, linewidth=1.0, color = "m", label="strike")
    ax.legend(loc = 'upper left',prop={'size': 6})
    return out

def plotD_strike_spot_1(param,ax,**kwargs):
    out = plotD(param,ax,**kwargs)
    params = option_param()
    spot = params.get_last_basket_value(**kwargs)
    strike = kwargs['getter'].get_strike(**kwargs)
    ax.axvline(x=spot, linewidth=1.0, color = "c", label="spot")
    ax.axvline(x=strike, linewidth=1.0, color = "m", label="strike")
    ax.legend(loc = 'upper left',prop={'size': 6})
    ax.set_ylim([-100, 100])
    return out

def single_scenario_output(results,**kwargs):
    spot_baskets,exact_pnls,codpy_pnls,exact_taylor_pnls,maturities,strikes = scenarios_PnL.format_output(results)
    spot_baskets,exact_pnls,codpy_pnls,exact_taylor_pnls = spot_baskets[0].ravel(),exact_pnls[0].ravel(),codpy_pnls[0].ravel(),exact_taylor_pnls[0].ravel()
    error_codpy = exact_pnls-codpy_pnls
    error_exact_taylor = exact_pnls-exact_taylor_pnls
    f_names = ["PnL exact","PnL codpy" ,"PnL taylor" ]
    labelx = 'basket values'
    labely = 'PnL'
    multi_plot([[spot_baskets,exact_pnls],[spot_baskets,codpy_pnls],[spot_baskets,exact_taylor_pnls]],plotD_strike_spot_1,f_names = f_names,labelx = labelx,labely = labely,**kwargs)
    

def multiple_scenario_output(results,**kwargs):
    from dateutil.relativedelta import relativedelta
    from dateutil import parser
    spot_baskets,exact_pnls,codpy_pnls,exact_taylor_pnls,maturities,strikes = scenarios_PnL.format_output(results)
    def plot_helper(xfx,**kwargs):
        spot_baskets, pnls = xfx[0],xfx[1]
        compare_plot_lists(spot_baskets, pnls, **kwargs)
    f_names = ["PnL exact","PnL codpy" ,"PnL taylor" ]
    labelx = 'basket values'
    labely = 'PnL'
    date1 = parser.parse((get_date(global_param['end_date'])).strftime("%Y-%m-%d"))
    maturity_date = [date1 for i in range(len(maturities))]
    date2 = [parser.parse(maturities[i]) for i in range(len(maturities))]
    diff = [(date2[i] - maturity_date[i] ).days for i in range(len(maturities))]
    diff = [("T = " + str(diff [i]) +" days") for i in range(len(maturities))]
    multi_plot([[spot_baskets,exact_pnls],[spot_baskets,codpy_pnls],[spot_baskets,exact_taylor_pnls]],plot_helper,f_names = f_names,labelx = labelx,labely = labely,listlabels =diff,mp_figsize=(9,9),loc = 'upper left',prop={'size': 3},mp_ncols=2,**kwargs)

def multiple_scenario_output_amine(results,**kwargs):
    from dateutil.relativedelta import relativedelta
    from dateutil import parser
    spot_baskets,exact_pnls,codpy_pnls,exact_taylor_pnls,maturities,strikes = scenarios_PnL.format_output(results)
    def plot_helper(xfx,**kwargs):
        spot_baskets, pnls = xfx[0],xfx[1]
        compare_plot_lists(spot_baskets, pnls, **kwargs)
    N = len(exact_pnls)
    labelx = 'Values (% K)'
    labely = 'Values (USD)'
    date1 = parser.parse((get_date(global_param['end_date'])).strftime("%Y-%m-%d"))
    maturity_date = [date1 for i in range(N)]
    date2 = [parser.parse(maturities[i]) for i in range(N)]
    diff = [(date2[i] - maturity_date[i] ).days for i in range(N)]
    f_names = [("T = " + str(diff [i]) +" days") for i in range(N)]
    scenarios = [ [exact_pnls[n],codpy_pnls[n],exact_taylor_pnls[n]] for n in range(N)]
    def helper(n) : 
        out = (spot_baskets[n]/float(strikes[n]) - 1)*100 
        return out.flatten()
    spot_strikes = [ helper(n)for n in range(N)]
    spot_strikes = [ (spot_strikes[n],spot_strikes[n],spot_strikes[n]) for n in range(N)]
    plot_datas = [[spot_strikes[n],scenarios[n]] for n in range(N)]
    title_fig = ["Exact PnL", "Codpy PnL", "Taylor PnL"]
    multi_plot(plot_datas,plot_helper,f_names = f_names,labelx = labelx,labely = labely,listlabels =title_fig,mp_figsize=(9,4),loc = 'upper left',prop={'size': 3},mp_ncols=2,**kwargs)
    pass

def multiple_scenario_output_amine_zoom(results,**kwargs):
    from dateutil.relativedelta import relativedelta
    from dateutil import parser
    spot_baskets,exact_pnls,codpy_pnls,exact_taylor_pnls,maturities,strikes = scenarios_PnL.format_output(results)
    def plot_helper(xfx,**kwargs):
        spot_baskets, pnls = xfx[0],xfx[1]
        compare_plot_lists(spot_baskets, pnls, **kwargs)
        
    N = len(exact_pnls)
    labelx = 'Basket values in percentage of the strike'
    labely = 'PnL in $'
    date1 = parser.parse((get_date(global_param['end_date'])).strftime("%Y-%m-%d"))
    maturity_date = [date1 for i in range(N)]
    date2 = [parser.parse(maturities[i]) for i in range(N)]
    diff = [(date2[i] - maturity_date[i] ).days for i in range(N)]
    f_names = [("T = " + str(diff [i]) +" days") for i in range(N)]
    scenarios = [ [exact_pnls[n],codpy_pnls[n],exact_taylor_pnls[n]] for n in range(N)]
    def helper(n) : 
        out = (spot_baskets[n]/float(strikes[n]) - 1)*100 
        return out.flatten()
    spot_strikes = [ helper(n)for n in range(N)]
    spot_strikes = [ (spot_strikes[n],spot_strikes[n],spot_strikes[n]) for n in range(N)]
    plot_datas = [[spot_strikes[n],scenarios[n]] for n in range(N)]
    title_fig = ["Exact PnL", "Codpy PnL", "Taylor PnL"]
    multi_plot(plot_datas,plot_helper,f_names = f_names,labelx = labelx,labely = labely,listlabels =title_fig,mp_figsize=(9,9),loc = 'upper left',prop={'size': 3},mp_ncols=2,**kwargs)
    pass

def get_symbols():
    symbols = global_param['symbols']
    symbols = [ c.replace('^','') for c in symbols]
    return symbols

def plot_train_test_variables(results,**kwargs):

    fun = kwargs['getter'].get_closed_formula().get_spot_basket
    generated_data = results[0]['generated_data'][:,:,0]
    historical_data = get_matrix(results[0]['historical_data'])
    minmax = np.array(get_box([generated_data,historical_data]))

    x = data_random_generator().get_raw_data(Nx = 1000, Ny = 0, Nz=0, D = historical_data.shape[1],minmax=minmax,**kwargs)[0]
    fx = kwargs['getter'].get_closed_formula().prices(**kwargs, values =x,set_fun = option_param.set_fun_helper)

    dates = set(x[:,0])
    if len(dates) > 1:
        x = pd.DataFrame(x,columns = ["times","basket values"])    
        fx = pd.DataFrame(fx,columns = ["option prices"])
        multi_plot([(x,fx)],plot_trisurf,projection='3d',elev = 30,azim=-25,linewidth = 0.2,antialiased = True,figsize=(15,15))
    else:
        f_names = ["option prices" ]
        labelx = 'basket values'
        labely = 'option prices'
        multi_plot([(x[:,1],fx)],plotD_strike_spot,f_names = f_names,labelx = labelx,labely = labely,**kwargs,figsize=(15,15))

def rmd_generated_data(results):
    generated_data = results[0]['generated_data']
    generated_data = np.squeeze(generated_data)
    generated_data = pd.DataFrame(generated_data,columns = ["Date"]+get_symbols())
    generated_data.Date = [str(get_date(n)) for n in generated_data.Date]
    return generated_data
     
def plot_confidence_levels(param,**kwargs):
    import itertools
    def fun(x,**kwargs): 
        out= np.ndarray([x.shape[0],2])
        out[:,0],out[:,1] = get_float(x.index),kwargs['getter'].get_closed_formula().get_spot_basket(x,**kwargs)
        return out
    fun = kwargs.get('fun',fun)
    training_set,test_set = fun(param[0],**kwargs),fun(param[1],**kwargs)

    ax = get_ax_helper(**kwargs)

    minmax = np.array(get_box([test_set,training_set]))
    mean = minmax.mean(axis=1)
    for d in range(minmax.shape[1]):
        min_,max_ = minmax[d,0],minmax[d,1]
        if min_==max_:
            minmax[d][0] -= 1
            minmax[d][1] += 1
        else:
            minmax[d][0] -= abs(minmax[d][0]-mean[d])*.1
            minmax[d][1] += abs(minmax[d][0]-mean[d])*.1
    Nx = kwargs.get("Nx",100)
    xlist = np.linspace(minmax[0][0], minmax[0][1], Nx)
    ylist = np.linspace(minmax[1][0],minmax[1][1], Nx)
    x = np.asarray([e for e in itertools.product(xlist,ylist)])
    X, Y = np.meshgrid(xlist, ylist)
    # fig, ax = plt.subplots()

    Dxy = op.Dnm(x =x,y=training_set,**kwargs)
    Dxy = Dxy.min(axis = 1)
    mat= np.zeros([Nx,Nx])
    def helper(n):
        m,k = np.argmin(abs(x[n,0]-xlist)),np.argmin(abs(x[n,1]-ylist))
        mat[k,m] = Dxy[n]
    [helper(n) for n in range(0,x.shape[0])]
    contour_filled = ax.contour(X,Y,mat)
    ax.clabel(contour_filled, fmt = '%2.1f', fontsize=6)
    plt.colorbar(contour_filled)
    plt.xlabel('time')
    plt.ylabel('basket')

    xb2,yb2,xt2,yt2 = test_set[:,0], test_set[:,1:],training_set[:,0], training_set[:,1:]
    xb2,yb2,xt2,yt2 = xb2,yb2,xt2,yt2

    x,y = np.concatenate((get_matrix(xb2),get_matrix(yb2)),axis=1),np.concatenate((get_matrix(xt2),get_matrix(yt2)),axis=1)
    scatter_params=[{'marker' : 'o','s':10,'color' : 'red','label':'training set'},{'s':10,'marker' : 'o','color' : 'blue','label':'test set'}]
    scatter_plot((y,x),ax = ax, mp_ncols = 4,scatter_params=scatter_params) 
    #plt.show()
    pass

def plot_train_test_set(results,**kwargs):

    historical_data = get_matrix(results[0]['historical_data'])
    generated_data = results[0]['generated_data'][:,:,0]
    raw_data = PnL_time_series_generator().get_raw_data(**kwargs)

    # plot_confidence_levels(training_set = historical_data,test_set = generated_data,**params_option)
    # plot_confidence_levels(training_set = raw_data,test_set = generated_data,**params_option)

    f_names = ["VaR train / test set","Hist. obs. train / test set"]
    labelx = 'basket values'
    labely = 'time'
    listlabels = []

    multi_plot([[historical_data,generated_data],[raw_data,generated_data]],plot_confidence_levels,f_names = f_names,labelx = labelx,labely = labely,listlabels = listlabels,mp_figsize=(9,4),loc = 'upper left',prop={'size': 3},mp_ncols=2,**kwargs)



def single_scenario(**kwargs): return scenarios_PnL().run([kwargs])

def rmd_test_set(results):
    generated_data = results[0]['generated_data']
    generated_data = np.squeeze(generated_data)
    generated_data = pd.DataFrame(generated_data,columns = ["Date"]+get_symbols())
    generated_data.Date = [str(get_date(n)) for n in generated_data.Date]
    return generated_data
   

def maturity_scenario(**kwargs):
    debug = kwargs.get("debug",False)
    nb_tick = kwargs.get('tick',3) 
    getter = kwargs['getter']
    today_date = getter.get_today_date(**kwargs)
    maturity = get_float(getter.get_maturity_date(**kwargs)) - get_float(today_date)
    def helper(n) : return today_date + datetime.timedelta(days = n)
    scenarios_mat, values = ['BasketOption','maturity_date'],[helper(maturity * i / nb_tick) for i in range(1,nb_tick)]
    # scenarios_mat, values = ['BasketBinary','maturity_date'],[helper(maturity * i / nb_tick) for i in range(1,nb_tick)]
    list_scenarios=generate_scenario().generate(scenarios_mat,values,[kwargs])
    return scenarios_PnL().run(list_scenarios,debug=debug)

def maturity_scenario_amine(**kwargs):
    debug = kwargs.get("debug",False)
    getter = kwargs['getter']
    today_date = getter.get_today_date(**kwargs)
    maturity = get_float(getter.get_maturity_date(**kwargs)) - get_float(today_date)
    def helper(n) : return today_date + datetime.timedelta(days = n)
    # date_test = kwargs.get("maturities",[10,30,90,180,365])
    date_test = kwargs.get("maturities",[10,365])
    scenarios_mat, values = ['BasketOption','maturity_date'],[helper(date_test[i]) for i in range(0,len(date_test))]
    # scenarios_mat, values = ['BasketBinary','maturity_date'],[helper(date_test[i]) for i in range(0,len(date_test))]

    list_scenarios=generate_scenario().generate(scenarios_mat,values,[kwargs])
    return scenarios_PnL().run(list_scenarios,debug=debug)

def get_codpy_PnL_error_matrix(results,file_name=None):
    from dateutil import parser
    spot_baskets,exact_pnls,codpy_pnls,exact_taylor_pnls,maturities,strikes = scenarios_PnL.format_output(results)
    N = len(exact_pnls)
    error_codpy = [get_relative_mean_squared_error(exact_pnls[n],codpy_pnls[n]) for n in range(0,len(exact_pnls))]
    date1 = parser.parse((get_date(global_param['end_date'])).strftime("%Y-%m-%d"))
    maturity_date = [date1 for i in range(N)]
    date2 = [parser.parse(maturities[i]) for i in range(N)]
    diff = [(date2[i] - maturity_date[i] ).days for i in range(N)]
    f_names = [("T = " + str(diff [i]) +" days") for i in range(N)]
    errors_codpy_matrix = pd.DataFrame(columns = set(f_names),index = set(strikes))
    for e,m,s in zip(error_codpy,f_names,strikes):errors_codpy_matrix.loc[s,m] = str(format(e*100,".2f"))+'\%'
    if file_name is not None: save_to_file(x=errors_codpy_matrix,file_name = file_name)
    return errors_codpy_matrix
def get_taylor_PnL_error_matrix(results,file_name=None):
    from dateutil import parser
    spot_baskets,exact_pnls,codpy_pnls,exact_taylor_pnls,maturities,strikes = scenarios_PnL.format_output(results)
    N = len(exact_pnls)
    error_codpy = [get_relative_mean_squared_error(exact_pnls[n],exact_taylor_pnls[n]) for n in range(0,len(exact_pnls))]
    date1 = parser.parse((get_date(global_param['end_date'])).strftime("%Y-%m-%d"))
    maturity_date = [date1 for i in range(N)]
    date2 = [parser.parse(maturities[i]) for i in range(N)]
    diff = [(date2[i] - maturity_date[i] ).days for i in range(N)]
    f_names = [("T = " + str(diff [i]) +" days") for i in range(N)]
    errors_taylor_matrix = pd.DataFrame(columns = set(f_names),index = set(strikes))
    for e,m,s in zip(error_codpy,f_names,strikes):errors_taylor_matrix.loc[s,m] = str(format(e*100,".2f"))+'\%'
    if file_name is not None: save_to_file(x=errors_taylor_matrix,file_name = file_name)
    return errors_taylor_matrix

def get_codpy_PnL_error_matrix_with_range(results,file_name=None):
    spot_baskets,exact_pnls,codpy_pnls,exact_taylor_pnls,maturities,strikes = scenarios_PnL.format_output(results)
    d=0.95
    u=1.05
    barrier_down = float(strikes[0])*d
    barrier_up = float(strikes[0])*u
    s0_codpy = [codpy_pnls[0], codpy_pnls[1], codpy_pnls[2]]
    s1_exact = [exact_pnls[0], exact_pnls[1], exact_pnls[2]]
    for i, val in enumerate(spot_baskets[0]) : 
        if ((spot_baskets[0])[i]>barrier_up or (spot_baskets[0])[i]< barrier_down) : 
            print(val)
            s0_codpy[0] = np.delete(s0_codpy[0],i)
            s0_codpy[1] = np.delete(s0_codpy[1],i)
            s0_codpy[2] = np.delete(s0_codpy[2],i)
            s1_exact[0] = np.delete(s1_exact[0],i)
            s1_exact[1] = np.delete(s1_exact[1],i)
            s1_exact[2] = np.delete(s1_exact[2],i)
    error_codpy = [get_relative_mean_squared_error(s1_exact[n],s0_codpy[n]) for n in range(0,len(s1_exact))]
    errors_codpy_matrix = pd.DataFrame(columns = set(maturities),index = set(strikes))
    for e,m,s in zip(error_codpy,maturities,strikes):errors_codpy_matrix.loc[s,m] = str(format(e*100,".2f"))+'\%'
    if file_name is not None: save_to_file(x=errors_codpy_matrix,file_name = file_name)
    return errors_codpy_matrix
    
def get_taylor_PnL_error_matrix_with_range(results,file_name=None):
    spot_baskets,exact_pnls,codpy_pnls,exact_taylor_pnls,maturities,strikes = scenarios_PnL.format_output(results)
    d=0.95
    u=1.05
    barrier_down = float(strikes[0])*d
    barrier_up = float(strikes[0])*u
    s0_taylor = [exact_taylor_pnls[0], exact_taylor_pnls[1], exact_taylor_pnls[2]]
    s1_exact = [exact_pnls[0], exact_pnls[1], exact_pnls[2]]
    for i, val in enumerate(spot_baskets[0]) : 
        if ((spot_baskets[0])[i]>barrier_up or (spot_baskets[0])[i]< barrier_down) : 
            print(val)
            s0_taylor[0] = np.delete(s0_taylor[0],i)
            s0_taylor[1] = np.delete(s0_taylor[1],i)
            s0_taylor[2] = np.delete(s0_taylor[2],i)
            s1_exact[0] = np.delete(s1_exact[0],i)
            s1_exact[1] = np.delete(s1_exact[1],i)
            s1_exact[2] = np.delete(s1_exact[2],i)
    error_codpy = [get_relative_mean_squared_error(s1_exact[n],s0_taylor[n]) for n in range(0,len(s1_exact))]
    errors_taylor_matrix = pd.DataFrame(columns = set(maturities),index = set(strikes))
    for e,m,s in zip(error_codpy,maturities,strikes):errors_taylor_matrix.loc[s,m] = str(format(e*100,".2f"))+'\%'
    if file_name is not None: save_to_file(x=errors_taylor_matrix,file_name = file_name)
    return errors_taylor_matrix

def get_deltas_error_matrix(results,file_name=None):
    spot_baskets,exact_pnls,codpy_pnls,exact_taylor_pnls,maturities,strikes = scenarios_PnL.format_output(results)
    def helper(r):
        codpy_nabla = r['codpy_nabla']
        exact_nabla = r['exact_nabla']
        exact_nabla[:,0] /= 365.
        return get_relative_mean_squared_error(codpy_nabla,exact_nabla) 
    error_codpy = [helper(r) for r in results]
    errors_matrix = pd.DataFrame(columns = set(maturities),index = set(strikes))
    for e,m,s in zip(error_codpy,maturities,strikes):errors_matrix.loc[s,m] = str(format(e*100,".2f"))+'\%'
    if file_name is not None: save_to_file(x=errors_matrix,file_name = file_name)
    return errors_matrix
def get_gammas_error_matrix(results,file_name=None):
    spot_baskets,exact_pnls,codpy_pnls,exact_taylor_pnls,maturities,strikes = scenarios_PnL.format_output(results)
    def helper(r):
        codpy_nabla = r['codpy_hessian']
        exact_nabla = r['exact_hessian']
        return get_relative_mean_squared_error(codpy_nabla,exact_nabla) 
    error_codpy = [helper(r) for r in results]
    errors_matrix = pd.DataFrame(columns = set(maturities),index = set(strikes))
    for e,m,s in zip(error_codpy,maturities,strikes):errors_matrix.loc[s,m] = str(format(e*100,".2f"))+'\%'
    if file_name is not None: save_to_file(x=errors_matrix,file_name = file_name)
    return errors_matrix
    

def strike_maturity_scenario(**kwargs):
    debug = kwargs.get("debug",False)
    nb_tick = kwargs.get('tick',6) 
    getter = kwargs['getter']
    today_date = getter.get_today_date(**kwargs)
    maturity = get_float(getter.get_maturity_date(**kwargs)) - get_float(today_date)
    def helper(n) : return today_date + datetime.timedelta(days = n)
    scenarios_mat, values = ['BasketOption','maturity_date'],[helper(maturity * i / nb_tick) for i in range(1,nb_tick)]
    list_scenarios=generate_scenario().generate(scenarios_mat,values,[kwargs])
    strike = getter.get_strike(**kwargs)
    scenarios_strike, values = ['BasketOption','strike_price'],[strike * (1. - (nb_tick/2.-float(i))/100.)  for i in range(1,nb_tick)]
    list_scenarios=generate_scenario().generate(scenarios_strike,values,list_scenarios)
    return scenarios_PnL().run(list_scenarios,debug = debug)
    indice = np.argmax(error_codpy)
    spot_baskets,exact_pnls,codpy_pnls,codpy_taylor_pnls,exact_taylor_pnls = spot_baskets[indice],exact_pnls[indice],codpy_pnls[indice],codpy_taylor_pnls[indice],exact_taylor_pnls[indice]
    print("worst error for strike =",strikes[indice], "; maturity = ", maturities[indice], ";error codpy% =",error_codpy[indice], ";error taylor% =",error_taylor[indice])
    pass

if __name__ == "__main__":
    import cProfile, pstats, io
    import re

   
    # codpy_error_matrix = get_codpy_PnL_error_matrix(results,file_name = "codpy_binary_error_matrix.csv").sort_index(axis=0)
    # taylor_error_matrix = get_taylor_PnL_error_matrix(results,file_name = "taylor_binary_error_matrix.csv").sort_index(axis=0)
    # deltas_error_matrix = get_deltas_error_matrix(results,file_name = "deltas_binary_error_matrix.csv").sort_index(axis=0)
    # gammas_error_matrix = get_gammas_error_matrix(results,file_name = "gammas_binary_error_matrix.csv").sort_index(axis=0)
    # print(codpy_error_matrix)
    # print(taylor_error_matrix)
    # print(deltas_error_matrix)
    # print(gammas_error_matrix)

#    
    # codpy_error_matrix = get_codpy_PnL_error_matrix(results).sort_index(axis=0)
    params_option = option_param_var().get_param()
    # results = scenarios_PnL().run([params_option])

    # results = single_scenario(**params_option)
    # single_scenario_output(results,**params_option)
    # single_scenario_error_output(results,**params_option)

    results = maturity_scenario_amine(**params_option)
    multiple_scenario_output_amine(results,**params_option)

    # results = maturity_scenario(**params_option)
    # multiple_scenario_output(results,**params_option)

    # single_scenario_error_output(results,**params_option)


    # plot_train_test_set(results=results,**params_option)
    # single_scenario_exact_delta_output_amine(results,**params_option)
    # single_scenario_exact_deltas_output_amine(results,**params_option)
    # single_scenario_exact_gammas_output_amine(results,**params_option)
    # # plot_train_test_set(results,**option_param_var().get_param())
    # plot_train_test_variables(results,**option_param_var().get_param())
    # single_scenario_output(results,**params_option)
    # single_scenario_error_output(results,**params_option)
    # results =  strike_maturity_scenario(**option_param_var().get_param())
    # multiple_scenario_output(results)

    # results =  strike_maturity_scenario(**option_param().get_param())
    codpy_error_matrix = get_codpy_PnL_error_matrix(results,file_name = "codpy_binary_error_matrix.csv").sort_index(axis=0)
    taylor_error_matrix = get_taylor_PnL_error_matrix(results,file_name = "taylor_binary_error_matrix.csv").sort_index(axis=0)
    print(codpy_error_matrix)
    print(taylor_error_matrix)
    # strike_maturity_scenario(**option_param().get_param())
    pass


