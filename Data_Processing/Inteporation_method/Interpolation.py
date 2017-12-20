'''
Created on Jan 27, 2016

@author: decha
'''

import numpy as np

class Interpolation(object):
    '''
    classdocs
    '''
    
    un_voice_value = -1.00000000e+10
    
    @staticmethod
    def poly_nomial_interpolate(lf0_contour, degree):
        
        lf0 = lf0_contour
        
        x = np.arange(len(lf0))

        un_voice_index = np.where(lf0==Interpolation.un_voice_value)

        lf0 = np.delete(lf0, un_voice_index)
        x = np.delete(x, un_voice_index)

        if len(x) == 1:
            x = [1]

        if len(x) == 0:
            lf0 = [1]
            x = [1]

        # print lf0, x

        poly_coeff = np.polyfit(x, lf0, degree)
        np.set_printoptions(precision=10,
                       suppress=True)

        return poly_coeff
        
        pass


    def __init__(self, params):
        '''
        Constructor
        '''
        