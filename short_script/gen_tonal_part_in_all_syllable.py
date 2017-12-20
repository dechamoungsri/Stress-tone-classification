
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

import numpy as np

def gen(syl_object_path):
    syllable_management = Utility.load_obj(syl_object_path)
    for syl in syllable_management.syllables_list:

        syl.gen_tonal_part_training_feature()

    Utility.save_obj(syllable_management, syl_object_path)
    pass

if __name__ == '__main__':

    # a = np.array([1, 1 , 5, 6, 7,np.nan,2, 5, 9,2])

    # print np.linspace(0, len(a), 50)
    # print np.interp(np.linspace(0, len(a)-1, 50), np.arange(len(a)), a)

    syl_object_path = '/home/h1/decha/Dropbox/Inter_speech_2016/Syllable_object/01_manual_labeling_object/syllable_all.pickle'

    gen()

    syllable_management = Utility.load_obj(syl_object_path)
    for syl in syllable_management.syllables_list:
        # print syl.training_feature[Syllable.Training_feature_tonal_part_raw_remove_head_tail_interpolated]
        y = syl.get_Y_features(Syllable.Training_feature_tonal_part_raw_remove_head_tail_having_missing, num_sampling=50,delta_bool=True, delta2_bool=True, exp=True, missing_data=True)
        # y = np.array(y)
        print syl.phone_duration
        print syl.get_duration([1,2])
        # if syl.name_index == 'tscsd_manual_c16_2':
        #     print y

    pass
