
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

import itertools

if __name__ == '__main__':

    st = Utility.load_obj('./stress_name_list.npy')
    print st

    pass
