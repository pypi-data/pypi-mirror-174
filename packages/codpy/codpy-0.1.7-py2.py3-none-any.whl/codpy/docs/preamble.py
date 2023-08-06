import os, sys
import time 
import numpy as np
import scipy
from pathlib import Path
parent_path = os.path.dirname(__file__)
parent_path = os.path.dirname(parent_path)
if parent_path not in sys.path: sys.path.append(parent_path)
from include import *
from codpy_tools import *
from data_generators import * 
from predictors import * 
from scikit_tools import * 
from mnist_codpy import * 
from housing_prices import * 
from reordering import * 
from stat_tools import *
from clustering import *
from time_series import * 
from Generator import *
from QL_tools import *
from PNL import *
from MonteCarloImpl import *
from gan_vanilla import *
from book_funs6 import *



plt.close('all')
plt.rc('font', size=6)

