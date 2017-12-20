
import sys
sys.path.append('../')
sys.path.append('/home/h1/decha/Dropbox/python_workspace/Utility/')

import GPy

from tool_box.util.utility import Utility

class GPModelByGPy(object):

    @staticmethod
    def execute_training(x, y, outpath, optimize=True):
        m = GPy.models.GPRegression(x, y)
        if optimize: 
            m.optimize('bfgs')

        Utility.save_obj(m, outpath)

    def __init__(self, params):
        '''
        Constructor
        '''

    pass
