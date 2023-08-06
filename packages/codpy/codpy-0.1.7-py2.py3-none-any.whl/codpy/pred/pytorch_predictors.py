import os, sys
from pathlib import Path
import torch.nn as nn
import torch
from preamble import *
from data_generators import * 
from codpy_predictors import * 



class PytorchRegressor(data_predictor):
    def get_params(**kwargs): return kwargs.get('PytorchRegressor',{})
    def get_model(self, **kwargs):
        import torch
        from torch.utils.data import DataLoader
        from torch.utils.data import TensorDataset
        import os
        os.environ["KMP_DUPLICATE_LIB_OK"]="TRUE"
        FX = torch.tensor(get_matrix(kwargs.get('FX',self.fx)),dtype=torch.float)
        self.epochs = kwargs.get('epochs',500)
        batch_size = kwargs.get('batch_size',128)
        layers = kwargs.get('layers', [128,64])
        out_layer =  kwargs.get('out_layer', FX.shape[1])
        self.loss = kwargs.get('loss',nn.CrossEntropyLoss())
        #dataset=TensorDataset(torch.tensor(get_matrix(self.x),dtype=torch.float),torch.tensor(get_matrix(self.fx),dtype=torch.float))
        #self.dataloader=DataLoader(dataset,batch_size = batch_size, shuffle=False)
        return PytorchNet(input_dim = self.D ,hidden_dim = layers, out_dim = out_layer, **kwargs)    
    def predictor(self,**kwargs):
        params = PytorchRegressor.get_params(**kwargs)
        self.model = self.fit(**params)
        self.f_z = self.predict(self.z)
    def fit(self, **kwargs):  
        import torch.jit as jit
        #model = torch.jit.script(self.get_model(**kwargs))
        optimizer = kwargs.get('optimizer', torch.optim.Adam)
        criterion = kwargs.get('loss', nn.MSELoss())
        model = self.get_model(**kwargs)
        optimizer = optimizer(model.parameters())
        log_each = 500
        x,fx = torch.FloatTensor(get_matrix(self.x)),torch.FloatTensor(get_matrix(self.fx))
        x.requires_grad_(True)
        for step in range(self.epochs):
            #for batch_x,batch_fx in dataloader:
            y_hat = model(x) 
            loss = criterion(fx, y_hat)
            optimizer.zero_grad()
            loss.backward()
            optimizer.step()
            if step % log_each == 0:
                print(f'{step}/{self.epochs} loss {loss.item():.5f}')
        return model
    def predict(self,x):
        self.model.eval()
        x = torch.FloatTensor(get_matrix(x))
        with torch.no_grad():
            p = self.model(x)
        return p.numpy().ravel()   
    def gradient(self,**kwargs):
        self.predictor(**kwargs)
        z = torch.FloatTensor(get_matrix(self.z)).requires_grad_(True)
        y = self.model(z)
        grad_outputs = torch.ones_like(y)
        try:
            self.grad = torch.autograd.grad(y, [z], grad_outputs = grad_outputs, create_graph=True)[0]
        except:
            self.model.eval()
            self.grad = torch.autograd.grad(y, [z], grad_outputs = grad_outputs, create_graph=True)[0]
        self.grad = self.grad.detach().numpy()
        return self.grad

    def id(self):
        return "PytorchRegressor"


