
import sys

# sys.path.append('/Users/dechamoungsri/Dropbox_dechamoungsri/Dropbox/python_workspace/Utility/')
sys.path.append('/home/h1/decha/Dropbox/python_workspace/Utility/')
sys.path.append('../../')
sys.path.append('../')
sys.path.append('/home/h1/decha/Dropbox/python_workspace/Inter_speech_2016/')
import matplotlib.mlab as mlab
from tool_box.util.utility import Utility
import scipy.stats as stats
from DataModel.Syllables.Syllable import Syllable
from DataModel.Syllables.SyllableDatabaseManagement import SyllableDatabaseManagement

import numpy as np
import matplotlib.pyplot as plt

import GPy

if __name__ == '__main__':

    x1 = np.array([[1,1]])
    x2 = np.array([[0,1]])

    k1 = GPy.kern.Linear(input_dim=1, active_dims=[0])
    # k2 = GPy.kern.Linear(input_dim=1, active_dims=[1])

    k = k1

    print k.K(x1,x2)

    pass
