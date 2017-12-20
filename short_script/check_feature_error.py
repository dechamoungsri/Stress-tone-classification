
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
import matplotlib.pyplot as plt

import random

if __name__ == '__main__':

    path = '/home/h1/decha/Dropbox/Inter_speech_2016/Syllable_object/Tonal_object/remove_all_silence_file/all_vowel_type/syllable_object_01234.pickle'

    fig_path = '/home/h1/decha/Dropbox/Inter_speech_2016/temporary_output/'

    syllable_obj = Utility.load_obj(path)

    syllable_obj.get_GP_LVM_training_data(Syllable.Training_feature_phone_tonal_separated_with_noise_reduction, [1,2], exp=False, delta_bool=True, delta2_bool=True, num_sampling=25)

    # while True:
    #     syl = syllable_obj.syllables_list[ int(random.random() * len(syllable_obj.syllables_list)) ]

    #     print syl.consonant, syl.vowel, syl.final_consonant, syl.tone, syl.stress_manual
    #     if syl.final_consonant != 'z^': break

    # new_feature = syl.get_Y_features(Syllable.Training_feature_phone_tonal_separated_with_noise_reduction, 25, delta_bool=True, delta2_bool=True)
    # # new_feature = syl.get_Y_features(Syllable.Training_feature_tonal_part_raw_remove_head_tail_interpolated, 25, delta_bool=True, delta2_bool=True)

    # print len(new_feature)

    # if syl.final_consonant == 'z^':
        
    #     plt.plot(np.arange(25, dtype=int), new_feature[0:25]-np.mean(new_feature[0:25]))
    #     plt.plot(np.arange(25, dtype=int), new_feature[25:50])
    #     plt.plot(np.arange(25, dtype=int), new_feature[50:75])
    #     plt.savefig('{}/check_vowel.pdf'.format(fig_path))
    #     sys.exit()

    # plt.plot(np.arange(25, dtype=int), new_feature[0:25]-np.mean(new_feature[0:25]))
    # plt.plot(np.arange(25, dtype=int), new_feature[25:50])
    # plt.plot(np.arange(25, dtype=int), new_feature[50:75])
    # plt.savefig('{}/check_vowel.pdf'.format(fig_path))

    # plt.clf()
    # plt.plot(np.arange(25, dtype=int), new_feature[75:100]-np.mean(new_feature[75:100]))
    # plt.plot(np.arange(25, dtype=int), new_feature[100:125])
    # plt.plot(np.arange(25, dtype=int), new_feature[125:150])
    # plt.savefig('{}/check_final_consonant.pdf'.format(fig_path))

    

    pass