class PytorchClassifier(codpyprClassifier, add_confusion_matrix):
    def get_params(**kwargs): return kwargs.get('PytorchClassifier',{})
    def get_model(self, **kwargs):
        import torch
        from torch.utils.data import DataLoader
        from torch.utils.data import TensorDataset
        import os
        params = PytorchClassifier.get_params(**kwargs)
        os.environ["KMP_DUPLICATE_LIB_OK"]="TRUE"
        self.epochs = params.get('epochs',5)
        batch_size = params.get('batch_size',128)
        layers = params.get('layers', [128,64])
        out_layer =  params.get('out_layer', [10])
        self.loss = params.get('loss',nn.CrossEntropyLoss())
        activation = params.get('activation',nn.ReLU())
        data_type = params.get("datatype", "float")
        dataset=TensorDataset(torch.tensor(self.x,dtype=torch.float),torch.tensor(self.fx,dtype=torch.long))
        self.dataloader=DataLoader(dataset,batch_size = batch_size, shuffle=False)
        return PytorchNet(input_dim = self.D ,hidden_dim = layers, out_dim = out_layer, activation = activation)

    def predictor(self,**kwargs):
        import torch
        optimizer = kwargs.get('optimizer', torch.optim.Adam)
        model = self.get_model(**kwargs)
        optimizer = optimizer(PytorchNet.parameters(model), lr=0.001)
        self.fit(**kwargs)
        z = torch.FloatTensor(self.z)
        self.f_z = model.predict(z, **kwargs)

    def fit(self,epochs, **kwargs):  
        import torch.jit as jit
        #model = torch.jit.script(self.get_model(**kwargs))
        optimizer = kwargs.get('optimizer', torch.optim.Adam)
        criterion = kwargs.get('loss', nn.MSELoss())
        model = self.get_model(**kwargs)
        optimizer = optimizer(model.parameters(), lr=0.001)
        log_each = 500
        x,fx = torch.FloatTensor(self.x),torch.FloatTensor(self.fx)
        x.requires_grad_(True)
        for step in range(self.epochs):
            for x,fx in self.dataloader:
                y_hat = model(x) 
                loss = criterion(fx, y_hat)
                optimizer.zero_grad()
                loss.backward()
                optimizer.step()
            if step % log_each == 0:
                print(f'{step}/{self.epochs} loss {loss.item():.5f}')
        return model

    def predict(self, z, **kwargs): 
        get_proba = kwargs.get('get_proba',False)
        f_z = []
        with torch.no_grad():
            if get_proba:
                for i,data in enumerate(z):
                    y_pred = self.model(data).clone().detach().numpy()
                    f_z.append(y_pred)
                f_z = np.array(f_z)
            else:
                for i,data in enumerate(z):
                    y_pred = self.model(data)
                    f_z.append(y_pred.argmax().item())
                f_z = np.asarray(f_z).reshape((len(f_z), 1))
        return f_z

    def id(self,name = "Pytorch"):
        return "Pytorch"

class PytorchNet(nn.Module):
    def __init__(self,input_dim, hidden_dim, out_dim, **kwargs):
        super(PytorchNet, self).__init__()
        activations = kwargs.get('activations',np.repeat(nn.ReLU(),len(hidden_dim)))
        dropout = 0.0
        current_dim = input_dim
        layers = []
        for hdim,activation in zip(hidden_dim,activations):
            layers.append(nn.Linear(current_dim, hdim))
            layers.append(activation)
            layers.append(nn.Dropout(p = dropout))
            current_dim = hdim
        layers.append(nn.Linear(current_dim, out_dim))
        self.net = nn.Sequential(*layers)
        print(self.net)

    def forward(self, input:torch.FloatTensor):
        return self.net(input)


if __name__ == "__main__":

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

    def test_pytorch(**kwargs):
        fun = kwargs.get("fun",my_fun)
        pytorch_regressor = kwargs.get("Pytorch_regressor",PytorchRegressor)(**kwargs)
        scenarios_list = [ (1, 100*i, 50,100*i ) for i in np.arange(1,5,1)]
        scenario_generator_ = scenario_generator()
        scenario_generator_.run_scenarios(scenarios_list,
        data_random_generator(fun = fun),
        pytorch_regressor,
        data_accumulator(), **kwargs)
        results = scenario_generator_.accumulator.get_output_datas().dropna(axis=1).T
        print(results)
        list_results = [(s.z,s.f_z) for s in scenario_generator_.accumulator.predictors]
        multi_plot(list_results,plot1D,mp_max_items = len(scenarios_list))
        pass
   
    def get_torch_param():
        return {'PytorchRegressor':
            {'epochs': 500,
            'layers': [128,128,128,128],
            'loss': nn.MSELoss(),
            'activations': [nn.SiLU(),nn.SiLU()],
            'optimizer': torch.optim.Adam,
            }}
    test_pytorch(**get_torch_param())
    


    def quad(x):
        return x ** 2
    
    def get_torch_param():
        return {'PytorchRegressor':
            {'epochs': 500,
            'layers': [128,128,128,128],
            'loss': nn.MSELoss(),
            # 'activations': [nn.SiLU(),nn.SiLU()],
            'optimizer': torch.optim.Adam
            }, 
            'fun': quad}

    test_pytorch(**get_torch_param())
    pass


