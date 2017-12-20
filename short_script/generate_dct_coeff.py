
import sys

# sys.path.append('/Users/dechamoungsri/Dropbox_dechamoungsri/Dropbox/python_workspace/Utility/')
sys.path.append('/home/h1/decha/Dropbox/python_workspace/Utility/')
sys.path.append('../../')
sys.path.append('../')
sys.path.append('/home/h1/decha/Dropbox/python_workspace/Inter_speech_2016/')

from tool_box.util.utility import Utility

from DataModel.Syllables.Syllable import Syllable
from DataModel.Syllables.SyllableDatabaseManagement import SyllableDatabaseManagement

import numpy as np
from scipy.fftpack import dct
from scipy.fftpack import idct

def gen_dct_data(syllable_management_path):

    syl_object = Utility.load_obj(syllable_management_path)

    for syl in syl_object.syllables_list:
        data = syl.get_Y_features(Syllable.Training_feature_tonal_part_raw_remove_head_tail_interpolated, 50, False, False, exp=True, subtract_means=False, output=None, missing_data=False)
        data_dct = dct(data, 2, norm='ortho')
        idct = dct(data_dct, 3, norm='ortho')

        print syl.name_index
        # print data
        # print data_dct
        # print idct

        syl.training_feature[Syllable.Training_feature_tonal_part_dct_coeff] = data_dct

    Utility.save_obj(syl_object, syllable_management_path)

    pass

def run():

    # syllable_management_path = '/home/h1/decha/Dropbox/Inter_speech_2016/Syllable_object/Tonal_object/remove_all_silence_file/all_vowel_type/syllable_object_01234.pickle'

    base = '/home/h1/decha/Dropbox/Inter_speech_2016/Syllable_object/Tonal_object/remove_all_silence_file/'

    for vowel_type in ['all_vowel_type', 'v', 'vv', 'vn', 'vvn', 'vsg', 'vvsg']:
        for tone in ['0','1','2','3','4','01234']:
            syllable_management_path = '{}/{}/syllable_object_{}.pickle'.format(base, vowel_type, tone)
            gen_dct_data(syllable_management_path)

    pass

if __name__ == '__main__':

    run()

    # data = np.array([0,1,2,3,4,3,2,1,0]).astype(float)

    # print data

    # data_dct = dct(data, 2, norm='ortho')
    # print data_dct

    # idct = dct(data_dct, 3, norm='ortho')
    # print idct

    pass
