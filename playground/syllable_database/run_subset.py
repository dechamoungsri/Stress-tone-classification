'''
Created on Jan 31, 2559 BE

@author: dechamoungsri
'''

import sys

# sys.path.append('/Users/dechamoungsri/Dropbox_dechamoungsri/Dropbox/python_workspace/Utility/')
sys.path.append('/home/h1/decha/Dropbox/python_workspace/Utility/')
sys.path.append('../../')

from tool_box.util.utility import Utility

from DataModel.Syllables.SyllableDatabaseManagement import SyllableDatabaseManagement
from DataModel.Syllables.Syllable import Syllable

import numpy as np

if __name__ == '__main__':
    
    # dropbox_path = '/Users/dechamoungsri/Dropbox_dechamoungsri/Dropbox/'
    dropbox_path = '/home/h1/decha/Dropbox/'

    # syllables_obj_path = '{}/Inter_speech_2016/Syllable_object/01_manual_labeling_object/Syllable_object.pickle'.format(dropbox_path)
    # outpath = '/home/h1/decha/Dropbox/Inter_speech_2016/temporary_output/'
    
    syllables_obj_path = '/home/h1/decha/Dropbox/Inter_speech_2016/Syllable_object/GPR-data-work-space/gpr_syllable_obj/Syllable_object_a_to_d.pickle'

    syllable_management = Utility.load_obj(syllables_obj_path)
    syllable_management.get_un_voice_file()

    # poly_coeff = np.polyfit([1], [2], 2)
    # print poly_coeff

    print len(syllable_management.syllables_list)

    count = 0

    # tone_list = syllable_management.get_tone_n_syllable(tone)
    # tone_DB = syllable_management
    # count+=len(tone_DB.syllables_list)
    # for syllable in tone_DB.syllables_list:
    #     degree = 2
    #     num_vectors = 50
    #     syllable.set_poly_val(
    #         degree,
    #         Syllable.TRAINING_FEATURE_POLYNOMIAL_2_DEGREE, 
    #         Syllable.TRAINING_FEATURE_POLYNOMIAL_2_DEGREE_VOICE, 
    #         Syllable.COEFFICIENT_POLYNOMIAL_2_DEGREE, num_vectors)
    # tone_DB.dump(syllables_obj_path)

    for tone in [0,1,2,3,4]:
        tone_list = syllable_management.get_tone_n_syllable(tone)
        tone_DB = SyllableDatabaseManagement(syllable_list=tone_list)
        count+=len(tone_DB.syllables_list)
        for syllable in tone_DB.syllables_list:
            degree = 2
            num_vectors = 50
            syllable.set_poly_val(
                degree,
                Syllable.TRAINING_FEATURE_POLYNOMIAL_2_DEGREE, 
                Syllable.TRAINING_FEATURE_POLYNOMIAL_2_DEGREE_VOICE, 
                Syllable.COEFFICIENT_POLYNOMIAL_2_DEGREE, num_vectors)
        tone_DB.dump('/home/h1/decha/Dropbox/Inter_speech_2016/Syllable_object/GPR-data-work-space/gpr_syllable_obj/Syllable_object_a_to_d_tone_{}.pickle'.format(tone))

        print count

    pass