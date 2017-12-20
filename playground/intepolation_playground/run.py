'''
Created on Jan 27, 2016

@author: decha
'''

import sys

# sys.path.append('/Users/dechamoungsri/Dropbox_dechamoungsri/Dropbox/python_workspace/Utility/')
sys.path.append('/home/h1/decha/Dropbox/python_workspace/Utility/')
sys.path.append('../../')

from tool_box.util.utility import Utility
from DataModel.Syllables.SyllableDatabaseManagement import SyllableDatabaseManagement
from DataModel.Syllables.Syllable import Syllable

from Data_Processing.Inteporation_method.Interpolation import Interpolation

if __name__ == '__main__':
    
    syllables_obj_path = '/home/h1/decha/Dropbox/Inter_speech_2016/Syllable_object/01_manual_labeling_object/Syllable_object.pickle'
    outpath = '/home/h1/decha/Dropbox/Inter_speech_2016/temporary_output/'
    
    syllable_management = Utility.load_obj(syllables_obj_path)
    
    syllable = syllable_management.get_syllable_at_index(2548)

    # poly_coeff = Interpolation.poly_nomial_interpolate(syllable.raw_data, 2)
    
    # print poly_coeff
    
    degree = 2

    syllable.set_poly_val(degree,Syllable.TRAINING_FEATURE_POLYNOMIAL_2_DEGREE, Syllable.TRAINING_FEATURE_POLYNOMIAL_2_DEGREE_VOICE, Syllable.COEFFICIENT_POLYNOMIAL_2_DEGREE, 50)
    syllable.plot('{}/{}.eps'.format(outpath,syllable.name_index), Syllable.TRAINING_FEATURE_POLYNOMIAL_2_DEGREE)
    
    syllable.plot('{}/{}_voice.eps'.format(outpath,syllable.name_index), Syllable.TRAINING_FEATURE_POLYNOMIAL_2_DEGREE_VOICE, voice=True)
    
    pass