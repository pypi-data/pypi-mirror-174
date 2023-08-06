import copy
import numpy as np
import time
from codpy_tools import parallel_task,get_relative_mean_squared_error

class scenarios_MC:
    def __init__(self):
        self.results =[]

    def run(self,scenarios,**kwargs):
        from codpy_tools import elapsed_time
        if isinstance(scenarios,list):
            self.results = parallel_task(scenarios,self.run,**kwargs)
            # self.results = [self.run(scenarios=scenario) for scenario in scenarios]
            return self.results 
        else:
            funs=scenarios.get('funs',AssertionError())
            out_scenario = {}
            for k in funs.keys():
                def fun(**scenarios): return obj(**scenarios)
                if isinstance(k,str):
                    obj=funs[k]
                    # out = elapsed_time(fun,msg="keys:"+k+" elapsed_time in seconds:",**scenarios)
                    out = fun(**{**scenarios,**out_scenario})
                    # out = fun(**scenarios,**out_scenario)
                    out_scenario[k]=out
                else: 
                    scenarios = k(**{**scenarios,**out_scenario})

            # test = get_relative_mean_squared_error(out_scenario['generated_pnls'],out_scenario['codpy_pnls'])                    

            return out_scenario

class generate_scenario:
    dic = {}

    def __init__(self,**kwargs):
        self.dic = copy.deepcopy(kwargs)

    def flatten_list(list_of_lists, flat_list=[]):
        if isinstance(list_of_lists,list):
            [generate_scenario.flatten_list(list_of_lists=item,flat_list = flat_list) for item in list_of_lists]
            return flat_list
        flat_list.append(list_of_lists)


    def generate(self,keys, values,scenarios):
        if isinstance(scenarios ,list):
            return generate_scenario.flatten_list([self.generate(keys,values,s) for s in scenarios], flat_list=[])
        def helper(keys,value,**kwargs):
            out=copy.deepcopy(kwargs)
            obj=out
            last_string=keys[-1]
            for s in keys[:-1]:
                obj=obj[s]
            obj[last_string]=value
            return out
        out = []
        for value in values:
            out.append(helper(keys = keys, value = value,**scenarios))
        return out


        